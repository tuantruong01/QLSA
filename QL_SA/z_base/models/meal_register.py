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
    meal_type = fields.Selection([('draft', 'Suất'), ('table', 'Bàn')],
                                 string=_('Hình thức ăn'), default='draft')
    date = fields.Date(string=_('Ngày đăng ký'), required=True)
    menu_ids = fields.Many2many('tigo.dish', 'menu_table_ref', 'table_menu', 'dish_table_id', string=_('Thực đơn'))
    employee_meal_register_ids = fields.One2many('tigo.detailed.registration', 'registration_id',
                                                 string="Đăng ký cho nhân viên")
    client_meal_register_ids = fields.One2many('tigo.register.client', 'registration_id',
                                               string="Đăng ký cho khách hàng")
    state = fields.Selection([('draft', 'Chờ'),
                              ('done', 'Đã đăng ký'),
                              ('cancel', 'Hủy')], default='draft')

    @api.onchange('menu_ids')
    def onchange_menu(self):
        for r in self:
            r.employee_meal_register_ids.menu = r.menu_ids

    @api.model
    def create(self, vals_list):
        res = super(MealRegister, self).create(vals_list)
        res['name'] = self.env['ir.sequence'].next_by_code('tigo.mealregister')
        return res

    def action_register(self):
        for r in self:
            r.state = 'done'
            for line in r.employee_meal_register_ids:
                self.env['confirm.dish'].create({
                    'employee_id': line.employee_id.id,
                    'department': line.employee_id.department_id.id if line.employee_id.department_id.id else False,
                    'date_register': r.date
                })

            for line in r.client_meal_register_ids:
                self.env['confirm.dish'].create({
                    'partner_id': line.partner_id.id,
                    'date_register': r.date
                })

    def action_cancel(self):
        for r in self:
            r.state = 'cancel'


