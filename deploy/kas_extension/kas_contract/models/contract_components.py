# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ContractComponents(models.Model):
    _name = 'contract.components'
    _inherit = ['mail.render.mixin', 'template.reset.mixin']
    _description = "Contract Componentes"
    _check_company_auto = True



    name = fields.Char(
        string='§. Überschrift',
        required = False,
        copy= True,
        readonly=False,
        help='Titel as § in Contract'
    )
    title = fields.Char(
        string='Beschreibung',
        required = False,
        copy= False,
        readonly=False,

    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True, index=True,
        default=lambda self: self.env.company
    )
    active = fields.Boolean(string='Active', default=True)
    text_block = fields.Html(string='Text', render_engine='qweb')
    model_id = fields.Many2one(
        comodel_name='ir.model'
    )
    sequence = fields.Integer(string="Sequence", default=10)
    position = fields.Selection([
        ('pre', 'Pre-Block'),
        ('sub', 'Sub-Block')
    ],
        string="Text-Position", default='pre', help="Position des Textblocks im Vertrag."
                                                    " 1. vor oder nach den Auftragspositionen."
                                                    " 2. Bei Teileistungsvertrag ’Inline' bestimmt die Auswahl vor oder nach den Leistungspositionen" )
    order_inline_text = fields.Boolean(string="Inline")
    section_signature = fields.Boolean(string="Im Unterschriftblock", default=False)


