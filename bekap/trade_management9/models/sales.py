from odoo import models, fields, api


class TradeSales(models.Model):
    _name = 'trade.management.sales'
    _description = 'Регістрація продажів'
    _inherit = 'trade.document.mixin'

    prefix = 'Чек ККМ'

    line_ids = fields.One2many(
        'trade.management.sales.line',
        'sales_id',
        string='Product'
    )


