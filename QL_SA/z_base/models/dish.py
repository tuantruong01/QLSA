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
    type = fields.Selection([('sing', 'Dịch vụ'), ('eat', 'Đồ ăn')], default='eat', string='Loại')

    @api.onchange('ingredient_ids', 'wage')
    def onchange_ingredient_ids(self):
        for r in self:
            r.price_total = sum(r.ingredient_ids.mapped('list_price'), r.wage)

    _sql_constraints = [('dish_id', 'unique(dish_id)', "Mã món ăn đã tồn tại")]

    # @api.onechange('wage')
    # def onchange_wage(self):
    #     for r in self:
    #         r.price_total = sum(r.ingredient_ids.mapped('list_price'), r.wage)
