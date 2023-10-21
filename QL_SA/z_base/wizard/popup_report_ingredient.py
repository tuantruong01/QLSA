from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PopupReportIngredient(models.TransientModel):
    _name = 'popup.report.ingredient'
    _description = 'Báo Cáo Nguyên Liệu'

    categ_id = fields.Many2one('product.category', string='Nhóm Thực Phẩm', required=True)

    def action_print(self):
        return self.env.ref('z_base.report_menu_order').report_action(self)