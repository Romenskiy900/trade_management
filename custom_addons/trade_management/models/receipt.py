from odoo import models, fields, api
from odoo.exceptions import UserError


class TradeReceipt(models.Model):
    _name = 'trade.management.receipt'
    _description = 'Reliability of goods'
    _inherit = 'trade.document.mixin'

    # prefix used in document name generation (from mixin)
    prefix = 'Reliability of goods'

    # partner (supplier/customer) related to this receipt
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True
    )

    # document date/time (used for accounting and reporting)
    date = fields.Datetime(default=fields.Datetime.now)

    # receipt lines containing products and quantities
    line_ids = fields.One2many(
        'trade.management.receipt.line',
        'receipt_id',
        string='Product'
    )

    # document state (draft → posted)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted')
    ], default='draft')

    # created stock picking linked to this receipt after posting
    stock_picking_id = fields.Many2one(
        'stock.picking',
        string='Stock Picking',
        readonly=True
    )

    # -------------------------
    # POST DOCUMENT
    # -------------------------
    def action_post(self):
        for rec in self:

            if rec.state == 'posted':
                raise UserError("Document already posted!")

            if not rec.line_ids:
                raise UserError("No lines in receipt!")

            supplier_location = self.env.ref('stock.stock_location_suppliers')
            stock_location = self.env.ref('stock.stock_location_stock')

            picking_type = self.env.ref('stock.picking_type_in')

            # create stock picking for incoming goods movement
            picking = self.env['stock.picking'].create({
                'partner_id': rec.partner_id.id,
                'picking_type_id': picking_type.id,
                'location_id': supplier_location.id,
                'location_dest_id': stock_location.id,
                'origin': rec.prefix,
            })

            # create stock moves for each receipt line
            for line in rec.line_ids:
                self.env['stock.move'].create({
                    'product_id': line.product_id.product_variant_id.id,
                    'product_uom_qty': line.quantity,
                    'quantity': line.quantity,
                    'picking_id': picking.id,
                    'location_id': supplier_location.id,
                    'location_dest_id': stock_location.id,
                    'description_picking': line.product_id.name,
                })

            # confirm and process stock picking
            picking.action_confirm()
            picking.action_assign()
            picking.button_validate()

            rec.stock_picking_id = picking.id
            rec.state = 'posted'

    # -------------------------
    # PROTECT POSTED DOCUMENTS
    # -------------------------
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