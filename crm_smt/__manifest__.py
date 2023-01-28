# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'CRM SMT',
    'version': '1.1',
    'category': 'Sukses Mandiri Teknindo/CRM',
    'summary': 'CRM in Sukses Mandiri Teknindo',
    'description': "",
    'website': 'https://smtek-tool.com/',
    'depends': [
        
    ],
    'data': [
        'views/crm_contact_views.xml',
        'security/ir.model.access.csv',
        'views/crm_menu_views.xml',

    ],

    'installable': True,
    'application': True,
    'auto_install': False,

}
