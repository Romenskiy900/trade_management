from odoo import models, fields, api


class TradeReceipt(models.Model):
    _name = 'trade.management.receipt'
    _description = 'Надходження товарів'
    _inherit = 'trade.document.mixin'

    prefix = 'Надходження товарів'

    counterparty_id = fields.Many2one(
        "trade.management.counterparty",
        string="Контрагент",
        required=True
    )

    line_ids = fields.One2many(
        'trade.management.receipt.line',
        'receipt_id',
        string='Товари'
    )


