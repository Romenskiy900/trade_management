from odoo import models, fields


class TradeProduct(models.Model):
    _inherit = 'product.template'

    sale_type = fields.Selection([
        ('retail', 'Роздріб'),
        ('wholesale', 'Опт'),
    ], string='Тип продажу')