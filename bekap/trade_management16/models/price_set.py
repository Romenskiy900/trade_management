from odoo import models, fields


class TradePriceSet(models.Model):
    _name = 'trade.management.price.set'
    _description = 'Price Set'
    _inherit = 'trade.document.mixin'

    prefix = 'Встановлення цін'

    date = fields.Date(
        string="Date",
        default=fields.Date.context_today
    )
    line_ids = fields.One2many(
        'trade.management.price.set.line',
        'price_set_id'
    )