from odoo.tests.common import TransactionCase


class TestTradeProduct(TransactionCase):

    # 1. Проверка создания продукта с retail
    def test_create_product_retail(self):
        product = self.env['product.template'].create({
            'name': 'Retail Product',
            'sale_type': 'retail',
        })

        self.assertEqual(product.sale_type, 'retail')

    # 2. Проверка создания продукта с wholesale
    def test_create_product_wholesale(self):
        product = self.env['product.template'].create({
            'name': 'Wholesale Product',
            'sale_type': 'wholesale',
        })

        self.assertEqual(product.sale_type, 'wholesale')

    # 3. Проверка значения по умолчанию
    def test_create_product_without_sale_type(self):
        product = self.env['product.template'].create({
            'name': 'Simple Product',
        })

        self.assertFalse(product.sale_type)