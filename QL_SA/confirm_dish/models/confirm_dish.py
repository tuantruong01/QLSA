from odoo import api, fields, models, _


class ConfirmDish(models.Model):
    _name = 'confirm.dish'
    _description = 'Xác nhận đã nhận suất ăn'

    name = fields.Char(string=_('Tên phiếu ăn', readonly=1))
    employee_id = fields.Many2one('res.users', string=_('Tên nhân viên'))
    partner_id = fields.Many2one('res.partner', string=_('Tên Khách'))
    date_register = fields.Date(string=_('Ngày đăng ký'))
    department = fields.Many2one('hr.department', string="Phòng ban")
    ate = fields.Boolean(string=_('Đã ăn'), default=False)

