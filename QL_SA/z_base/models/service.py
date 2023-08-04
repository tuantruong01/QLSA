from odoo import models, fields, _, api
from odoo.exceptions import UserError
from datetime import datetime


class MealRegister(models.Model):
    _name = 'tigo.service'
    _description = 'Dịch vụ'

    name_id = fields.Many2one('res.users',
                              string=_('Người đặt'),
                              default=lambda self: self.env.user,
                              readonly=1)
    code = fields.Integer(string=_('Mã Đặt Phòng'), requied=1)
    type = fields.Selection([('sing', 'Hát'), ('eat', 'Ăn uống')], string=_('Kiểu Dịch Vụ'), default="eat")
    sate = fields.Selection([('draft', 'Chờ'),
                             ('pay1', 'Đã Thanh Toán Tiền Cọc'),
                             ('pay2', 'Đã Thanh Toán'),
                             ('cancel', 'Hủy')])
    room_id = fields.Many2one('tigo.room', string=_('Phòng'))
    dish_ids = fields.Many2many('tigo.dish', 'service_ref', 'service_id', 'dish_s_id', string=_('Món'), default="")
    start_day = fields.Datetime(string=_("Ngày bắt đầu"))
    end_day = fields.Datetime(string=_('Ngày kết thúc'))
    deposit = fields.Float(string="Tiền cọc 20% hóa đơn")
    total = fields.Float(string='Tổng Thanh Toán')
    price = fields.Float(string='Thành tiền')
    note = fields.Char(string='Ghi Chú')
    time_use = fields.Float(string='Tổng giờ hát', compute='_compute_timeup')

    _sql_constraints = [('code', 'unique(code)', "Mã đặt phòng đã tồn tại")]

    @api.depends('start_day', 'end_day')
    def _compute_timeup(self):
        for r in self:
            if r.start_day and r.end_day:
                if r.type == 'sing':
                    time_up = r.end_day - r.start_day
                    r.time_use = time_up.total_seconds() / 3600
                else:
                    r.time_use = 0
            else:
                r.time_use = 0

    @api.onchange('dish_ids')
    def onchange_ingredient_ids(self):
        for r in self:
                r.price = sum(r.dish_ids.mapped('price_total'), (r.time_use * 40000))
                r.deposit = (r.price * 0.2)
                r.total = r.price - r.deposit
