# /home/docker/odoo/live/volumes/addons/odoo_chrome_pdf/models/ir_actions_report.py

import logging
import subprocess
import os
from odoo import models, api, _
from odoo.exceptions import UserError
import json
from bs4 import BeautifulSoup

_logger = logging.getLogger(__name__)

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _call_playwright_render_subprocess(self, payload):
        # DIESE FUNKTION IST KORREKT UND BLEIBT UNVERÄNDERT
        addon_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(addon_path, 'kas_playwright_runner.py')
        input_bytes = json.dumps(payload).encode('utf-8')
        try:
            process = subprocess.run(['python3', script_path], input=input_bytes, capture_output=True, check=True, timeout=60)
            return process.stdout
        except Exception as e:
            _logger.error(f"Fehler im Playwright-Subprozess: {e}", exc_info=True)
            raise UserError(_("Fehler bei der PDF-Generierung durch Playwright."))

    @api.model
    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        report = self._get_report(report_ref)
        _logger.info(f"DEBUGGING-MODUS: Rendering fuer '{report.name}' gestartet.")
        header_html = ""
        body_html = ""
        footer_html = ""

        try:
            # HOLEN DER ROH-HTML-DATEN (DIESE ZEILE FEHLTE)
            
            report_model = self.env[report.model]
            docs = report_model.browse(res_ids)
            # render_context = {'docs': docs, 'company': self.env.company}
            # WICHTIG: Vollständige render_context für das neue Header-Template
            doc = docs[0] if docs else None
            render_context = self._get_rendering_context(report, res_ids, data)
            company = doc.company_id if doc else self.env.company
            render_context.update({
                'docs': docs,
                'o': doc,
                'company': company,
            })
            
            # ======================= MINIMALINVASIVE ÄNDERUNG START =======================
            # 1. Fülle header_html durch direkten Aufruf des neuen Templates
            header_html = self.env['ir.qweb']._render('kas_contract.kas_layout_header', render_context)
            if isinstance(header_html, bytes):
                header_html = header_html.decode('utf-8')
            _logger.info(f"DEBUG DIREKT GERENDERTER HEADER: {header_html[:500]}")
            # ======================== MINIMALINVASIVE ÄNDERUNG ENDE =======================
            
            
            full_html = self.env['ir.qweb']._render(report.report_name, render_context)
            
            if isinstance(full_html, bytes):
                full_html = full_html.decode('utf-8')
            _logger.info(f"ROH-HTML VOR ZERLEGUNG: {full_html[:12500]}")
            soup = BeautifulSoup(full_html, 'html.parser')

            # Extrahiere den Header
            header_tag = soup.find('div', class_='header')
            if header_tag:
                # header_html = str(header_tag)
                header_tag.decompose()
            _logger.info(f"ZERLEGT (BS4) - HEADER: {header_html[:300]}")

            # ======================= MINIMALINVASIVE ÄNDERUNG FÜR FOOTER START =======================
            # 1. Fülle footer_html durch direkten Aufruf des neuen Templates (kopiert vom Header)
            footer_html = self.env['ir.qweb']._render('kas_contract.kas_layout_footer', render_context)
            if isinstance(footer_html, bytes):
                footer_html = footer_html.decode('utf-8')
            _logger.info(f"DEBUG DIREKT GERENDERTER FOOTER: {footer_html[:11500]}")
            
            # Extrahiere den Footer
            footer_tag = soup.find('div', class_='footer')
            if footer_tag:
                #footer_html = str(footer_tag)
                footer_tag.decompose()
            _logger.info(f"ZERLEGT (BS4) - FOOTER: {footer_html[:11300]}")
            
            # Der Body ist der verbleibende Inhalt des <body>-Tags
            body_tag = soup.find('body')
            if body_tag:
                body_html = body_tag.decode_contents()
            _logger.info(f"ZERLEGT (BS4) - BODY: {body_html[:11300]}")

            payload = {
                'body': body_html,
                'header': header_html,
                'footer': footer_html,
            }

            pdf_data = self._call_playwright_render_subprocess(payload)
            return pdf_data, 'pdf'
            
        except Exception as e:
            _logger.error(f"Kritischer Fehler bei DEBUG-Rendering. Fehler: {e}", exc_info=True)
            return super()._render_qweb_pdf(report_ref, res_ids, data)