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
        search_price_date = fields.Date.context_today(self)

        """ selected records """
        active_price_sets = self.env['trade.management.price.set'].search([
            ('date', '<=', search_price_date)
        ], order='date desc, id desc')

        if active_price_sets:
            """ last price """
        price_line = self.env['trade.management.price.set.line'].search([
            ('product_id', '=', self.product_id.id),
            ('price_set_id', 'in', active_price_sets.ids)
        ], limit=1)

        if price_line:
            self.price = price_line.price
        return

        # Fallback if no price setting document is found

        self.price = self.product_id.list_price


    @api.depends('quantity', 'price')
    def _compute_sum(self):
        """ Automatically calculate the total sum for the line """

        for rec in self:
            rec.sum = rec.quantity * rec.price

