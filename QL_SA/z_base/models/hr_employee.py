from odoo import models, fields


class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    code_employee = fields.Char('Mã nhân viên')

