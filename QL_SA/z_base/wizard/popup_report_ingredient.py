from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PopupReportIngredient(models.TransientModel):
    _name = 'popup.report.ingredient'
    _description = 'Báo Cáo Nguyên Liệu'

    categ_id = fields.Many2one('product.category', string='Nhóm Thực Phẩm', required=True)
    product_type = fields.Selection([
        ('consu', 'Tiêu dùng'),
        ('service', 'Dịch vụ'),
        ('product', 'Sản phẩm lưu kho'),
        ('food', 'Thực phẩm')], string='Loại sản phẩm', default='consu', required=True)