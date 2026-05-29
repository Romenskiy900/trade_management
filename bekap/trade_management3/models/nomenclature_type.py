from odoo import models, fields

class TradeNomenclatureType(models.Model):
    _name = "trade.management.nomenclature.type"
    _description = "Вид номенклатури"

    name = fields.Char(string="Найменування", required=True)
