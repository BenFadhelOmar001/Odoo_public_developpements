# -*- coding: utf-8 -*-



{
    'name': 'REPORT STATEMENT',
    'version': '15.0',
    'category': 'Custom',
    'summary': '',
    'description': """

       """,
    'website': 'exploit-consult.com',
    'depends': ['base', 'account'],
    'data': [


        'security/ir.model.access.csv',

        'views/account_move_view.xml',
        'views/res_partner_view.xml',

        'wizards/releve_partner_wiz_view.xml',

        'reports/releve_partner_wiz_report_config.xml',
        'reports/releve_partner_wiz_report_template.xml',
        
        
    ],

    'installable': True,
    'auto_install': False,
    'application': True,

    
    
}
