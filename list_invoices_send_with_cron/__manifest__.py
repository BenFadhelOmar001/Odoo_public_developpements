# -*- coding: utf-8 -*-
{
    'name' : 'custom_portal_preview_report',
    'description':"""
custom_portal_preview_report    """,
    'version' : '18.0',
    'category': 'Custom',
    'website': 'https://www.exploit-consult.com',
    'depends' : ['base', 'account'],
    'data': [
      
        'views/list_invoices_send_view.xml',
        'security/ir.model.access.csv',


    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    
}
