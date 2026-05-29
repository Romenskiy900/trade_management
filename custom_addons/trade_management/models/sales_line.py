# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Tradesalesline(models.Model):
    _name = 'trade.management.sales.line'
    _description = 'Sales order line'

    # reference to parent sales document
    sales_id = fields.Many2one(
        'trade.management.sales',
        string='Products',
        ondelete='cascade'
    )

    # product sold in this line
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True
    )

    # quantity of product (default = 1 for immediate calculation)
    quantity = fields.Integer(
        string='Quantity',
        default=1,
        required=True
    )

    # unit price taken from price list (readonly, calculated via onchange)
    price = fields.Float(
        string='Price',
        digits='Product Price',
        readonly=True
    )

    # total line amount = quantity * price (stored for reporting/search)
    sum = fields.Float(
        string='Sum',
        compute='_compute_sum',
        store=True,
        digits='Product Price'
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """
        Load product price based on latest valid price set before current datetime
        """

        if self.product_id:
            search_price_date = fields.Datetime.now()

            # fetch latest price from price set lines
            self.env.cr.execute("""
                SELECT psl.price
                FROM trade_management_price_set_line psl
                JOIN trade_management_price_set ps
                    ON ps.id = psl.price_set_id
                WHERE psl.product_id = %s
                  AND ps.date <= %s
                ORDER BY ps.date DESC, psl.id DESC
                LIMIT 1
            """, (
                self.product_id.id,
                search_price_date,
            ))

            row = self.env.cr.fetchone()

            # fallback to 0 if no price found
            self.price = row[0] if row else 0

    @api.depends('quantity', 'price')
    def _compute_sum(self):
        """
        Compute line total amount (quantity * price)
        """

        for rec in self:
            rec.sum = rec.quantity * rec.price