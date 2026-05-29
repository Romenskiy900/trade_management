from odoo import models, fields, api
from datetime import date

class HospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Візити пацієнтів'
    _order = 'planned_datetime desc'

    name = fields.Char(
        string='Назва',
        compute='_compute_name',
        store=True
    )

    status = fields.Selection(
        selection=[
            ('planned', 'Заплановано'),
            ('done', 'Завершено'),
            ('cancelled', 'Скасовано'),
        ],
        string='Статус візиту',
        default='planned'
    )

    planned_datetime = fields.Datetime(
        string='Запланована дата та час візиту',
        required=True
    )

    visit_datetime = fields.Datetime(
        string='Дата та час візиту'
    )

    visit_count = fields.Integer(
        string="Кількість",
        default=1
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

    summary = fields.Html(
        string='Епікриз / Summary'
    )

    disease_id = fields.Many2one(
        'hr.hospital.disease',
        string='Діагноз'
    )

    is_locked = fields.Boolean(
        compute='_compute_is_locked',
        store=False
    )

    @api.depends('visit_datetime')
    def _compute_is_locked(self):
        for rec in self:
            if not rec.id:
                rec.is_locked = False
                continue

            if rec.visit_datetime:
                visit_date = fields.Date.to_date(rec.visit_datetime)
                today = fields.Date.context_today(rec)

                rec.is_locked = visit_date <= today
            else:
                rec.is_locked = False

    @api.depends('patient_id', 'doctor_id', 'visit_datetime')
    def _compute_name(self):
        for rec in self:
            patient = rec.patient_id.name or ''
            doctor = rec.doctor_id.name or ''
            visit_datetime = rec.visit_datetime or ''

            rec.name = f"{patient} - {doctor} - {visit_datetime}"


