from odoo import models, fields, api

class HospitalDoctorHistory(models.Model):
    _name = 'hr.hospital.doctor.history'
    _description = 'Історія персональних лікарів'
    _order = 'date_start desc'
    _inherit = ['sequence.mixin']

    name = fields.Char(
        string='Назва',
        compute='_compute_name',
        store=True
    )
    patient_id = fields.Many2one(
        'hr.hospital.patient',
        string='Пацієнт',
        required=True
    )

    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Лікар',
        required=True
    )

    date_start = fields.Date(
        string='Дата призначення',
        default=fields.Date.today
    )

    date_end = fields.Date(
        string='Дата зміни лікаря',
        default = fields.Date.today
    )

    active = fields.Boolean(
        string='Активний',
        default=True
    )

    @api.onchange('date_start', 'date_end')
    def _onchange_dates(self):
        if self.date_start and self.date_end:
            if self.date_end < self.date_start:
                self.date_end = self.date_start
                return {
                    'warning': {
                        'title': 'Помилка дати',
                        'message': 'Дата зміни лікаря не може бути раніше ніж дата призначення'
                    }
                }


    @api.depends('patient_id', 'doctor_id', 'doctor_id.category_id', 'date_start')
    def _compute_name(self):
       for rec in self:
            patient = rec.patient_id.name or ''
            doctor = rec.doctor_id.name or ''
            category = rec.doctor_id.category_id.name or ''
            date = rec.date_start or ''

            rec.name = f"{patient} - {doctor} ({category}) {date}"
