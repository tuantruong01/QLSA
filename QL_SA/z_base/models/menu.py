from odoo import models, fields, _, api
from datetime import timedelta

from odoo.exceptions import UserError


class Menu(models.Model):
    _name = 'tigo.menu'
    _description = 'Menu'

    code_menu = fields.Char(string=_('Mã thực đơn'), readonly=1)
    name = fields.Char(string=_('Tên thực đơn'), requied=True)
    dish_ids = fields.Many2many('tigo.dish', 'menu_dish_ref', 'menu_id', 'dish_id', string=_('Món ăn'))
    type_menu = fields.Selection([('set', 'Suất ăn'), ('table', 'Bàn')], string=_('Kiểu thực đơn'), default="set")

    @api.model
    def create(self, vals_list):
        res = super(Menu, self).create(vals_list)
        res['code_menu'] = self.env['ir.sequence'].next_by_code('tigo.menu')
        return res


class SettingMenu(models.Model):
    _name = 'tigo.menu.setting'
    _description = 'Cấu Hình'

    name = fields.Char(string=_('Mã Cấu Hình'), readonly=1)
    state = fields.Selection([('unactive', 'Chưa kích hoạt'), ('active', 'Đã kích hoạt')], string=_('Trạng Thái'),
                             default="unactive")
    menu_ids = fields.Many2many('tigo.menu', 'setting_menu_ref', 'setting_id', 'menu_id', string=_('Thực Đơn'))
    day_start = fields.Date(string="Từ ngày")
    day_end = fields.Date(string="Đến ngày", readonly=True)
    type = fields.Selection([('day', 'Ngày'), ('week', 'Tuần')], string="Theo ngày/tuần")
    type_menu = fields.Selection([('set', 'Suất'), ('table', 'Bàn')], string=_('Kiểu Thực Đơn'),
                                 default="set")
    day = fields.Date(string="Ngày")

    @api.model
    def create(self, vals_list):
        res = super(SettingMenu, self).create(vals_list)
        res['name'] = self.env['ir.sequence'].next_by_code('tigo.menu.setting')
        return res

    def action_active(self):
        for r in self:
            r.state = "active"

    def action_unactive(self):
        for r in self:
            r.state = "unactive"

    @api.onchange('day_start')
    def onchange_day_start(self):
        for r in self:
            if r.day_start:
                if r.day_start.weekday() != 0:
                    raise UserError(_('Bạn phải chọn ngày đầu tuần.'))
                else:
                    r.day_end = r.day_start + timedelta(days=6)

    @api.onchange('menu_ids')
    def onchange_type_menu(self):
        for r in self:
            if r.type_menu == 'set':
                menu_ids = self.env['tigo.menu'].search([('type_menu', '=', r.type_menu)]).ids
                return {'domain': {'menu_ids': [('id', 'in', menu_ids)]}}
            else:
                menu_ids = self.env['tigo.menu'].search([('type_menu', '=', r.type_menu)]).ids
                return {'domain': {'menu_ids': [('id', 'in', menu_ids)]}}
