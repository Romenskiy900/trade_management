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

    date = fields.Date(
        string='Date',
        related='price_set_id.date',
        store=True,
        readonly=True
    )

    price = fields.Float(string='Price',
                         required=True,)

    # Standard Odoo Python validation triggered on save
    @api.constrains('price')
    def _check_quantity_positive(self):
        for rec in self:
            if rec.price <= 0:
                raise ValidationError("The price must be greater than zero!")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            rec.product_id.list_price = rec.price
        return records

    def write(self, vals):
        res = super().write(vals)  # Записываем данные в текущую модель
        if 'price' in vals or 'product_id' in vals:
            for rec in self:
                rec.product_id.list_price = rec.price
        return res