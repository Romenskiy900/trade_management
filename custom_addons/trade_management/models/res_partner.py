from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"


    is_trade_partner = fields.Boolean(
        string="Trade counterparty"
    )