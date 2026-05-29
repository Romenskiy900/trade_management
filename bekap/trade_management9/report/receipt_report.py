from odoo import models


class ReceiptReport(models.AbstractModel):
    _name = 'report.trade_management.receipt_report_template'
    _description = 'Receipt Report'

    def _get_report_values(self, docids, data=None):

        docs = self.env['trade.management.receipt'].search(
            [],
            order='create_date, pertner_id'
        )

        return {
            'docs': docs,
        }