from odoo import models, fields, _, api

from odoo.exceptions import ValidationError


class OrderDish(models.Model):
    _name = 'tigo.dish.order'
    _description = 'Đặt Món'

    order_dish_id = fields.Many2one('tigo.service', string=_('Đặt Món Ăn'))
    dish_id = fields.Many2one('tigo.dish', string=_('Tên Món'))
    number = fields.Integer(string=_('Số lượng'))
    price = fields.Float(string=_('Thành Tiền'))
    price_unit = fields.Float(string=_('Đơn Giá'))
    note = fields.Text(string='Ghi Chú')
