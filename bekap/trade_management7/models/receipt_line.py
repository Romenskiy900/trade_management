from odoo import models, fields


class TradeReceiptline(models.Model):
    _name = 'trade.management.receipt.line'
    _description = 'Рядок товарів'

    receipt_id = fields.Many2one(
        'trade.management.receipt',
        string='Товари',
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        'product.template',
        string='Товар',
        required=True
    )

    quantity = fields.Integer(string='Кількість')