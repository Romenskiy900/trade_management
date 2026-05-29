from odoo import models, fields


class Tradesalesline(models.Model):
    _name = 'trade.management.sales.line'
    _description = 'Рядок товарів'

    sales_id = fields.Many2one(
        'trade.management.sales',
        string='Товари',
        ondelete='cascade'
    )

    nomenclature_id = fields.Many2one(
        'trade.management.nomenclature',
        string='Номенклатура',
        required=True
    )

    quantity = fields.Integer(string='Кількість')

    price = fields.Float(string='Ціна')