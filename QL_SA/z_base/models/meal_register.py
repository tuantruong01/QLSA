from odoo import models, fields, _, api


class MealRegister(models.Model):
    _name = 'tigo.mealregister'
    _description = 'Đăng ký bữa ăn'

    name = fields.Char(string=_('Mã suất ăn'), readonly=1)
    register = fields.Many2one('res.users',
                               string=_('Người đăng ký'),
                               default=lambda self: self.env.user,
                               readonly=1)
    number = fields.Selection([('four', '4'), ('six', '6')], string=_('Số người đăng ký'), default="four")
    meal_type = fields.Selection([('draft', 'suất'), ('table', 'bàn')],
                                 string=_('Hình thức ăn'), default='draft')
    date = fields.Date(string=_('Ngày đăng ký'))
    menu_ids = fields.Many2many('tigo.dish', 'menu_table_ref', 'table_menu', 'dish_table_id', string=_('Thực đơn'))
    employee_mealregister_ids = fields.One2many('tigo.detailed.registration', 'registration_id',
                                                string="Đăng ký cho nhân viên")
    client_mealregister_ids = fields.One2many('tigo.register.client', 'registration_id',
                                              string="Đăng ký cho khách hàng")

    @api.onchange('menu_ids')
    def onchange_menu(self):
        for r in self:
            r.employee_mealregister_ids.menu = r.menu_ids
            r.client_mealregister_ids.menu = r.menu_ids

    @api.model
    def create(self, vals_list):
        res = super(MealRegister, self).create(vals_list)
        res['name'] = self.env['ir.sequence'].next_by_code('tigo.mealregister')
        return res


class Detail(models.Model):
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
