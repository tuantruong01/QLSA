from odoo import models, fields, _, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class MealRegister(models.Model):
    _name = 'tigo.service'
    _description = 'Dịch vụ'

    name_id = fields.Many2one('hr.employee', string=_('Người Đặt'), required=1)
    name = fields.Char(string=_('Mã Đặt Phòng'), readonly=1)
    type = fields.Selection([('sing', 'Hát'), ('eat', 'Ăn uống')], string=_('Kiểu Dịch Vụ'), default="eat")
    state = fields.Selection([('quotes', 'Báo Giá'),
                              ('order', 'Đặt Phòng'),
                              ('pay', 'Thanh Toán'),
                              ('payed', 'Đã Thanh Toán'),
                              ('cancel', 'Hủy')], string='Trạng Thái', default='quotes')
    room_id = fields.Many2one('tigo.room', string=_('Phòng'))
    start_day = fields.Datetime(string=_("Ngày bắt đầu"), required=True)
    end_day = fields.Datetime(string=_('Ngày kết thúc'), required=True)
    deposit = fields.Float(string="Tiền cọc")
    price = fields.Float(string='Tiền Phòng', readonly=1)
    time_use = fields.Float(string='Giờ Sử Dụng', compute='_compute_time_up')
    order_dish_ids = fields.One2many('tigo.dish.order', 'order_dish_id', string=_('Đặt Món Ăn'))

    @api.model
    def create(self, vals_list):
        res = super(MealRegister, self).create(vals_list)
        res['name'] = self.env['ir.sequence'].next_by_code('tigo.service')
        return res

    @api.depends('start_day', 'end_day', 'type', 'room_id', 'price')
    def _compute_time_up(self):
        for r in self:
            if r.start_day and r.end_day and r.room_id:
                if r.type == 'sing' or r.type == 'eat':
                    time_up = r.end_day - r.start_day
                    r.time_use = time_up.total_seconds() / 3600
                    r.price = r.room_id.price * r.time_use
                else:
                    r.time_use = 0
            else:
                r.time_use = 0

    def action_order(self):
        for r in self:
            r.state = 'order'

    def action_pay(self):
        for r in self:
            r.state = 'pay'

    def action_cancel(self):
        for r in self:
            r.state = 'cancel'
            return {
                'name': _('note'),
            }

    def action_payed(self):
        for r in self:
            r.state = 'payed'

    @api.onchange('type', 'room_id')
    def onchange_room_id(self):
        for r in self:
            if r.type == 'eat':
                room = self.env['tigo.room'].search([('type_room', '=', 'eat')]).ids
                return {'domain': {'room_id': [('id', 'in', room)]}}
            else:
                room = self.env['tigo.room'].search([('type_room', '=', 'sing')]).ids
                return {'domain': {'room_id': [('id', 'in', room)]}}

    @api.onchange('start_day')
    def onchange_day_start(self):
        for r in self:
            if r.start_day and r.start_day < datetime.now() - timedelta(days=1):
                raise UserError(_('Ngày bắt đầu phải lớn hơn hoặc bằng ngày hiện tại.'))
            else:
                pass

    @api.onchange('end_day')
    def onchange_day_end(self):
        for r in self:
            if r.start_day and r.end_day:
                if r.end_day and r.end_day < r.start_day:
                    raise UserError(_('Ngày kết thúc phải lớn hơn ngày hiện tại.'))
                else:
                    pass
