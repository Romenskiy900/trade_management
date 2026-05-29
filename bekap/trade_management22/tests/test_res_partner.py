from odoo.tests.common import TransactionCase


class TestResPartnerExtension(TransactionCase):

    # 1. Проверка, что партнер создается
    def test_partner_create(self):
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })

        self.assertTrue(partner)
        self.assertEqual(partner.name, 'Test Partner')

    # 2. Проверка записи email (базовое поле res.partner)
    def test_partner_email(self):
        partner = self.env['res.partner'].create({
            'name': 'Email Test',
            'email': 'test@mail.com',
        })

        self.assertEqual(partner.email, 'test@mail.com')

    # 3. Проверка изменения записи (write)
    def test_partner_write(self):
        partner = self.env['res.partner'].create({
            'name': 'Old Name',
        })

        partner.write({
            'name': 'New Name',
        })

        self.assertEqual(partner.name, 'New Name')