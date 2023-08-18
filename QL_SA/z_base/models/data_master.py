from odoo import models, fields, _, api


class Room(models.Model):
    _name = 'tigo.room'
    _description = 'Phòng'

    code_room = fields.Char(string=_('Mã Phòng'), readonly=1)
    name = fields.Char(string=_('Tên Phòng'), requied=True)
    type_room = fields.Selection([('sing', 'Phòng Hát'), ('eat', 'Phòng Ăn')], string=_('Dạng'), default="eat")
    sate = fields.Selection([('unoccupied', 'Trống'), ('occupied', 'Sử dụng')], string=_('Trạng Thái'),
                            default="unoccupied", readonly=1)
    price = fields.Float(string=('Giá Phòng/Giờ'))
    level = fields.Selection([('normal', 'Phòng thường'), ('vip', 'Phòng VIP')], string=_('Kiểu Phòng'),
                             default="normal")

    @api.model
    def create(self, vals_list):
        res = super(Room, self).create(vals_list)
        res['code_room'] = self.env['ir.sequence'].next_by_code('tigo.room')
        return res