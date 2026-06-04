from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TradeReceiptline(models.Model):

    _name = 'trade.management.receipt.line'
    _description = 'Receipt line'

    receipt_id = fields.Many2one('trade.management.receipt', string='Products')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Integer(string='Quantity', required=True)

    # Ensure quantity is positive
    @api.constrains('quantity')
    def _check_quantity_positive(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError("The quantity must be greater than zero!")