from odoo import models, fields, api
from datetime import date


class TradeDocumentMixin(models.AbstractModel):
    """
    Абстрактна модель для формування номерів документів
    та автоматичної генерації унікального імені.
    """

    _name = 'trade.document.mixin'
    _description = 'Document numbering mixin'

    sequence_code = 'trade.document.common'
    prefix = None


    number = fields.Char(string="Number",readonly=True, copy=False)
    name = fields.Char(string="Name",readonly=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:

            seq = self.env['ir.sequence'].next_by_code(self.sequence_code)
            vals['number'] = seq or '00000'

            today = date.today()

            vals['name'] = f"{self.prefix}/{today}/{vals['number']}"

        return super().create(vals_list)