# _*_ coding: utf-8_*_
{
    'name': 'custom_demande_achat',
    'version': '12.0.1.0.0',
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'sequence':-100,
    'category': 'Uncategorized',
    'depends': ['purchase', 'purchase_request', 'sale'],
    'data': [
            'views/purchase_request.xml',
            'security/ir.model.access.csv',

    ],
    'demo': [],
    'application': True,
    'installable':True,
}
