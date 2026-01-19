from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    sequence_prefix = fields.Char(
        string="Firmenidentifikationscode",
        help="Einzigartiger Code pro Unternehmen, der zur Generierung von Sequenz-Codes verwendet wird (z.B. 'kas_be')."
    )