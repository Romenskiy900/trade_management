from odoo import models, fields, api
from odoo.exceptions import UserError


class TradeSales(models.Model):
    _name = 'trade.management.sales'
    _description = 'Регістрація продажів'
    _inherit = 'trade.document.mixin'

    prefix = 'Чек ККМ'

    line_ids = fields.One2many(
        'trade.management.sales.line',
        'sales_id',
        string='Product'
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted')
    ], default='draft')

    stock_picking_id = fields.Many2one(
        'stock.picking',
        readonly=True
    )

    def action_post(self):
        for rec in self:

            if rec.state == 'posted':
                raise UserError("Already posted!")

            if not rec.line_ids:
                raise UserError("No lines in sales!")

            warehouse_location = self.env.ref('stock.stock_location_stock')
            customer_location = self.env.ref('stock.stock_location_customers')
            picking_type = self.env.ref('stock.picking_type_out')


            product_ids = rec.line_ids.mapped('product_id').ids

            # =========================================================
            # ⚡ 1 SQL QUERY - CHECK STOCK (stock.quant)
            # =========================================================
            self.env.cr.execute("""
                   SELECT
                       sq.product_id,
                       SUM(sq.quantity - sq.reserved_quantity) AS available_qty
                   FROM stock_quant sq
                   WHERE sq.location_id = %s
                     AND sq.product_id = ANY(%s)
                   GROUP BY sq.product_id
               """, (
                warehouse_location.id,
                product_ids
            ))


            stock_map = dict(self.env.cr.fetchall())

            # =========================================================
            # CHECK STOCK
            # =========================================================
            for line in rec.line_ids:
                available = stock_map.get(line.product_id.id, 0)

                if line.quantity > available:
                    raise UserError(
                        f"Not enough stock for {line.product_id.display_name}. "
                        f"Available: {available}, needed: {line.quantity}"
                    )


            # -------------------------
            # CREATE OUT PICKING
            # -------------------------
            picking = self.env['stock.picking'].create({
                'partner_id': False,
                'picking_type_id': picking_type.id,
                'location_id': warehouse_location.id,
                'location_dest_id': customer_location.id,
                'origin': rec.prefix,
            })

            # -------------------------
            # CREATE MOVES
            # -------------------------
            for line in rec.line_ids:
                self.env['stock.move'].create({
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'picking_id': picking.id,
                    'location_id': warehouse_location.id,
                    'location_dest_id': customer_location.id,
                })

            # -------------------------
            # RESERVE + VALIDATE
            # -------------------------
            picking.action_confirm()
            picking.action_assign()

            # если есть остатки → спишет
            picking.button_validate()

            rec.stock_picking_id = picking.id
            rec.state = 'posted'

    def write(self, vals):
        for rec in self:
            if rec.state == 'posted':
                raise UserError("Cannot edit posted receipt!")
        return super().write(vals)