from odoo import models, fields


class ReceiptReportWizard(models.TransientModel):
    _name = 'trade.management.receipt.report.wizard'
    _description = 'Receipt Report Wizard'

    date_from = fields.Datetime(string="Date From", required=True)
    date_to = fields.Datetime(string="Date To", required=True)

    def action_print_report(self):
        return self.env.ref(
            'trade_management.action_receipt_report'
        ).report_action(
            self,
            data={
                'date_from': self.date_from,
                'date_to': self.date_to,
            }
        )