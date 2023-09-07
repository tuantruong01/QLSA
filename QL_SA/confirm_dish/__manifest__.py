# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Xác Nhận Ăn',
    'version': '1.2',
    'summary': 'Invoices & Payments',
    'sequence': 10,
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'datas/sequence.xml',
        'views/confirm_dish.xml'
    ],
    'license': 'LGPL-3',
}
