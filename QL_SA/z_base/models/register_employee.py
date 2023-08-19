from odoo import models, fields, _, api


class RegisterEmployee(models.Model):
    _name = 'tigo.detailed.registration'
    _description = 'Đăng ký Nhân Viên'

    registration_id = fields.Many2one('tigo.mealregister', string=_('Đăng ký suất ăn'))
    code_id = fields.Many2one('hr.employee', string='Mã nhân viên')
    employee = fields.Char(string="Nhân viên", related='code_id.name')
    number_phone = fields.Char(string=_('Số điện thoại'), related='code_id.mobile_phone')
    menu = fields.Many2many('tigo.dish', 'menu_ref', 'register_id', 'dish_register_id', string=_('Thực đơn'))
    dpm_id = fields.Many2one('hr.department', string="Phòng Ban", related='code_id.department_id')