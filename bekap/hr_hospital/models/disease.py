from odoo import models, fields

class HospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease Type'

    name = fields.Char(
        string='Назва хвороби',
        required=True,
        help="Введіть назву хвороби"
    )
