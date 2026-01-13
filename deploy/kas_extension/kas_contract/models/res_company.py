# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Company(models.Model):
    _inherit = "res.company"


    contract_logo = fields.Binary("Logo Contract")
    contract_footer = fields.Binary("Footer Contract")