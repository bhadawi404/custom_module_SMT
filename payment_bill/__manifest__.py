# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment SMT',
    'version': '1.1',
    'category': 'Sukses Mandiri Teknindo',
    'summary': 'Payment in Sukses Mandiri Teknindo',
    'description': "",
    'website': 'https://smtek-tool.com/',
    'depends': [
       'core_smt','purchase_order_supplier','master_data'
    ],
    'data': [
        'views/payment_views.xml',
        'security/ir.model.access.csv',
        'views/payment_menu_views.xml',

    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
