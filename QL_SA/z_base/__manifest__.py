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
        'base', 'hr', 'point_of_sale', 'product', 'report_xlsx', 'sale'
    ],
    'data': [
        'security/qlsa_security.xml',
        'security/ir.model.access.csv',
        'views/meal_register.xml',
        'views/confirm_dish.xml',
        'views/hr_employee_inherit_view.xml',

        'views/menu_setting_day.xml',
        'views/menu_setting_week.xml',

        'views/service.xml',
        'views/quotes.xml',
        'views/pay_view.xml',

        'views/menu_set.xml',
        'views/menu_table.xml',
        'views/week.xml',
        'views/dish.xml',
        'views/product_product_inherit_views.xml',
        'views/menu_service.xml',
        'views/room_service.xml',
        'views/popup.xml',
        'views/view_setting.xml',

        'datas/sequence.xml',
        'wizard/popup_report_menu_oder.xml',
        'report/report_menu_order.xml',
        'wizard/popup_report_ingredient.xml',

    ],
    'license': 'LGPL-3',
}
