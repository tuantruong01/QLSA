from odoo import models, fields, _, api


class RegisterEmployee(models.Model):
    _name = 'tigo.detailed.registration'
    _description = 'Đăng ký Nhân Viên'

    registration_id = fields.Many2one('tigo.mealregister', string=_('Đăng ký suất ăn'))
    employee_id = fields.Many2one('hr.employee', string='Tên Nhân Viên')
    code = fields.Char(string="Mã Nhân Viên", related='employee_id.code_employee')
    number_phone = fields.Char(string=_('Số điện thoại'), related='employee_id.mobile_phone')
    menu_id = fields.Many2one('tigo.menu', string=_('Thực đơn'))
    department_id = fields.Many2one('hr.department', string="Phòng Ban", related='employee_id.department_id')
    note = fields.Char(string=_('Ghi Chú'))
    person = fields.Boolean(string=_('Người đại diện'))


class Client(models.Model):
    _name = 'tigo.register.client'
    _description = 'Đăng ký Khách Hàng'

    registration_id = fields.Many2one('tigo.mealregister', string=_('Đăng ký suất ăn'))
    menu = fields.Many2many('tigo.dish', 'menu_client_ref', 'register_client_id', 'dish_client_id',
                            string=_('Thực đơn'))
    partner_id = fields.Many2one('res.partner', string=_('Tên khách hàng'))
    phone_client = fields.Char(string=_('Số điện thoại'))
    note = fields.Char(string="Ghi chú")
    person = fields.Boolean(string=_('Người đại diện'))

