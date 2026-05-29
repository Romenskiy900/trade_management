from odoo import models, fields


class Tradesalesline(models.Model):
    _name = 'trade.management.sales.line'
    _description = 'Рядок товарів'

    sales_id = fields.Many2one(
        'trade.management.sales',
        string='Products',
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        'product.template',
        string='Product',
        required=True
    )

    quantity = fields.Integer(string='Quantity')

    price = fields.Float(string='Price')

    sum = fields.Float(string='Sum')
