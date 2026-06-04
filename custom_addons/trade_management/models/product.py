from odoo import models, fields, api


class TradeProduct(models.Model):
    _inherit = 'product.template'

    sale_type = fields.Selection([
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
    ], string='Type of sale')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Make products storable by default
            if 'is_storable' not in vals:
                vals['is_storable'] = True

        return super(TradeProduct, self).create(vals_list)