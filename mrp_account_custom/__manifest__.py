# -*- coding: utf-8 -*-

{
    'name': 'Comptabilité avancée - MRP',
    'version': '1.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Aanalyse de comptabilité de fabrication',
    'description': " ",
    'author': 'Ben Fadhel Omar',
    'depends': ['mrp_account'],
    'data': [

        'security/ir.model.access.csv',
        'security/mrp_account_custom_security.xml',
        'views/mrp_account_view.xml',
        'views/cost_structure_report.xml',
        'reports/mrp_report_views.xml',
        ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
    'assets': {
        'web.assets_common': [
            'mrp_account_custom/static/**/*',
        ],
    }
}
