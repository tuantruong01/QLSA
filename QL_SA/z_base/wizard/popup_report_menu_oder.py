from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PopupReportMenuOder(models.TransientModel):
    _name = 'popup.report.menu.oder'
    _description = 'Báo Cáo Suất Ăn Đã Đặt'

    begin = fields.Date(string="Từ Ngày", required=True)
    end = fields.Date(string="Đến Ngày", required=True)

    @api.onchange('begin', 'end')
    def onchange_begin_end(self):
        for r in self:
            if r.begin and r.end:
                if r.end < r.begin:
                    raise ValidationError('Ngày bắt kết thúc phải lớn hơn hoặc bằng ngày bắt đầu')

    def action_print(self):
        return self.env.ref('z_base.report_menu_order').report_action(self)
