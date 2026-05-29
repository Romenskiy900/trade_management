from odoo import models, fields

class TradeNomenclature(models.Model):
    _name = "trade.management.nomenclature"
    _description = "Номенклатура"

    name = fields.Char(string="Найменування", required=True)

    type = fields.Selection([
        ('product', 'Товар'),
        ('service', 'Послуга'),
        ('raw', 'Сировина'),
    ], string="Вид номенклатури", default='product', required=True)