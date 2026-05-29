from odoo import models, fields, api


class TradePriceSet(models.Model):
    _name = 'trade.management.price.set'
    _description = 'Встановлення цін'

    name = fields.Char(
        string='Номер',
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )

    line_ids = fields.One2many(
        'trade.management.price.set.line',
        'price_set_id',
        string='Товари'
    )

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:

            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'trade.management.price.set'
                ) or 'New'

        return super().create(vals_list)