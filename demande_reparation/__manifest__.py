# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'demande_reparation',
    'version': '18.0.0.0.0',
    'category': 'CUSTOM',
    'sequence': 75,
    'summary': '',
    'description': "",
    'website': 'https://exploit-consult.com',
    'images': [

    ],
    'depends': [
        'base',
        'purchase',
        'sale',


    ],
    'data': [
        'security/ir.model.access.csv',
        'views/demande_reparation_view.xml',


    ],

    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
