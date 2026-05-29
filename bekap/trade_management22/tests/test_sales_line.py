from odoo.tests.common import TransactionCase


class TestTradeSalesLine(TransactionCase):

    def setUp(self):
        super().setUp()

        self.product = self.env['product.template'].create({
            'name': 'Test Product',
        })

    # 1. Проверка quantity по умолчанию
    def test_default_quantity(self):
        line = self.env['trade.management.sales.line'].create({
            'product_id': self.product.id,
        })

        self.assertEqual(line.quantity, 1)

    # 2. Проверка вычисления суммы
    def test_compute_sum(self):
        line = self.env['trade.management.sales.line'].create({
            'product_id': self.product.id,
            'quantity': 2,
            'price': 100,
        })

        self.assertEqual(line.sum, 200)

    # 3. Проверка product_id
    def test_product_assignment(self):
        line = self.env['trade.management.sales.line'].create({
            'product_id': self.product.id,
        })

        self.assertEqual(line.product_id, self.product)