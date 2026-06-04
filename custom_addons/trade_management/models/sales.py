from odoo import models, fields, api
from odoo.exceptions import UserError


class TradeSales(models.Model):
    _name = 'trade.management.sales'
    _description = 'Sales registration'
    _inherit = 'trade.document.mixin'

    prefix = 'Чек ККМ'

    line_ids = fields.One2many('trade.management.sales.line', 'sales_id', string='Product')
    state = fields.Selection([('draft', 'Draft'), ('posted', 'Posted')], default='draft')
    stock_picking_id = fields.Many2one('stock.picking', readonly=True)

    def action_post(self):
        picking_type_out = self.env.ref('stock.picking_type_out')
        warehouse_location = picking_type_out.default_location_src_id
        customer_location = self.env.ref('stock.stock_location_customers')

        for rec in self:
            # Skip already processed documents
            if rec.state == 'posted' or rec.stock_picking_id:
                continue

            if not rec.line_ids:
                raise UserError("No lines in sales!")

            # Check available stock before posting
            self.env['stock.quant'].flush_model()
            for line in rec.line_ids:
                variant = line.product_id.product_variant_id or line.product_id

                self.env.cr.execute("""
                    SELECT COALESCE(SUM(quantity - reserved_quantity), 0)
                    FROM stock_quant
                    WHERE product_id = %s AND location_id = %s
                """, (variant.id, warehouse_location.id))
                product_qty = self.env.cr.fetchone()[0]

                if line.quantity > product_qty:
                    raise UserError(
                        f"Недостатньо товара '{variant.name}'. Требуется: {line.quantity}, Доступно: {product_qty}")

            # Create outgoing stock picking
            picking = self.env['stock.picking'].create({
                'picking_type_id': picking_type_out.id,
                'location_id': warehouse_location.id,
                'location_dest_id': customer_location.id,
                'origin': f"{rec.prefix} {rec.id}",
            })

            # Create stock moves for sales lines
            moves_vals = []
            for line in rec.line_ids:
                variant = line.product_id.product_variant_id or line.product_id
                uom_id = variant.uom_id.id if variant.uom_id else self.env.ref('uom.product_uom_unit').id

                moves_vals.append({
                    'product_id': variant.id,
                    'product_uom_qty': line.quantity,
                    'product_uom': uom_id,
                    'picking_id': picking.id,
                    'location_id': warehouse_location.id,
                    'location_dest_id': customer_location.id,
                })

            moves = self.env['stock.move'].create(moves_vals)

            # Confirm and assign stock moves
            picking.action_confirm()
            picking.action_assign()

            # Set done quantities before validation
            for move in moves:
                move.quantity = move.product_uom_qty
                move.picked = True

            # Validate picking without backorders
            picking.with_context(skip_backorder=True).button_validate()

            rec.stock_picking_id = picking.id
            rec.state = 'posted'

        self.env['stock.quant'].flush_model()

    def write(self, vals):
        for rec in self:
            if rec.state == 'posted':
                raise UserError("Cannot edit posted sales document!")
        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.state == 'posted':
                raise UserError("Cannot delete posted sales document!")
        return super().unlink()