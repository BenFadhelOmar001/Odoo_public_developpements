# -*- coding: utf-8 -*-

{
    'name': 'MRP custom',
    'version': '1.0',
    'category': 'manifacturing',
    'description': "Custom version of MRP module that contain planning, maintenance, quality and other analytic features ",
    'author': 'Ben Fadhel Omar',
    'images': [
    ],
    'depends': ['base_setup', 'base','mrp','stock', 'board','mrp_account_custom'],
    'data': [

        'security/ir.model.access.csv',
        'security/security.xml',
        'views/prod_custom_views.xml',
        'views/mrp_workcenter_views.xml',
        'views/kpi_dashboard.xml',
        'views/mrp_production_views.xml',
        'views/mrp_workorder_views.xml',
        'views/mrp_bom_views.xml',
        'views/report_work_order.xml',
        'views/maintenance_views.xml',
        'wizards/split_mo_wizard_view.xml',
    ],

    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {
        'web.assets_common': [
            'mrp_custom/static/src/scss',
        ],
    }

}
