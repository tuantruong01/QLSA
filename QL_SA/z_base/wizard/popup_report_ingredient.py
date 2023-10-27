from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PopupReportIngredient(models.TransientModel):
    _name = 'popup.report.ingredient'
    _description = 'Báo Cáo Nguyên Liệu'

    categ_ids = fields.Many2many('product.category', 'product_category_ref', 'ingredient_id', 'category_id',
                                 string='Nhóm Thực Phẩm', required=True)
    all = fields.Boolean(string='Tất Cả')

    def action_print(self):
        return self.env.ref('z_base.report_menu_order').report_action(self)

    @api.onchange('all')
    def onchange_all(self):
        for r in self:
            if r.all == True:
                r.categ_ids = self.env['product.category'].search([])


