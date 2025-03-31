# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'facturation_bc_bmt',
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
        'sale',
        'infolib_l10n_tn_stamp_tax',


    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/facturation_bc_bmt_view.xml',


    ],

    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
