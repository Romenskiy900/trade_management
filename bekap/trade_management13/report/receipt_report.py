from odoo import models, api
from collections import defaultdict


class ReceiptReport(models.AbstractModel):
    _name = 'report.trade_management.receipt_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        data = data or {}

        date_from = data.get('date_from')
        date_to = data.get('date_to')

        domain = []

        if date_from:
            domain.append(('date', '>=', date_from))
        if date_to:
            domain.append(('date', '<=', date_to))

        receipts = self.env['trade.management.receipt'].search(domain)

        grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        for r in receipts:
            date_key = r.date.date()
            partner = r.pertner_id.name or 'Undefined'

            for line in r.line_ids:
                product = line.product_id.name or 'Undefined'
                grouped[date_key][partner][product] += line.quantity

        return {
            'docs': receipts,
            'grouped': dict(grouped),
            'date_from': date_from,
            'date_to': date_to,
        }