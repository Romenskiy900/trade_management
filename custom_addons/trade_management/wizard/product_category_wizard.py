from odoo import models, fields


class ProductCategoryWizard(models.TransientModel):
    _name = 'product.category.wizard'
    _description = 'Mass Change Product Category'

    # selected products to be updated
    product_ids = fields.Many2many(
        'product.template',
        string='Products'
    )

    # new category to assign to selected products
    categ_id = fields.Many2one(
        'product.category',
        string='New Category',
        required=True
    )

    def action_apply(self):
        # apply selected category to all chosen products
        self.product_ids.write({
            'categ_id': self.categ_id.id
        })