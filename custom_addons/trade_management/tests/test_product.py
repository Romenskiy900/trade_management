from odoo.tests.common import TransactionCase


class TestTradeProduct(TransactionCase):

    def test_create_product_retail(self):
        # create product with retail sale type
        product = self.env['product.template'].create({
            'name': 'Retail Product',
            'sale_type': 'retail',
        })

        # ensure sale_type is correctly assigned
        self.assertEqual(product.sale_type, 'retail')

    def test_create_product_wholesale(self):
        # create product with wholesale sale type
        product = self.env['product.template'].create({
            'name': 'Wholesale Product',
            'sale_type': 'wholesale',
        })

        # ensure sale_type is correctly assigned
        self.assertEqual(product.sale_type, 'wholesale')

    def test_create_product_without_sale_type(self):
        # create product without specifying sale_type
        product = self.env['product.template'].create({
            'name': 'Simple Product',
        })

        # default value should be empty/False
        self.assertFalse(product.sale_type)