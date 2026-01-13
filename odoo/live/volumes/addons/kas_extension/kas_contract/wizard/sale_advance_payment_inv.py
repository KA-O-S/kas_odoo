# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.tools import format_date, frozendict

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    consolidated_billing = fields.Boolean(
        string="Consolidated Bill", default=False,
        help="Create one invoice for all orders related to same customer and same invoicing address"
    )


