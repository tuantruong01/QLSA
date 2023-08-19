from odoo import api, fields, models, _


class ConfirmDish(models.Model):
    _name = 'confirm.dish'
    _description = 'Xác nhận đã nhận suất ăn'

    name = fields.Char(string=_('Tên phiếu ăn', readonly=1))
    employee_id = fields.Many2one('res.users', string=_('Tên nhân viên'))
    date_register = fields.Date(string=_('Ngày đăng ký'))
