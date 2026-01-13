# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    contact_person = fields.Many2many(
        'res.partner',
        'kas_partner_res_partner_rel',
        string= 'Kontakt')
    contact_partner_allg = fields.Many2many(
        'res.partner',
        'kas_partner_allg_res_partner_rel',
        string='Allg. Kontakt')
    contact_person_names = fields.Char(string='Contact Person Names', compute='get_contact_person_names')

    def get_contact_person_names(self):
        for record in self:
            contact_person_names = ', '.join(record.contact_person.mapped('name'))
            contact_partner_allg_names = ', '.join(record.contact_partner_allg.mapped('name'))
            combined_names = ', '.join(filter(None, [contact_person_names, contact_partner_allg_names]))
            record.contact_person_names = combined_names