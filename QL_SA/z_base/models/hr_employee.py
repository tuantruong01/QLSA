from odoo import models, fields


class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    code_employee = fields.Char('Mã nhân viên')

    _sql_constraints = [('code_employee', 'unique(code_employee)', "Mã nhân viên đã tồn tại")]
