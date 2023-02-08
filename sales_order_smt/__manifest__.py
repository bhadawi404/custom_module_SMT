# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sales Order SMT',
    'version': '1.1',
    'category': 'Sukses Mandiri Teknindo/Sales Order',
    'summary': 'Sales Order in Sukses Mandiri Teknindo',
    'description': "",
    'website': 'https://smtek-tool.com/',
    'depends': [
        'core_smt','crm_smt','master_data'
    ],
    'data': [
        'views/sales_order_views.xml',
        'views/quotation_views.xml',
        'security/ir.model.access.csv',
        'views/quote_menu_views.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
