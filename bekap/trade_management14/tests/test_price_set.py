from odoo.tests.common import TransactionCase


class TestTradePriceSet(TransactionCase):

    def setUp(self):
        super().setUp()


        self.product = self.env['product.template'].create({
            'name': 'Test Product',
        })


        self.price_set = self.env['trade.management.price.set'].create({
            'date': '2026-01-01',
        })


    def test_create_price_set_line_with_price(self):
        line = self.env['trade.management.price.set.line'].create({
            'price_set_id': self.price_set.id,
            'product_id': self.product.id,
            'price': 150.50,
        })


        self.assertTrue(line)
        self.assertEqual(line.price, 150.50)
        self.assertEqual(line.product_id, self.product)
        self.assertEqual(line.price_set_id, self.price_set)