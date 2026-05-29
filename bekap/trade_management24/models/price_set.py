from odoo import models, fields


class TradePriceSet(models.Model):
    _name = 'trade.management.price.set'
    _description = 'Price Set'
    _inherit = 'trade.document.mixin'

    # human-readable prefix used in generated document name (from mixin)
    prefix = 'Established price'

    # document date (defaults to current user context date)
    date = fields.Date(
        string="Date",
        default=fields.Date.context_today
    )

    # lines belonging to this price set
    line_ids = fields.One2many(
        'trade.management.price.set.line',
        'price_set_id'
    )