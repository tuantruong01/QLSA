from odoo import api, fields, models


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    detailed_type = fields.Selection(selection_add=[('food', 'Thực phẩm')], ondelete={'food': 'set default'})