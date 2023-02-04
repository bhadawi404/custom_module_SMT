# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Inventory SMT',
    'version': '1.1',
    'category': 'Sukses Mandiri Teknindo/Inventory',
    'summary': 'Inventory in Sukses Mandiri Teknindo',
    'description': "",
    'website': 'https://smtek-tool.com/',
    'depends': [
        'core_smt'
    ],
    'data': [
        'views/inventory_stock_location.xml',
        'views/inventory_stock_warehouse.xml',
        'views/inventory_operation_type.xml',
        'security/ir.model.access.csv',
        'views/inventory_menu_views.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
