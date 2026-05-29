from odoo import models, fields


class TradePriceSetLine(models.Model):
    _name = 'trade.management.price.set.line'
    _description = 'Рядок встановлення цін'

    price_set_id = fields.Many2one(
        'trade.management.price.set',
        string='Установка цен',
        ondelete='cascade'
    )

    nomenclature_id = fields.Many2one(
        'trade.management.nomenclature',
        string='Номенклатура',
        required=True
    )

    price = fields.Float(string='Цена')