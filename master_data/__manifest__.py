# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Master Data',
    'version': '1.1',
    'category': 'Sukses Mandiri Teknindo/Master Data',
    'summary': 'Master Data in Sukses Mandiri Teknindo',
    'description': "",
    'website': 'https://smtek-tool.com/',
    'depends': [
        'core_smt'
    ],
    'data': [
        'views/master_data_supplier_views.xml',
        'views/master_data_material_views.xml',
        'views/master_data_customer_views.xml',
        'security/ir.model.access.csv',
        'views/master_data_product_views.xml',
        'views/master_data_menu_views.xml',

    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
