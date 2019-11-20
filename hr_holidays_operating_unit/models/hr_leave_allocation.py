# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class HolidaysAllocation(models.Model):
    _inherit = "hr.leave.allocation"

    operating_unit_id = fields.Many2one(
        'operating.unit',
        'Operating Unit',
        default=lambda self: (
            self.env['res.users'].operating_unit_default_get()
            )
    )

    @api.onchange("employee_id", "holiday_type")
    def _onchange_operating_unit_id(self):
        if self.holiday_type == "employee" \
                and self.employee_id.default_operating_unit_id:
            self.operating_unit_id = self.employee_id.default_operating_unit_id
        else:
            self.operating_unit_id = None

    @api.multi
    @api.constrains('operating_unit_id')
    def _constrain_operating_unit_id(self):
        for rec in self:
            if rec.operating_unit_id and rec.employee_id \
                    and rec.operating_unit_id \
                    not in rec.employee_id.operating_unit_ids:
                message = _('{} is an invalid Operating Unit for the employee {}').format(
                    rec.operating_unit_id.name, rec.employee_id.name)
                raise ValidationError(message)

