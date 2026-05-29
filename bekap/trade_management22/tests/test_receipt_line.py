from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestTradeReceiptLine(TransactionCase):

    def setUp(self):
        super().setUp()

        self.product = self.env['product.template'].create({
            'name': 'Test Product',
            'list_price': 100,
        })

    # 1. Успешное создание строки
    def test_create_receipt_line_success(self):
        line = self.env['trade.management.receipt.line'].create({
            'product_id': self.product.id,
            'quantity': 5,
        })

        self.assertEqual(line.quantity, 5)
        self.assertEqual(line.product_id, self.product)

    # 2. Ошибка если quantity = 0
    def test_quantity_zero_validation(self):
        with self.assertRaises(ValidationError):
            self.env['trade.management.receipt.line'].create({
                'product_id': self.product.id,
                'quantity': 0,
            })

    # 3. Ошибка если quantity < 0
    def test_quantity_negative_validation(self):
        with self.assertRaises(ValidationError):
            self.env['trade.management.receipt.line'].create({
                'product_id': self.product.id,
                'quantity': -10,
            })