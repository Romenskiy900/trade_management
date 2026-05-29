from odoo import models, fields, api


class TradeReceipt(models.Model):
    _name = 'trade.management.receipt'
    _description = 'Надходження товарів'
    _inherit = 'trade.document.mixin'

    prefix = 'Надходження товарів'

    pertner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True
    )

    date = fields.Datetime(default=fields.Datetime.now)

    line_ids = fields.One2many(
        'trade.management.receipt.line',
        'receipt_id',
        string='Product'
    )


