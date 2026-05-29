from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TradePriceSetLine(models.Model):
    _name = 'trade.management.price.set.line'
    _description = 'Рядок встановлення цін'

    price_set_id = fields.Many2one(
        'trade.management.price.set',
        string='Price setting',
    )


    product_id = fields.Many2one(
        'product.template',
        string='Product',
        required=True
    )

    price = fields.Float(string='Price',
                         required=True,)

    # Standard Odoo Python validation triggered on save
    @api.constrains('quantity')
    def _check_quantity_positive(self):
        for rec in self:
            if rec.price <= 0:
                raise ValidationError("The price must be greater than zero!")