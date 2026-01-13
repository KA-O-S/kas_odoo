# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pre_block = fields.Html(string="Pre-Block")
    sub_block = fields.Html(string="Sub-Block")
    contract_components_ids = fields.Many2many(
        comodel_name="sale.order.contract",
        string="Text Blöcke",

        store=True
    )
    contract_components = fields.One2many(
        comodel_name="sale.order.contract",
        inverse_name="order_id",
        string="Text Blöcke",
    )
    date_initial_contract = fields.Date(string="Rahmenvertrag vom")
    date_contract_duration = fields.Date(string="Vertragsdauer")
    page_break_signature = fields.Boolean(string="Page Break Unterschrift")
    page_break_orderline = fields.Boolean(string="Page Break Order Lines")
    order_line_section = fields.One2many(
        'sale.order.line', 'order_id',
        string='Sections',
        domain=[('display_type', '=', 'line_section')]
    )

    # Für die Funktion Auftragsdatum im Timesheet --> Modul kas_extension
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['origin_contract'] = self.id
        return invoice_vals
    @api.model
    def default_get(self, fields_list):
        res = super(SaleOrder, self).default_get(fields_list)
        current_company = self.env.company.id
        components = self.env['contract.components'].search([('active', '=', True), ('company_id', '=', current_company)])

        contract_components = []
        for component in components:

            contract_component = self.env['sale.order.contract'].create({
                'title': component.title,
                'name': component.name,
                'text_block': component.text_block,
                'position': component.position,
                'model_id' : component.model_id.id,
                'order_inline_text' : component.order_inline_text,
                'section_signature' : component.section_signature,
            })
            contract_components.append(contract_component.id)
        res['contract_components'] = [(6, 0, contract_components)]
        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    #ToDo remove Field print_price if not used
    print_price =fields.Boolean(string="Mit Preis", default=True)
    section_pauschal = fields.Boolean(string="Pauschal", default=False)
    section_stundensatz = fields.Boolean(string="Stundensatz", default=False)

class SaleOrderContract(models.Model):
    _name = 'sale.order.contract'
    _description = "Sale Order Contract Componentes"
    _check_company_auto = True


    name = fields.Char(string="§. Überschrift")
    title = fields.Char(string="Beschreibung")
    text_block = fields.Html(string="Text")
    order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Verkaufsauftrag"
    )
    sequence = fields.Integer(string="Sequence")
    position = fields.Selection([
        ('pre', 'Pre-Block'),
        ('sub', 'Sub-Block')
    ],
        string="Text-Position", default='pre',
        help="Position des Textblocks im Vertrag."
             " 1. vor oder nach den Auftragspositionen."
             " 2. Bei Teileistungsvertrag ’Inline' bestimmt die Auswahl vor oder nach den Leistungspositionen"
    )
    page_break = fields.Boolean(string="Page Break", default=False)
    model_id = fields.Many2one(
        comodel_name='ir.model'
    )
    order_inline_text = fields.Boolean(string="Inline")
    section_signature = fields.Boolean(string="Im Unterschriftblock", default=False)