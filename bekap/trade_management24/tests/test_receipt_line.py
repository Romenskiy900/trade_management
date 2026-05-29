from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestTradeReceiptLine(TransactionCase):

    def setUp(self):
        super().setUp()

        # product used for receipt line tests
        self.product = self.env['product.template'].create({
            'name': 'Test Product',
            'list_price': 100,
        })

    def test_create_receipt_line_success(self):
        # create valid receipt line
        line = self.env['trade.management.receipt.line'].create({
            'product_id': self.product.id,
            'quantity': 5,
        })

        # ensure correct values stored
        self.assertEqual(line.quantity, 5)
        self.assertEqual(line.product_id, self.product)

    def test_quantity_zero_validation(self):
        # quantity = 0 should trigger validation error
        with self.assertRaises(ValidationError):
            self.env['trade.management.receipt.line'].create({
                'product_id': self.product.id,
                'quantity': 0,
            })

    def test_quantity_negative_validation(self):
        # negative quantity should trigger validation error
        with self.assertRaises(ValidationError):
            self.env['trade.management.receipt.line'].create({
                'product_id': self.product.id,
                'quantity': -10,
            })