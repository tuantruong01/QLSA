from odoo import models, fields, _, api


class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    code_employee = fields.Char(string=_('Mã nhân viên'), readonly=1)

    _sql_constraints = [('code_employee', 'unique(code_employee)', 'Không Được Đặt Trùng Mã Nhân Viên')]

    @api.model
    def create(self, vals_list):
        res = super(HrEmployeeInherit, self).create(vals_list)
        res['code_employee'] = self.env['ir.sequence'].next_by_code('hr.employee')
        return res

    def write(self, vals):
        result = super(HrEmployeeInherit, self).write(vals)
        if self.code_employee:
            return result
        else:
            self.code_employee = self.env['ir.sequence'].next_by_code('hr.employee')
            return result
