from odoo import models, fields, api
from odoo.exceptions import ValidationError


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

    # FIXED: Added required=True so Odoo never sends NULL to PostgreSQL
    quantity = fields.Integer(
        string='Quantity',
        required=True,
    )

    # Standard Odoo Python validation triggered on save
    @api.constrains('quantity')
    def _check_quantity_positive(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError("The quantity must be greater than zero!")