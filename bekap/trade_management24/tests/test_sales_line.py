from odoo.tests.common import TransactionCase


class TestTradeSalesLine(TransactionCase):

    def setUp(self):
        super().setUp()

        # product used for sales line tests
        self.product = self.env['product.template'].create({
            'name': 'Test Product',
        })

    def test_default_quantity(self):
        # create sales line without specifying quantity
        line = self.env['trade.management.sales.line'].create({
            'product_id': self.product.id,
        })

        # default quantity must be 1
        self.assertEqual(line.quantity, 1)

    def test_compute_sum(self):
        # create sales line with price and quantity
        line = self.env['trade.management.sales.line'].create({
            'product_id': self.product.id,
            'quantity': 2,
            'price': 100,
        })

        # verify computed total amount
        self.assertEqual(line.sum, 200)

    def test_product_assignment(self):
        # create sales line and check product relation
        line = self.env['trade.management.sales.line'].create({
            'product_id': self.product.id,
        })

        # ensure correct product is linked
        self.assertEqual(line.product_id, self.product)