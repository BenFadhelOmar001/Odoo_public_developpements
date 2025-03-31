# Copyright Netformica - Mohamed Machta
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': "Tunisia Stamp Tax",
    'version': '18.0.0.0.0',
    'author': 'Netformica Web Solutions',
    'website': 'https://www.netformica.com',
    'category': 'Localisation',
    "license": "LGPL-3",
    'depends': ['base', 'account'],
    'application': False,
    'data': [
        #'reports/report_facture_config.xml',
        #'reports/report_facture_template.xml',

        #'views/invoice.xml',
        'views/account_tax_view.xml',
    ],
    'images': [
        'static/description/screen.jpg',
    ],
}
