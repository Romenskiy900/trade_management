from odoo.tests.common import TransactionCase


class TestResPartnerExtension(TransactionCase):

    def test_partner_create(self):
        # create new partner record
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })

        # ensure partner exists and name is correct
        self.assertTrue(partner)
        self.assertEqual(partner.name, 'Test Partner')

    def test_partner_email(self):
        # create partner with email
        partner = self.env['res.partner'].create({
            'name': 'Email Test',
            'email': 'test@mail.com',
        })

        # verify email stored correctly
        self.assertEqual(partner.email, 'test@mail.com')

    def test_partner_write(self):
        # create partner record
        partner = self.env['res.partner'].create({
            'name': 'Old Name',
        })

        # update partner name
        partner.write({
            'name': 'New Name',
        })

        # verify update applied
        self.assertEqual(partner.name, 'New Name')