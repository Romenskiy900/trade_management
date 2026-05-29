from odoo import models, fields


class ProductCategoryWizard(models.TransientModel):
    _name = 'product.category.wizard'
    _description = 'Mass Change Product Category'

    product_ids = fields.Many2many(
        'product.template',
        string='Products'
    )

    categ_id = fields.Many2one(
        'product.category',
        string='New Category',
        required=True
    )

    def action_apply(self):
        self.product_ids.write({
            'categ_id': self.categ_id.id
        })