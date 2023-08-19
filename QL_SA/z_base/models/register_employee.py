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


class Client(models.Model):
    _name = 'tigo.register.client'
    _description = 'Đăng ký Khách Hàng'

    registration_id = fields.Many2one('tigo.mealregister', string=_('Đăng ký suất ăn'))
    menu = fields.Many2many('tigo.dish', 'menu_client_ref', 'register_client_id', 'dish_client_id',
                            string=_('Thực đơn'))
    name_client = fields.Char(string=_('Tên khách hàng'))
    phone_client = fields.Integer(string=_('Số điện thoại'))
    note = fields.Char(string="Ghi chú")
