# -*- coding: utf-8 -*-
{
    'name' : 'CTonline API',
    'description':"""
calling CTonline api to modify quantities for subscriptions
    """,
    'version' : '18.0',
    'category': 'Custom',
    'website': 'https://www.exploit-consult.com',
    'depends' : ['base', 'base_setup', 'sale', ],
    'data': [
      
        'views/product_template_view.xml',
        'views/res_config_settings_view.xml',

        'data/cronjob_subscriptions.xml',
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    
}
