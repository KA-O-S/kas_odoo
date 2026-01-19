# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

_logger.warning("!!! Achtung laedt Datei !!!")


class AccountMove(models.Model):
    _inherit = "account.move"

    _logger.warning("--- Achtung laedt Klasse")

    period_performance = fields.Char(string="Leistungszeitraum")
    origin_contract = fields.Many2one('sale.order', string="Vertrag Ursprung")
    invoice_number = fields.Char(readonly=True)
    with_timesheet = fields.Boolean(string="Mit Zeitnachweis" ,default=False)
    with_prepayment = fields.Boolean(string="Vorkasse", default=False)

    def action_post(self):
        for move in self:
            if move.move_type in ['out_invoice', 'in_invoice'] and not move.invoice_number:
                prefix = move.company_id.sequence_prefix
                sequence_code = ''
                if prefix == 'kasb':
                    sequence_code = 'kas_be.invoice'
                elif prefix == 'kasr':
                    sequence_code = 'kas_re.invoice'
                else:
                    sequence_code = 'sale.order'
                move.invoice_number = self.env['ir.sequence'].next_by_code(sequence_code)
        return super(AccountMove, self).action_post()