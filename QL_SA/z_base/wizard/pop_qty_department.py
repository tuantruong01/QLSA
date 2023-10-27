from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PopupQtyDepartment(models.TransientModel):
    _name = 'popup.report.qty.department'
    _description = 'Số lượng suất ăn đã đăng ký theo phòng ban'

    begin = fields.Date(string="Từ Ngày", required=True)
    end = fields.Date(string="Đến Ngày", required=True)

    @api.onchange('begin', 'end')
    def onchange_begin_end(self):
        for r in self:
            if r.begin and r.end:
                if r.end < r.begin:
                    raise ValidationError('Ngày bắt kết thúc phải lớn hơn hoặc bằng ngày bắt đầu')

    def action_print(self):
        return self.env.ref('z_base.report_qty_department').report_action(self)
