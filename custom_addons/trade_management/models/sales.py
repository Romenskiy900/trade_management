from odoo import models, fields, api
from odoo.exceptions import UserError


class TradeSales(models.Model):
    _name = 'trade.management.sales'
    _description = 'Sales registration'
    _inherit = 'trade.document.mixin'

    # document prefix used for generated name (from mixin)
    prefix = 'Чек ККМ'

    # sales lines (products + quantities)
    line_ids = fields.One2many(
        'trade.management.sales.line',
        'sales_id',
        string='Product'
    )

    # document state: draft or posted
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted')
    ], default='draft')

    # linked stock picking created after posting
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

            # collect product variant IDs for stock check
            product_ids = rec.line_ids.mapped('product_id.product_variant_id').ids

            # check available stock via SQL aggregation
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

            # validate stock availability before creating moves
            for line in rec.line_ids:
                variant_id = line.product_id.product_variant_id.id
                available = stock_map.get(variant_id, 0)

                if not self.env.context.get('install_demo'):
                    if line.quantity > available:
                        raise UserError(
                            f"Not enough stock for {line.product_id.display_name}. "
                            f"Available: {available}, needed: {line.quantity}"
                        )

            # create outgoing picking (sale delivery)
            picking = self.env['stock.picking'].create({
                'partner_id': False,
                'picking_type_id': picking_type.id,
                'location_id': warehouse_location.id,
                'location_dest_id': customer_location.id,
                'origin': rec.prefix,
            })

            # create stock moves for each sale line
            for line in rec.line_ids:
                self.env['stock.move'].create({
                    'product_id': line.product_id.product_variant_id.id,
                    'product_uom_qty': line.quantity,
                    'quantity': line.quantity,
                    'picking_id': picking.id,
                    'location_id': warehouse_location.id,
                    'location_dest_id': customer_location.id,
                    'description_picking': line.product_id.name,
                })

            # confirm and reserve stock
            picking.action_confirm()
            picking.action_assign()

            # force move quantities for validation
            for move in picking.move_ids:
                move.quantity = move.product_uom_qty
                if move.move_line_ids:
                    move.move_line_ids.quantity = move.product_uom_qty

            picking.button_validate()

            rec.stock_picking_id = picking.id
            rec.state = 'posted'

    def write(self, vals):
        for rec in self:
            if rec.state == 'posted':
                raise UserError("Cannot edit posted receipt!")
        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.state == 'posted':
                raise UserError("Cannot delete posted sales document!")
        return super().unlink()