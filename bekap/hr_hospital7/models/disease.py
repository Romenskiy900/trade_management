from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease Type'
    _parent_name = 'parent_id'
    _parent_store = True

    name = fields.Char(required=True, string='Хвороба')

    parent_id = fields.Many2one(
        'hr.hospital.disease',
        string='Розділ хвороби',
        ondelete='restrict'
    )

    parent_path = fields.Char(index=True)

    child_ids = fields.One2many(
        'hr.hospital.disease',
        'parent_id',
        string='Підпорядковані хвороби'
    )

    display_name = fields.Char(compute='_compute_display_name', store=True)

    @api.depends('name', 'parent_id')
    def _compute_display_name(self):
        for rec in self:
            names = []
            current = rec
            visited = set()
            while current and current.id and current.id not in visited:
                visited.add(current.id)
                names.append(current.name)
                current = current.parent_id
            rec.display_name = " / ".join(reversed(names))

    @api.constrains('parent_id')
    def _check_no_cycle(self):
        for rec in self:
            parent = rec.parent_id
            visited = set()
            while parent:
                if parent.id == rec.id:
                    raise ValidationError("Не можливо встановити в батьківський елемент самого себе")
                if parent.id in visited:
                    raise ValidationError("Не можливо встановити в батьківський елемент самого себе")
                visited.add(parent.id)
                parent = parent.parent_id