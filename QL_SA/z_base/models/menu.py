from odoo import models, fields, _, api


class Menu(models.Model):
    _name = 'tigo.menu'
    _description = 'Menu'

    id = fields.Integer(string=_('Mã thực đơn'), readonly=1)
    name = fields.Char(string=_('Tên thực đơn'), requied=True)
    dish_ids = fields.Many2many('tigo.dish', 'menu_dish_ref', 'menu_id', 'dish_id', string=_('Món ăn'))
    type_menu = fields.Selection([('draft', 'Suất ăn'), ('table', 'Bàn')], string=_('Kiểu thực đơn'), default="draft")
    sate = fields.Selection([('draft', 'Chưa Kích Hoạt'), ('table', 'Kích hoạt')], string=_('Trạng Thái'), default="draft")

