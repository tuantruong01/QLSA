from odoo import models, fields, _, api

from odoo.exceptions import ValidationError


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

    @api.onchange('menu_id', 'registration_id.meal_type', 'registration_id.date')
    def onchange_employee_meal_register_ids(self):
        for r in self:
            if r.registration_id.meal_type == 'set' and r.registration_id.date:
                menu_week_ids = self.env['tigo.menu.setting'].search([('day_start', '<=', r.registration_id.date),
                                                                      ('day_end', '>=', r.registration_id.date),
                                                                      ('type_menu', '=', r.registration_id.meal_type),
                                                                      ('state', '=', 'active')])
                menu_day_id = self.env['tigo.menu.setting'].search([('state', '=', 'active'),
                                                                    ('type_menu', '=', r.registration_id.meal_type),
                                                                    ('day', '=', r.registration_id.date)])
                if not menu_week_ids and not menu_day_id:
                    menu = []
                    return {'domain': {'menu_id': [('id', 'in', menu)]}}
                else:
                    menu = menu_week_ids + menu_day_id
                    if menu:
                        return {'domain': {'menu_id': [('id', 'in', menu.menu_ids.ids)]}}
            else:
                menu = []
                return {'domain': {'menu_id': [('id', 'in', menu)]}}

    @api.constrains('employee_id')
    def check_employee_id(self):
        for r in self:
            data = self.env['confirm.dish'].search(
                [('date_register', '=', r.registration_id.date), ('employee_id', '=', r.employee_id.name)])
            if len(data) > 0:
                raise ValidationError(_('Nhân Viên đã đăng ký!'))

    @api.onchange('employee_id')
    def onchange_emplyee_id(self):
        for r in self:
            list_employee = []
            for i in r.registration_id.employee_meal_register_ids:
                list_employee.append(i.employee_id.id)
            return {'domain': {'employee_id': [('id', 'not in', tuple(list_employee))]}}


class Client(models.Model):
    _name = 'tigo.register.client'
    _description = 'Đăng ký Khách Hàng'

    registration_id = fields.Many2one('tigo.mealregister', string=_('Đăng ký suất ăn'))
    menu_id = fields.Many2one('tigo.menu', string=_('Thực đơn'))
    partner_id = fields.Many2one('res.partner', string=_('Tên khách hàng'))
    phone_client = fields.Char(string=_('Số điện thoại'), related='partner_id.phone')
    company = fields.Char(string=_('Tên công ty'), related='partner_id.company_id.name')
    position = fields.Char(string=_('Chức danh'), related='partner_id.function')
    note = fields.Char(string="Ghi chú")
    person = fields.Boolean(string=_('Người đại diện'))

    @api.onchange('menu_id', 'registration_id.meal_type', 'registration_id.date')
    def onchange_menu_id(self):
        for r in self:
            if r.registration_id.meal_type == 'set' and r.registration_id.date:
                menu_week_ids = self.env['tigo.menu.setting'].search([('day_start', '<=', r.registration_id.date),
                                                                      ('day_end', '>=', r.registration_id.date),
                                                                      ('type_menu', '=', r.registration_id.meal_type),
                                                                      ('state', '=', 'active')])
                menu_day_id = self.env['tigo.menu.setting'].search([('state', '=', 'active'),
                                                                    ('type_menu', '=', r.registration_id.meal_type),
                                                                    ('day', '=', r.registration_id.date)])
                if not menu_week_ids and not menu_day_id:
                    menu = []
                    return {'domain': {'menu_id': [('id', 'in', menu)]}}
                else:
                    menu = menu_week_ids + menu_day_id
                    if menu:
                        return {'domain': {'menu_id': [('id', 'in', menu.menu_ids.ids)]}}
            else:
                menu = []
                return {'domain': {'menu_id': [('id', 'in', menu)]}}