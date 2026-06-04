from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class TradeReceipt(models.Model):
    _name = 'trade.management.receipt'
    _description = 'Reliability of goods'
    _inherit = 'trade.document.mixin'

    prefix = 'Reliability of goods'

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    date = fields.Datetime(default=fields.Datetime.now)
    line_ids = fields.One2many('trade.management.receipt.line', 'receipt_id', string='Product')
    state = fields.Selection([('draft', 'Draft'), ('posted', 'Posted')], default='draft')
    stock_picking_id = fields.Many2one('stock.picking', string='Stock Picking', readonly=True)

    def action_post(self):
        for rec in self:
            if rec.state == 'posted':
                raise UserError("Document already posted!")
            if not rec.line_ids:
                raise UserError("No lines in receipt!")

            picking_type = self.env.ref('stock.picking_type_in')

            # Create incoming stock picking
            picking = self.env['stock.picking'].create({
                'partner_id': rec.partner_id.id,
                'picking_type_id': picking_type.id,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': picking_type.default_location_dest_id.id,
                'origin': rec.prefix,
            })

            # Create stock moves for receipt lines
            for line in rec.line_ids:
                variant = line.product_id
                uom_id = variant.uom_id.id

                self.env['stock.move'].create({
                    'product_id': variant.id,
                    'product_uom_qty': line.quantity,
                    'product_uom': uom_id,
                    'picking_id': picking.id,
                    'location_id': picking.location_id.id,
                    'location_dest_id': picking.location_dest_id.id,
                    'description_picking': variant.name,
                })

            # Confirm and assign stock moves
            picking.action_confirm()
            picking.action_assign()

            # Set done quantities before validation
            for move in picking.move_ids:
                move.quantity = move.product_uom_qty
                if move.move_line_ids:
                    for move_line in move.move_line_ids:
                        move_line.quantity = move.product_uom_qty

            # Validate picking and process related wizards if needed
            res = picking.with_context(
                button_validate_picking_ids=[picking.id],
                skip_backorder=True,
                picking_label_ids=False
            ).button_validate()

            rec.stock_picking_id = picking.id
            rec.state = 'posted'

            # Refresh stock-related caches
            self.env['stock.quant'].flush_model()
            self.env['stock.move'].flush_model()
            self.env['stock.move.line'].flush_model()
            self.env['stock.quant'].invalidate_model()

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