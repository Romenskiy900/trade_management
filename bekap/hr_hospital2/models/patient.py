
from odoo import models, fields

class HospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Пацієнт'

    _inherit = ['hospital.medic.info']

    name = fields.Char(string='ПІБ', required=True)

    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Персональний лікар'
    )

    history_ids = fields.One2many(
        'hr.hospital.doctor.history',
        'patient_id',
        string='Історія лікарів'
    )


    insurance_number = fields.Char(
        string='Номер страхового поліса',
        size=20
    )

    doctor_change_date = fields.Date(string="Дата зміни лікаря")