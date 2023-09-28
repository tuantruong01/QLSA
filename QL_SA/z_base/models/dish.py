from odoo import api, models, fields, _


class Dish(models.Model):
    _name = 'tigo.dish'
    _description = 'Dish'

    name = fields.Char(string=_('Tên món ăn'), required=True)
    ingredient_ids = fields.Many2many('product.template', 'dish_product_ref', 'dish_id', 'ptml_id',
                                      string=_('Nguyên liệu'))
    code_dish = fields.Char(string=_('Mã Món'), readonly=1)
    price_total = fields.Float(string=_('Giá'))
    wage = fields.Float(string=_('Chi Phí Khác'))
    type_service = fields.Selection([('service', 'Dịch vụ ngoài'), ('internal', 'Nội bộ')], string='Kiểu', required=True)
    type_food = fields.Selection([('eat', 'Đồ ăn'), ('drink', 'Đồ uống')], default='eat', string='Dạng thực phẩm')
    type_room = fields.Selection([('sing', 'Phòng Hát'), ('eat', 'Phòng Ăn'), ('all', 'Tất Cả')],
                                 string=_('Món Phòng Hát/Ăn'))
    img = fields.Binary(string='Hình ảnh')

    @api.model
    def create(self, vals_list):
        res = super(Dish, self).create(vals_list)
        res['code_dish'] = self.env['ir.sequence'].next_by_code('tigo.dish')
        return res

    @api.onchange('ingredient_ids')
    def onchange_ingredient_ids(self):
        for r in self:
            r.price_total = sum(r.ingredient_ids.mapped('list_price'), r.wage)

    @api.onchange('wage')
    def onchange_wage(self):
        for r in self:
            r.price_total = sum(r.ingredient_ids.mapped('list_price'), r.wage)
