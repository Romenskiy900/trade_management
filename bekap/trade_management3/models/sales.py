from odoo import models, fields, api


class TradeSales(models.Model):
    _name = 'trade.management.sales'
    _description = 'Регістрація продажів'
    _inherit = 'trade.document.mixin'

    prefix = 'ЧекККМ'

    line_ids = fields.One2many(
        'trade.management.sales.line',
        'sales_id',
        string='Товари'
    )

    # @api.model_create_multi
    # def create(self, vals_list):
    #
    #     for vals in vals_list:
    #
    #         if vals.get('name', 'New') == 'New':
    #             vals['name'] = self.env['ir.sequence'].next_by_code(
    #                 'trade.management.sales'
    #             ) or 'New'
    #
    #     return super().create(vals_list)