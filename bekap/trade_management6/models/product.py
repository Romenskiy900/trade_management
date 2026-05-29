from odoo import models, fields


class TradeProduct(models.Model):
    _inherit = 'product.template'

    sale_type = fields.Selection([
        ('retail', 'Розница'),
        ('wholesale', 'Опт'),
    ], string='Тип продажу')