from odoo import models, fields, api


class Tradesalesline(models.Model):
    _name = 'trade.management.sales.line'
    _description = 'poison of price setting'

    sales_id = fields.Many2one('trade.management.sales', string='Products', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Integer(string='Quantity', default=1, required=True)


    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.ref('base.UAH').id
    )
    price = fields.Monetary(string='Price', currency_field='currency_id', readonly=True)
    sum = fields.Monetary(string='Sum', compute='_compute_sum', store=True, currency_field='currency_id')

    # Load the latest valid price for the selected product
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:

            price_set = self.env['trade.management.price.set'].search([
                ('date', '<=', fields.Datetime.now()),
                ('line_ids.product_id', '=', self.product_id.id)
            ], order='date desc', limit=1)

            if price_set:
                price_line = price_set.line_ids.filtered(lambda line: line.product_id == self.product_id)
                self.price = price_line[-1].price if price_line else 0
            else:
                self.price = 0

    # Calculate line total.
    @api.depends('quantity', 'price')
    def _compute_sum(self):
        for rec in self:
            rec.sum = rec.quantity * rec.price