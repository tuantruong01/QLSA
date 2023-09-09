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
    name = fields.Char(string=_('Mã Đặt Phòng'), readonly=1)
    type = fields.Selection([('sing', 'Hát'), ('eat', 'Ăn uống')], string=_('Kiểu Dịch Vụ'), default="eat")
    state = fields.Selection([('quotes', 'Báo Giá'),
                              ('order', 'Đặt Phòng'),
                              ('pay', 'Thanh Toán'),
                              ('cancel', 'Hủy')], default='quotes')
    room_id = fields.Many2one('tigo.room', string=_('Phòng'))
    dish_ids = fields.Many2many('tigo.dish', 'service_ref', 'service_id', 'dish_s_id', string=_('Món'), default="")
    start_day = fields.Datetime(string=_("Ngày bắt đầu"))
    end_day = fields.Datetime(string=_('Ngày kết thúc'))
    deposit = fields.Float(string="Tiền cọc 20% hóa đơn", readonly=1)
    total = fields.Float(string='Số Tiền ', readonly=1)
    price = fields.Float(string='Tổng Thanh Toán', readonly=1)
    note = fields.Char(string='Ghi Chú')
    time_use = fields.Float(string='Tổng giờ hát', compute='_compute_time_up')

    @api.model
    def create(self, vals_list):
        res = super(MealRegister, self).create(vals_list)
        res['name'] = self.env['ir.sequence'].next_by_code('tigo.service')
        return res

    @api.depends('start_day', 'end_day', 'type')
    def _compute_time_up(self):
        for r in self:
            if r.start_day and r.end_day:
                if r.type == 'sing':
                    time_up = r.end_day - r.start_day
                    r.time_use = time_up.total_seconds() / 3600
                else:
                    r.time_use = 0
            else:
                r.time_use = 0

    @api.onchange('room_id')
    def onchange_dish_ids(self):
        for r in self:
            if r.type == 'eat':
                dish = self.env['tigo.dish'].search([('|'), ('type_room', '=', 'eat'), ('type_room', '=', 'all')]).ids

                return {'domain': {'dish_ids': [('id', 'in', dish)]}}
            else:
                dish = self.env['tigo.dish'].search([('|'), ('type_room', '=', 'sing'), ('type_room', '=', 'all')]).ids
                return {'domain': {'dish_ids': [('id', 'in', dish)]}}

    @api.onchange('dish_ids')
    def onchange_dish_id(self):
        for r in self:
            price_room = sum(r.room_id.mapped('price'))
            r.price = sum(r.dish_ids.mapped('price_total'), (r.time_use * price_room))
            r.deposit = (r.price * 0.2)
            r.total = r.price - r.deposit

    @api.onchange('end_day', 'start_day', 'type', 'room_id')
    def onchange_end_day(self):
        for r in self:
            if r.type == 'eat':
                r.time_use = 0
                r.price = sum(r.dish_ids.mapped('price_total'), (r.time_use * 40000))
                r.deposit = (r.price * 0.2)
                r.total = r.price - r.deposit
            elif r.type == 'sing':
                r.price = sum(r.dish_ids.mapped('price_total'), (r.time_use * 40000))
                r.deposit = (r.price * 0.2)
                r.total = r.price - r.deposit

    def action_order(self):
        for r in self:
            r.state = 'order'

    def action_pay(self):
        for r in self:
            r.state = 'pay'

    def action_cancel(self):
        for r in self:
            r.state = 'cancel'

    @api.onchange('type', 'room_id')
    def onchange_room_id(self):
        for r in self:
            if r.type == 'eat':
                room = self.env['tigo.room'].search([('type_room', '=', 'eat')]).ids
                return {'domain': {'room_id': [('id', 'in', room)]}}
            else:
                room = self.env['tigo.room'].search([('type_room', '=', 'sing')]).ids
                return {'domain': {'room_id': [('id', 'in', room)]}}
