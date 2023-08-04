from odoo import models, fields, _, api


class Menu(models.Model):
    _name = 'tigo.menu'
    _description = 'Menu'

    code = fields.Integer(string=_('Mã thực đơn'))
    name = fields.Char(string=_('Tên thực đơn'), requied=True)
    dish_ids = fields.Many2many('tigo.dish', 'menu_dish_ref', 'menu_id', 'dish_id', string=_('Món ăn'))
    type_menu = fields.Selection([('draft', 'suất ăn'), ('table', 'Bàn')], string=_('Kiểu thực đơn'))
    date = fields.Date(string=_('Ngày áp dụng'))

    _sql_constraints = [('code', 'unique(code)', "Mã thực đơn đã tồn tại")]