import logging
import subprocess
import os
from odoo import models, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _call_playwright_render_subprocess(self, html):
        addon_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(addon_path, 'kas_playwright_runner.py')

        if not os.path.exists(script_path):
            _logger.error(f"Playwright-Runner-Skript nicht gefunden unter: {script_path}")
            raise UserError(_("Das Playwright-Hilfsskript konnte nicht gefunden werden."))

        _logger.info(f"Starte Playwright-Subprozess mit Skript: {script_path}")
        html_bytes = html.encode('utf-8')
        
        try:
            process = subprocess.run(
                ['python3', script_path],
                input=html_bytes,
                capture_output=True,
                check=True,
                timeout=60
            )
            
            pdf_data = process.stdout
            
            if process.stderr:
                _logger.warning(f"Playwright-Subprozess-Log: {process.stderr.decode('utf-8', errors='ignore')}")

            if not pdf_data:
                raise UserError(_("Die PDF-Generierung ergab eine leere Datei."))

            _logger.info(f"Playwright-Subprozess erfolgreich. PDF-Groesse: {len(pdf_data)} bytes.")
            return pdf_data

        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode('utf-8', errors='ignore')
            _logger.error(f"Playwright-Subprozess fehlgeschlagen. Fehler: {error_message}")
            raise UserError(_("Fehler bei der PDF-Generierung: %(error)s", error=error_message))
        except subprocess.TimeoutExpired:
            _logger.error("Playwright-Subprozess hat das Zeitlimit von 60s ueberschritten.")
            raise UserError(_("Die PDF-Generierung hat zu lange gedauert und wurde abgebrochen."))
        except Exception as e:
            _logger.error(f"Unerwarteter Fehler beim Aufruf des Playwright-Subprozesses: {e}", exc_info=True)
            raise UserError(_("Ein unerwarteter Fehler ist bei der PDF-Generierung aufgetreten."))

    @api.model
    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        report = self._get_report(report_ref)
        _logger.info(f"KAS PDF (Playwright/Subprozess): Rendering fuer '{report.name}' angefordert.")
        
        try:
            html_content, _ = self._render_qweb_html(report_ref, res_ids, data)
            if isinstance(html_content, bytes):
                html_content = html_content.decode('utf-8')
            
            pdf_data = self._call_playwright_render_subprocess(html_content)
            
            return pdf_data, 'pdf'
            
        except Exception as e:
            _logger.error(f"Kritischer Fehler bei Playwright-Rendering von '{report.name}'. Fallback zu wkhtmltopdf wird versucht. Fehler: {e}", exc_info=True)
            return super()._render_qweb_pdf(report_ref, res_ids, data)
