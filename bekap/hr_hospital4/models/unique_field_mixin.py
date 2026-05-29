from odoo import models
from odoo.exceptions import ValidationError

class UniqueFieldMixin(models.AbstractModel):
    _name = 'unique.field.mixin'
    _description = 'Unique Field Mixin'

    def _check_unique_field_mixin(self, vals, field_name):

        if field_name not in vals:
            return vals

        value = vals[field_name]

        domain = [(field_name, '=', value)]

        if self.ids:
            domain.append(('id', 'not in', self.ids))

        existing = self.search(domain, limit=1)

        if existing:
            raise ValidationError(
                f"Запис з таким значенням '{value}' вже існує!"
            )

        return vals