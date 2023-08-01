from odoo import models, fields, _, api


class Room(models.Model):
    _name = 'tigo.room'
    _description = 'Phòng'

    id_room = fields.Integer(string=_('Mã Phòng'), requied=True)
    name = fields.Char(string=_('Tên Phòng'), requied=True)
    type_room = fields.Selection([('sing', 'Phòng Hát'), ('eat', 'Phòng Ăn')], string=_('Kiểu Phòng'))
    sate = fields.Selection([('unoccupied', 'Trống'), ('occupied', 'Đã Được Đặt')], string=_('Trạng Thái'),
                            default="unoccupied", readonly=1)



