from odoo import models, fields, _, api


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
    day_start = fields.Date(string="Từ ngày", requied=True)
    day_end = fields.Date(string="Đến ngày", requied=True)
    color = fields.Integer(string='Color Index')
    _sql_constraints = [('uniq_color', 'unique(color)', 'The color index must be unique.')]

    @api.model
    def create(self, vals_list):
        res = super(SettingMenu, self).create(vals_list)
        res['name'] = self.env['ir.sequence'].next_by_code('tigo.menu.setting')
        return res

    def action_active(self):
        for r in self:
            r.state = "active"
            r.color = 0

    def action_unactive(self):
        for r in self:
            r.state = "unactive"
            r.color = 5
