from odoo.tests.common import TransactionCase


class TestTradePriceSet(TransactionCase):

    def setUp(self):
        super().setUp()

        # test product used for price set line creation
        self.product = self.env['product.template'].create({
            'name': 'Test Product',
        })

        # base price set document for linking lines
        self.price_set = self.env['trade.management.price.set'].create({
            'date': '2026-01-01',
        })

    def test_create_price_set_line_with_price(self):
        # create price set line with product and price
        line = self.env['trade.management.price.set.line'].create({
            'price_set_id': self.price_set.id,
            'product_id': self.product.id,
            'price': 150.50,
        })

        # record must be created successfully
        self.assertTrue(line)

        # check stored price value
        self.assertEqual(line.price, 150.50)

        # check correct product relation
        self.assertEqual(line.product_id, self.product)

        # check correct parent relation
        self.assertEqual(line.price_set_id, self.price_set)