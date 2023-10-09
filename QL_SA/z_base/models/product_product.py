from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    product_type = fields.Selection([
        ('consu', 'Tiêu dùng'),
        ('service', 'Dịch vụ'),
        ('product', 'Sản phẩm lưu kho'),
        ('food', 'Thực phẩm')], string='Loại sản phẩm', default='consu', required=True)

    @api.constrains('name')
    def constrains_name(self):
        for r in self:
            if len(r.name) > 50:
                raise ValidationError(_('Tên nguyên liệu không được nhỏ hơn 50 ký tự'))
            data = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '{', '}', '[', ']', ]
            for i in data:
                if i in r.name:
                    raise ValidationError(_('Tên nguyên liệu không được chứa ký tự đặc biệt'))
            product_template_id = self.env['product.template'].search([('name', '=', r.name)])
            if len(product_template_id) > 1:
                raise ValidationError(_('Nguyên liệu đã tồn tại!'))

    @api.onchange('product_type')
    def constrains_product_type(self):
        for r in self:
            if r.product_type in ['consu', 'service', 'product', 'food']:
                r.purchase_ok = False
                r.sale_ok = False


