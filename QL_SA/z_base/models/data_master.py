from odoo import models, fields, _, api
from odoo.exceptions import UserError
from datetime import timedelta


class Room(models.Model):
    _name = 'tigo.room'
    _description = 'Phòng'

    code_room = fields.Char(string=_('Mã Phòng'), readonly=1)
    name = fields.Char(string=_('Tên Phòng'), requied=True)
    type_room = fields.Selection([('sing', 'Phòng Hát'), ('eat', 'Phòng Ăn')], string=_('Dạng'))
    sate = fields.Selection([('unoccupied', 'Trống'), ('occupied', 'Sử dụng')], string=_('Trạng Thái'),
                            default="unoccupied", readonly=1)
    price = fields.Float(string=_('Giá Phòng / Giờ'))
    level = fields.Selection([('normal', 'Phòng thường'), ('vip', 'Phòng VIP')], string=_('Kiểu Phòng'),
                             default="normal")

    @api.model
    def create(self, vals_list):
        res = super(Room, self).create(vals_list)
        res['code_room'] = self.env['ir.sequence'].next_by_code('tigo.room')
        return res

    _sql_constraints = [('name', 'unique(name)', 'Không Được Đặt Trùng Tên Phòng')]


class Week(models.Model):
    _name = 'tigo.week'
    _description = 'Tuần Trong Năm'

    name = fields.Char(string='Tuần', required=1)
    begin = fields.Date(string='Từ ngày', required=1)
    end = fields.Date(string='Đến ngày', readonly=1)

    @api.onchange('begin')
    def onchange_begin(self):
        for r in self:
            if r.begin:
                if r.begin.weekday() != 0:
                    raise UserError(_('Bạn phải chọn ngày đầu tuần.'))
                else:
                    r.end = r.begin + timedelta(days=6)
