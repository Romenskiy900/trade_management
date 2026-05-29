from odoo import models, fields, api

class HospitalDoctorCategory(models.Model):
    _name = 'hr.hospital.doctor.category'
    _description = 'Категорії лікарів'
    _order = 'sequence, name'
    _inherit = ['sequence.mixin', 'unique.field.mixin']


    name = fields.Char(string='Категорія', required=True)
    sequence = fields.Integer(
        string='Послідовність',
        readonly=True,
        copy=False
    )

    doctor_ids = fields.One2many(
        'hr.hospital.doctor',
        'category_id',
        string='Лікарі'
    )

    def create(self, vals):
        vals = self._check_and_set_sequence(
            vals,
            'sequence'
        )
        vals = self._check_unique_field_mixin(
            vals,
            'name'
        )
        return super().create(vals)

    def write(self, vals):
        if 'name' in vals:
            for rec in self:
                rec._check_unique_field_mixin(vals, 'name')

        return super().write(vals)

