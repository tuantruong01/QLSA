from odoo import api, fields, models, _


class ConfirmDish(models.Model):
    _name = 'confirm.dish'
    _description = 'Xác nhận đã nhận suất ăn'

    name = fields.Char(string=_('Tên phiếu ăn', readonly=1))
    employee_id = fields.Char(string=_('Họ và tên'), required=True)
    date_register = fields.Date(string=_('Ngày đăng ký'))
    department = fields.Many2one('hr.department', string="Phòng ban")
    ate = fields.Boolean(string=_('Đã ăn'), default=False)
    mealregister_id = fields.Many2one('tigo.mealregister', string=_('Đăng ký suất ăn'))

    @api.model
    def create(self, vals_list):
        res = super(ConfirmDish, self).create(vals_list)
        res['name'] = self.env['ir.sequence'].next_by_code('confirm.dish')
        return res