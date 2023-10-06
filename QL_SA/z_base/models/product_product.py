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
            product_template_id = self.env['product.template'].search([('name', '=', r.name)])
            if len(product_template_id) > 1:
                raise ValidationError(_('Sản phẩm đã tồn tại!'))
