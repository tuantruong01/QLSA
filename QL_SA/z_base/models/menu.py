from odoo import models, fields, _, api


class Menu(models.Model):
    _name = 'tigo.menu'
    _description = 'Menu'

    id = fields.Integer(string=_('Mã thực đơn'), readonly=1)
    name = fields.Char(string=_('Tên thực đơn'), requied=True)
    dish_ids = fields.Many2many('tigo.dish', 'menu_dish_ref', 'menu_id', 'dish_id', string=_('Món ăn'))
    type_menu = fields.Selection([('draft', 'Suất ăn'), ('table', 'Bàn')], string=_('Kiểu thực đơn'), default="draft")
    state = fields.Selection([('unactive', 'Chưa Kích Hoạt'), ('active', 'Kích hoạt')], string=_('Trạng Thái'),
                            default="unactive")


class SettingMenu(models.Model):
    _name = 'tigo.menu.setting'
    _description = 'Cấu Hình'

    id = fields.Integer(string=_('Mã thực đơn'), readonly=1)
    state = fields.Selection([('unactive', 'Chưa kích hoạt'), ('active', 'Đã kích hoạt')], string=_('Trạng Thái'),
                            default="unactive")
    menu_ids = fields.Many2many('tigo.menu', 'setting_menu_ref', 'setting_id', 'menu_id', string=_('Thực Đơn'))
    day_start = fields.Date(string="Từ ngày", requied=True)
    day_end = fields.Date(string="Đến ngày", requied=True)

    def action_active(self):
        for r in self:
            r.state = "active"

    def action_unactive(self):
        for r in self:
            r.state = "unactive"
