# -*- encoding: utf-8 -*-

{
    'name': 'Master Production Schedule',
    'version': '1.0',
    'category': 'Manufacturing/Manufacturing',
    'depends': ['mrp', 'purchase_stock'],
    'description': """Master Production Schedule""",
    'author': 'Oussema Khorchani',
    'data': [
        'security/ir.model.access.csv',
        'security/mrp_mps_security.xml',
        'views/mrp_mps_views.xml',
        'views/mrp_mps_menu_views.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/mrp_mps_forecast_details_views.xml'
    ],
    'demo': [
        'data/mps_demo.xml',
    ],
    'application': False,
    'license': 'AGPL-3',
    'assets': {
        'web.assets_backend': [
            'mrp_mps/static/src/js/client_action.js',
            'mrp_mps/static/src/scss/client_action.scss',
        ],
        'web.assets_qweb': [
            'mrp_mps/static/src/xml/**/*',
        ],
    }
}
