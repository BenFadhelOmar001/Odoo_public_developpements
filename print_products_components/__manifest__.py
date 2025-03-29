# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'print_products_components',
    'version': '1.1',
    'category': 'CUSTOM',
    'sequence': 75,
    'summary': '',
    'description': "",
    'website': 'https://exploit-consult.com',
    'images': [

    ],
    'depends': [
        'base',
        'base_setup',
        'sale',
        'report_xlsx',


    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/views.xml',


    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
