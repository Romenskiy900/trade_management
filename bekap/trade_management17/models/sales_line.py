# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Tradesalesline(models.Model):
    _name = 'trade.management.sales.line'
    _description = 'Рядок товарів'

    sales_id = fields.Many2one(
        'trade.management.sales',
        string='Products',
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        'product.template',
        string='Product',
        required=True
    )

    # Set default quantity to 1 so the sum can compute immediately
    quantity = fields.Integer(string='Quantity',
                              default=1,
                              required=True)

    price = fields.Float(string='Price',
                         digits='Product Price',
                         readonly=True)

    # Sum must be a computed field to automatically calculate Price * Quantity
    sum = fields.Float(
        string='Sum',
        compute='_compute_sum',
        store=True,
        digits='Product Price'
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):

        """ Setting price """

        if self.product_id:
            """ Let's find the price selection date """
            # search_price_date = fields.Date.context_today(self)
            search_price_date = fields.Datetime.now()

            """ selected records """

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

            self.price = row[0] if row else 0




    @api.depends('quantity', 'price')
    def _compute_sum(self):
        """ Automatically calculate the total sum for the line """

        for rec in self:
            rec.sum = rec.quantity * rec.price

