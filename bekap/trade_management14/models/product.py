from odoo import models, fields


class TradeProduct(models.Model):
    _inherit = 'product.template'

    sale_type = fields.Selection([
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
    ], string='Type of sale')

