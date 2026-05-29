from odoo import models, fields


class HospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Прийом пацієнта'

    name = fields.Integer(string='Номер прийому', required=True)

    visit_date = fields.Datetime(
        string='Дата і час прийому',
        default=fields.Datetime.now,
        required=True
    )

    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Лікар',
        required=True
    )

    patient_id = fields.Many2one(
        'hr.hospital.patient',
        string='Пацієнт',
        required=True
    )

    disease_id = fields.Many2one(
        'hr.hospital.disease',
        string='Діагноз'
    )

    treatment_notes = fields.Text(
        string='Рекомендації лікаря'
    )