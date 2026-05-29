from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Лікар'


    name = fields.Char(string='ПІБ', required=True)

    category_id = fields.Many2one(
        'hr.hospital.doctor.category',
        string='Категорія'
    )

    user_id = fields.Many2one(
        'res.users',
        string='Користувач системи'
    )

    mentor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Ментор',
        domain=[('is_intern', '=', False)]
    )

    is_intern = fields.Boolean(
        string='Інтерн',
        compute='_compute_is_intern',
        store=True
    )

    intern_ids = fields.One2many(
        'hr.hospital.doctor',
        'mentor_id',
        string='Інтерни'
    )

    visit_ids = fields.One2many(
        'hr.hospital.visit',
        'doctor_id',
        string='Історія візитів'
    )

    patient_ids = fields.Many2many(
        'hr.hospital.patient',
        compute='_compute_patient_ids',
        string='Пацієнти лікаря'
    )

    @api.depends('visit_ids.patient_id')
    def _compute_patient_ids(self):
        for rec in self:
            rec.patient_ids = rec.visit_ids.mapped('patient_id')

    @api.depends('mentor_id')
    def _compute_is_intern(self):
        for rec in self:
            rec.is_intern = bool(rec.mentor_id)

    @api.constrains('mentor_id')
    def _check_mentor(self):
        for rec in self:
            if rec.mentor_id:
                if rec.mentor_id.is_intern:
                    raise ValidationError('Ментор не може бути інтерном')
                else:
                    interns = self.search([
                        ('mentor_id', '=', rec.id),
                        ('is_intern', '=', True)
                    ], limit=1)

                    if interns:
                        raise ValidationError(
                            'Цей лікар вже є ментором, тому не може бути інтерном'
                        )

    def action_create_visit(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Новий візит',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_doctor_id': self.id
            }
        }