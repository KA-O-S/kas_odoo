# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    period_performance = fields.Char(string="Leistungszeitraum")
    origin_contract = fields.Many2one('sale.order', string="Vertrag Ursprung")
    invoice_number = fields.Char(readonly=True)

    def action_post(self):
        for move in self:
            if move.move_type in ['out_invoice', 'in_invoice'] and not move.invoice_number:
                if move.company_id.id == 1:
                    sequence_code = 'kas_be.invoice'
                else:
                    sequence_code = 'kas_re.invoice'
                move.invoice_number = self.env['ir.sequence'].next_by_code(sequence_code)
        return super(AccountMove, self).action_post()