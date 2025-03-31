# -*- coding: utf-8 -*-
{
    'name': "CUSTOM PORTAL PREVIEW REPORT",

    'summary': "Collect, organize and share documents.",

    'description': """
App to upload and manage your documents.
    """,

    'category': 'Productivity/Documents',
    'sequence': 80,
    'version': '1.4',
    'application': True,
    'website': 'https://www.odoo.com/app/documents',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale', 'sale_subscription'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'reports/external_layout_boxed_abonnement_mct.xml',
        'reports/external_layout_boxed_abonnement_mct_portal_preview.xml',
        'reports/external_layout_boxed_mct.xml',
        'reports/external_layout_boxed_mct_portal_preview.xml',
        'reports/report_invoice_document.xml',
        'reports/report_document_abonnement_mct.xml',
        'reports/report_invoice_document_portal_preview.xml',
        'reports/report_document_portal_preview_abonnement_mct.xml',
        'views/account_report.xml',
        'views/abonnement_report.xml',

    ],

    
    'license': 'OEEL-1',
    'assets': {
        
    }
}
