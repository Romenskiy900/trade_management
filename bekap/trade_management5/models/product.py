from odoo import models, fields


class TradeProduct(models.Model):
    _inherit = 'product.template'


    trade_code2 = fields.Char(string="Код товара2")
    is_trade_item = fields.Boolean(string="Товар (Trade Module)")