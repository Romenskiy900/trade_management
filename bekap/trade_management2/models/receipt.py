from odoo import models, fields, api


class TradeReceipt(models.Model):
    _name = 'trade.management.receipt'
    _description = 'Надходження товарів'
    _inherit = 'trade.document.mixin'

    prefix = 'Надходження товарів'

    line_ids = fields.One2many(
        'trade.management.receipt.line',
        'receipt_id',
        string='Товари'
    )

    # @api.model_create_multi
    # def create(self, vals_list):
    #
    #     for vals in vals_list:
    #
    #         if vals.get('name', 'New') == 'New':
    #             vals['name'] = self.env['ir.sequence'].next_by_code(
    #                 'trade.management.receipt'
    #             ) or 'New'
    #
    #     return super().create(vals_list)