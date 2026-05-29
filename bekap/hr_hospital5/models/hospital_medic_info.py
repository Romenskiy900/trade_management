from odoo import models, fields, api
# from datetime import date

class HospitalMedicInfo(models.AbstractModel):
    _name = 'hospital.medic.info'
    _description = 'Medical Information'

    blood_group = fields.Selection(
        selection=[
            ('o_pos', 'O(I) Rh+'),
            ('o_neg', 'O(I) Rh-'),
            ('a_pos', 'A(II) Rh+'),
            ('a_neg', 'A(II) Rh-'),
            ('b_pos', 'B(III) Rh+'),
            ('b_neg', 'B(III) Rh-'),
            ('ab_pos', 'AB(IV) Rh+'),
            ('ab_neg', 'AB(IV) Rh-'),
        ],
        string='Група крові'
    )

    gender = fields.Selection(
        selection=[
            ('male', 'Чоловік'),
            ('female', 'Жінка'),
        ],
        string='Стать'
    )

    birth_date = fields.Date(string='Дата народження')


    age = fields.Integer(string='Вік')

    @api.onchange('birth_date')
    def _onchange_birth_date(self):
        for rec in self:
            if rec.birth_date:
                today = fields.Date.context_today(rec)
                birth = fields.Date.to_date(rec.birth_date)
                change_year = -1
                if today.month > birth.month or (today.month == birth.month and today.day >= birth.day):
                    change_year = 0
                rec.age = today.year - birth.year + change_year

            else:
                rec.age = 0