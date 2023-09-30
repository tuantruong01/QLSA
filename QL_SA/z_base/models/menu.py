from odoo import models, fields, _, api
from datetime import timedelta

from odoo.exceptions import ValidationError


class Menu(models.Model):
    _name = 'tigo.menu'
    _description = 'Menu'

    code_menu = fields.Char(string=_('Mã thực đơn'), readonly=1)
    name = fields.Char(string=_('Tên thực đơn'), required=True)
    dish_ids = fields.Many2many('tigo.dish', 'menu_dish_ref', 'menu_id', 'dish_id', string=_('Món ăn'), required=True)
    type_menu = fields.Selection([('set', 'Suất ăn'), ('table', 'Bàn')], string=_('Kiểu thực đơn'), required=True)
    number_of_people = fields.Selection([('four', '4'), ('six', '6')], string=_('Số người/ Bàn'))
    image = fields.Binary(string='Hình Thực Đơn')

    @api.model
    def create(self, vals_list):
        res = super(Menu, self).create(vals_list)
        res['code_menu'] = self.env['ir.sequence'].next_by_code('tigo.menu')
        return res

    def unlink(self):
        detailed_registration_ids = self.env['tigo.detailed.registration'].search([('menu_id', '=', self.id)])
        if len(detailed_registration_ids) > 0:
            raise ValidationError(_('Sản phẩm này đã được đăng ký trong suất ăn!'))
        return super(Menu, self).unlink()


class SettingMenu(models.Model):
    _name = 'tigo.menu.setting'
    _description = 'Cấu Hình'

    name = fields.Char(string=_('Mã Cấu Hình'), readonly=1)
    state = fields.Selection([('unactive', 'Chưa kích hoạt'), ('active', 'Đã kích hoạt')], string=_('Trạng Thái'),
                             default="unactive")
    menu_ids = fields.Many2many('tigo.menu', 'setting_menu_ref', 'setting_id', 'menu_id', string=_('Thực Đơn'))
    day_start = fields.Date(string="Từ ngày", readonly=True)
    day_end = fields.Date(string="Đến ngày", readonly=True)
    type = fields.Selection([('day', 'Ngày'), ('week', 'Tuần')], string="Theo ngày/tuần")
    type_menu = fields.Selection([('set', 'Suất'), ('table', 'Bàn')], string=_('Kiểu Thực Đơn'))
    day = fields.Date(string="Ngày")
    number_of_people = fields.Selection([('four', '4'), ('six', '6')], string=_('Số người/ Bàn'))
    detail_dish = fields.Char(string=_('Chi tiết món'), readonly=True)
    week = fields.Many2one('tigo.week', string='Tuần')

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

    @api.onchange('week')
    def onchange_day_start(self):
        for r in self:
            r.day_start = r.week.begin
            r.day_end = r.week.end

    @api.onchange('menu_ids', 'type_menu', 'number_of_people')
    def onchange_type_menu(self):
        for r in self:
            if r.type_menu == 'set':
                menu_ids = self.env['tigo.menu'].search([('type_menu', '=', r.type_menu)]).ids
                return {'domain': {'menu_ids': [('id', 'in', menu_ids)]}}
            else:
                if r.number_of_people == 'four':
                    menu_ids = self.env['tigo.menu'].search(
                        [('type_menu', '=', 'table'), ('number_of_people', '=', 'four')]).ids
                    return {'domain': {'menu_ids': [('id', 'in', menu_ids)]}}
                else:
                    menu_ids = self.env['tigo.menu'].search(
                        [('type_menu', '=', 'table'), ('number_of_people', '=', 'six')]).ids
                    return {'domain': {'menu_ids': [('id', 'in', menu_ids)]}}

    @api.onchange('menu_ids')
    def _onchange_menu_id(self):
        for r in self:
            datas = ''
            for line in r.menu_ids:
                datas += line.name + ":" + ', '.join([line.name for line in r.dish_ids]) + '; '
            r.detail_dish = datas
