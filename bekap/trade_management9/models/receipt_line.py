from odoo import models, fields


class TradeReceiptline(models.Model):
    _name = 'trade.management.receipt.line'
    _description = 'Рядок товарів'

    receipt_id = fields.Many2one(
        'trade.management.receipt',
        string='Products',
    )

    product_id = fields.Many2one(
        'product.template',
        string='Product',
        required=True
    )

    quantity = fields.Integer(string='Quantity')