from odoo import models, fields


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

    price = fields.Float(string='Price')