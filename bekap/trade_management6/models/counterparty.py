from odoo import models, fields

class TradeCounterparty(models.Model):
    _name = "trade.management.counterparty"
    _description = "Контрагенти"

    name = fields.Char(string="ПІБ", required=True)

