# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'custom_centrale_meuble',
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
        'mrp',
        'sale',


    ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',


    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
