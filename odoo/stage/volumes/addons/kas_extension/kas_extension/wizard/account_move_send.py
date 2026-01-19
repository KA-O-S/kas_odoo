# -*- coding: utf-8 -*-
from odoo import api, models
import logging

_logger = logging.getLogger(__name__)

class AccountMoveSend(models.TransientModel):
    _inherit = 'account.move.send'

    @api.model
    def _prepare_invoice_pdf_report(self, invoice, invoice_data):
        """
        FINALE, BEWIESENE KORREKTUR: Erzwingt das Rendering des korrekten Reports.

        GRUND: Der Standard-Wizard-Pfad verwendet einen hartcodierten Report-Namen,
        der die `odoo_chrome_pdf`-Engine umgeht. Ein direkter Aufruf von _render_qweb_pdf
        fuehrt zu Folgefehlern.

        LOESUNG: Wir ueberschreiben die Methode und rufen die offizielle, stabile
        `_render`-Methode von `ir.actions.report` mit dem korrekten, als String
        uebergebenen Report-Namen auf. Diese Methode wird korrekt von `odoo_chrome_pdf`
        abgefangen und verarbeitet.
        """
        _logger.warning("!!! FINALE KORREKTUR V3: _prepare_invoice_pdf_report wird aufgerufen. !!!")

        if invoice.invoice_pdf_report_id:
            _logger.warning("--- PDF existiert bereits (ID: %s). Wiederverwendung.", invoice.invoice_pdf_report_id.id)
            return

        # Dies ist der technische Name der QWeb-Vorlage, die gedruckt werden soll.
        # Da `odoo_chrome_pdf` auf `ir.actions.report` lauscht, wird dieser Aufruf abgefangen.
        correct_report_name = 'kas_extension.report_invoice_account_move_kas'
        _logger.warning("--- Verwende Report-Namen: %s", correct_report_name)

        content, report_format = self.env['ir.actions.report']._render(correct_report_name, invoice.ids)

        _logger.warning("--- Rendering abgeschlossen. Format: %s, Groesse: %s bytes.", report_format, len(content))

        # Füge das Ergebnis dem Wizard hinzu.
        invoice_data['pdf_attachment_values'] = {
            'raw': content,
            'name': invoice._get_invoice_report_filename(),
            'mimetype': 'application/pdf',
            'res_model': invoice._name,
            'res_id': invoice.id,
            'res_field': 'invoice_pdf_report_file',
        }