from odoo import models, fields

class TradeNomenclature(models.Model):
    _name = "trade.management.nomenclature"
    _description = "Номенклатура"

    name = fields.Char(string="Найменування", required=True)

    type_id = fields.Many2one(
        "trade.management.nomenclature.type",
        string="Вид номенклатури",
        required=True
    )
