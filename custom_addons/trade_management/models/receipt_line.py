from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TradeReceiptline(models.Model):
    _name = 'trade.management.receipt.line'
    _description = 'Receipt line'

    # reference to parent receipt document
    receipt_id = fields.Many2one(
        'trade.management.receipt',
        string='Products',
    )

    # product being received in this line
    product_id = fields.Many2one(
        'product.template',
        string='Product',
        required=True
    )

    # quantity of product in this receipt line
    quantity = fields.Integer(
        string='Quantity',
        required=True,
    )

    # validation rule to ensure quantity is always positive
    @api.constrains('quantity')
    def _check_quantity_positive(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError("The quantity must be greater than zero!")