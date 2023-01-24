# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase Order SMT',
    'version': '1.1',
    'category': 'Sukses Mandiri Teknindo/Master Data',
    'summary': 'Master Data in Sukses Mandiri Teknindo',
    'description': "",
    'website': 'https://smtek-tool.com/',
    'depends': [
        'master_data'
    ],
    'data': [
        'views/purchase_order_received_views.xml',
        'security/ir.model.access.csv',
        'views/purchase_order_supplier_views.xml',
        'views/purchase_order_menu_views.xml',

    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
