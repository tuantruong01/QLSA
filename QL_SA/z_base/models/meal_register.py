from datetime import datetime

from odoo import models, fields, _, api
from odoo.exceptions import UserError


class MealRegister(models.Model):
    _name = 'tigo.mealregister'
    _description = 'Đăng ký bữa ăn'

    name = fields.Integer(string=_('Mã suất ăn'))
    register = fields.Many2one('res.users',
                               string=_('Người đăng ký'),
                               default=lambda self: self.env.user,
                               readonly=1)
    number = fields.Selection([('four', '4'), ('six', '6')], string=_('Số người đăng ký'))
    meal_type = fields.Selection([('draft', 'suất'), ('table', 'bàn')],
                                 string=_('Hình thức ăn'), default='draft')
    date = fields.Date(string=_('Ngày đăng ký'))
    menu = fields.Many2one('tigo.dish', string=_('Thực đơn'))
    employee_mealregister_ids = fields.One2many('tigo.detailed.registration', 'registration_id',
                                                string="Đăng ký cho nhân viên")
    client_mealregister_ids = fields.One2many('tigo.detailed.registration', 'registration_id',
                                              string="Đăng ký cho khách hàng")

    _sql_constraints = [('name', 'unique(name)', "Mã đăng ký đã tồn tại")]

    # @api.onchange('date')
    # def onchange_menu(self):
    #     for r in self:
    #         if r.date:
    #             # date = datetime.strptime(r.date, '%Y-%m-%d')
    #             menu = self.env['tigo.menu'].search([('date', '=', '2023-07-14')]).mapped('dish_ids').ids
    #             return {
    #                 'domain': {
    #                     'menu': [('id', '=', menu)]
    #                 }
    #             }
    #

class Detail(models.Model):
    _name = 'tigo.detailed.registration'
    _description = 'Đăng ký chi tiết'

    registration_id = fields.Many2one('tigo.mealregister', string=_('Đăng ký suất ăn'))
    code = fields.Many2one('hr.employee', string='Mã nhân viên')
    employee_id = fields.Char(string="Nhân viên", related='code.name')
    number_phone = fields.Char(string=_('Số điện thoại'), related='code.mobile_phone')
    menu = fields.Many2one('tigo.dish', string=_('Thực đơn'))
    name_client = fields.Char(string=_('Tên khách hàng'))
    phone_client = fields.Integer(string=_('Số điện thoại'))
    menu_client = fields.Many2one('tigo.menu', string=_('Thực đơn'))
