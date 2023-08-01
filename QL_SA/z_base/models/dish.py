from odoo import api, models, fields, _


class Dish(models.Model):
    _name = 'tigo.dish'
    _description = 'Dish'

    name = fields.Char(string=_('Tên món ăn'), requied=True)
    ingredient_ids = fields.Many2many('product.template', 'dish_product_ref', 'dish_id', 'ptml_id',
                                      string=_('Nguyên liệu'))
    dish_id = fields.Char(string=_('Mã Món'), requied=True)
    price_total = fields.Float(string=_('Thành Tiền'), readonly=1)

    @api.onchange('ingredient_ids')
    def onchange_ingredient_ids(self):
        for r in self:
            r.price_total = sum(r.ingredient_ids.mapped('list_price'))

    _sql_constraints = [('dish_id', 'unique(dish_id)', "Mã món ăn đã tồn tại")]
