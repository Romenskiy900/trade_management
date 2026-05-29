from odoo import models, api
from collections import defaultdict


class ReceiptReport(models.AbstractModel):
    _name = 'report.trade_management.receipt_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        Prepare data for receipt report template.
        Groups receipts by date → partner → product.
        """

        data = data or {}

        # report filter range start date
        date_from = data.get('date_from')

        # report filter range end date
        date_to = data.get('date_to')

        # search domain for filtering receipts
        domain = []

        if date_from:
            domain.append(('date', '>=', date_from))
        if date_to:
            domain.append(('date', '<=', date_to))

        # fetch receipts matching filters
        receipts = self.env['trade.management.receipt'].search(domain)

        # nested structure: date → partner → product → quantity
        grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        for r in receipts:
            # normalize date to day level (remove time part)
            date_key = r.date.date()

            # partner name fallback if missing
            partner = r.partner_id.name or 'Undefined'

            for line in r.line_ids:
                # product name fallback if missing
                product = line.product_id.name or 'Undefined'

                # accumulate quantities per product per partner per day
                grouped[date_key][partner][product] += line.quantity

        return {
            'docs': receipts,
            'grouped': dict(grouped),
            'date_from': date_from,
            'date_to': date_to,
        }