
from odoo import models, fields

class HospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Пацієнт'

    name = fields.Char(string='ПІБ', required=True)
    birthday = fields.Date(string='Дата народження')
