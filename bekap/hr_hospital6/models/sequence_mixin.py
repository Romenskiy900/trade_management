from odoo import models

class SequenceMixin(models.AbstractModel):
    _name = 'sequence.mixin'
    _description = 'Sequence Mixin'

    def _check_and_set_sequence(self, vals, field_name):

        if vals.get(field_name):
            return vals

        last = self.search(
            [(field_name, "!=", False)],
            order=f"{field_name} desc",
            limit=1
        )

        last_value = last[field_name] or 0

        if isinstance(last_value, int):
            vals[field_name] = last_value + 1
        else:
            vals[field_name] = 1

        return vals