# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Quản lý suất ăn',
    'version': '1.2',
    'summary': 'Invoices & Payments',
    'sequence': 10,
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': [
        'base', 'hr'
    ],
    'data': ['views/meal_register.xml',
             'views/dish.xml',
             'views/menu.xml',
             'views/hr_employee_inherit_view.xml',
             'views/room.xml',
             'views/service.xml',
             'views/menu_service.xml',

             'security/ir.model.access.csv',
             'security/qlsa_security.xml'
             ],
    'license': 'LGPL-3',
}
