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

    @api.onchange('menu_id')
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
                menu_ids = menu_week_ids + menu_day_id
                if menu_ids:
                    list_menu_ids = []
                    for data in menu_ids:
                        for line in data.menu_ids:
                            list_menu_ids.append(line.id)
                    return {'domain': {'menu_id': [('id', 'in', tuple(list_menu_ids))]}}


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
