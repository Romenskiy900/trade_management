from odoo import models, fields, api
from datetime import date


class TradeDocumentMixin(models.AbstractModel):
    """
    Abstract mixin for automatic document numbering and name generation.
    """

    _name = 'trade.document.mixin'
    _description = 'Document numbering mixin'

    sequence_code = 'trade.document.common'  # ir.sequence code for numbering
    prefix = None  # document type prefix (defined in child models)

    number = fields.Char(string="Number", readonly=True, copy=False)
    name = fields.Char(string="Name", readonly=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        """
        Generate sequence number and document name.
        """

        for vals in vals_list:
            seq = self.env['ir.sequence'].next_by_code(self.sequence_code)
            vals['number'] = seq or '00000'

            today = date.today()
            vals['name'] = f"{self.prefix}/{today}/{vals['number']}"

        return super().create(vals_list)