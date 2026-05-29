from dateutil.utils import today

from odoo import models, fields

class HospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Пацієнт'

    _inherit = ['hospital.medic.info']

    name = fields.Char(string='ПІБ', required=True)

    phone = fields.Char(string='Телефон')

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

    def action_open_patient_visits(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Історія візитів',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_create_quick_visit(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Новий візит',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.doctor_id.id,
                'default_visit_datetime': today(),
                'default_planned_datetime': today(),
            }
        }