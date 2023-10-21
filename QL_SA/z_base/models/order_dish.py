from odoo import models, fields, _, api


class OrderDish(models.Model):
    _name = 'tigo.dish.order'
    _description = 'Đặt Món'

    order_dish_id = fields.Many2one('tigo.service', string=_('Đặt Món Ăn'))
    dish_id = fields.Many2one('tigo.dish', string=_('Tên Món'))
    number = fields.Integer(string=_('Số lượng'))
    price = fields.Integer(string=_('Thành Tiền'), readonly=1)
    price_unit = fields.Integer(string=_('Đơn Giá'), readonly=1)
    note = fields.Text(string='Ghi Chú')

    @api.onchange('dish_id', 'number')
    def onchange_dish_id(self):
        for r in self:
            if r.number and r.dish_id:
                r.price_unit = r.dish_id.price_total
                r.price = r.price_unit * r.number

