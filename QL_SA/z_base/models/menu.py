from odoo import models, fields, _, api


class Menu(models.Model):
    _name = 'tigo.menu'
    _description = 'Menu'

    id = fields.Integer(string=_('Mã thực đơn'), readonly=1)
    name = fields.Char(string=_('Tên thực đơn'), requied=True)
    dish_ids = fields.Many2many('tigo.dish', 'menu_dish_ref', 'menu_id', 'dish_id', string=_('Món ăn'))
    type_menu = fields.Selection([('draft', 'Suất ăn'), ('table', 'Bàn')], string=_('Kiểu thực đơn'), default="draft")
    sate = fields.Selection([('draft', 'Chưa Kích Hoạt'), ('use', 'Kích hoạt')], string=_('Trạng Thái'), default="draft")

class SettingMenu(models.Model):
    _name = 'tigo.menu.setting'
    _description = 'Cấu Hình'

    id = fields.Integer(string=_('Mã thực đơn'), readonly=1)
    sate = fields.Selection([('draft', 'Chưa kích hoạt'), ('use', 'Đã kích hoạt')], string=_('Trạng Thái'), default="draft")
    menu_ids = fields.Many2many('tigo.menu', 'setting_menu_ref', 'setting_id', 'menu_id', string=_('Thực Đơn'))
    day_start = fields.Datetime(string="Từ ngày", requied=True)
    day_end = fields.Datetime(string="Đến ngày", requied=True)