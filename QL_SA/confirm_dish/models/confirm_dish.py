from odoo import api, fields, models


class CofirmDish(models.Model):
    _name = 'cofirm.ish'
    _description = 'Xác nhận đã nhận suất ăn'

    name = fields.Char()
