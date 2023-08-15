from odoo import api, models, fields, _


class Dish(models.Model):
    _name = 'tigo.dish'
    _description = 'Dish'

    name = fields.Char(string=_('Tên món ăn'), requied=True)
    ingredient_ids = fields.Many2many('product.template', 'dish_product_ref', 'dish_id', 'ptml_id',
                                      string=_('Nguyên liệu'))
    id = fields.Integer(string=_('Mã Món'), readonly=1)
    price_total = fields.Float(string=_('Thành tiền'), readonly=1)
    wage = fields.Float(string=_('Tiền công'))
    type_service = fields.Selection([('service', 'Dịch vụ ngoài'), ('internal', 'Nội bộ')], default='internal',
                                    string='Kiểu ')
    type_food = fields.Selection([('eat', 'Đồ ăn'), ('drink', 'Đồ uống')], default='eat', string='Dạng thực phẩm')

    @api.onchange('ingredient_ids')
    def onchange_ingredient_ids(self):
        for r in self:
            r.price_total = sum(r.ingredient_ids.mapped('list_price'), r.wage)

    @api.onchange('wage')
    def onchange_wage(self):
        for r in self:
            r.price_total = sum(r.ingredient_ids.mapped('list_price'), r.wage)
