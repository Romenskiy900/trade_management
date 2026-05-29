from odoo import models, fields, api


class TradeReceipt(models.Model):
    _name = 'trade.management.receipt'
    _description = 'Reliability of goods'
    _inherit = 'trade.document.mixin'

    prefix = 'Reliability of goods'

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


