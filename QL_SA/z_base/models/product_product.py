from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    detailed_type = fields.Selection(selection_add=[('food', 'Thực phẩm')], ondelete={'food': 'set default'})

    @api.constrains('name')
    def constrains_name(self):
        for r in self:
            product_template_id = self.env['product.template'].search([('name', '=', r.name)])
            if len(product_template_id) > 0:
                raise ValidationError(_('Sản phẩm đã tồn tại!'))
