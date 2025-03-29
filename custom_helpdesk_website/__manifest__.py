# -*- coding: utf-8 -*-
{
    'name': "custom_helpdesk_website",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',  'website', 'custom_helpdesk', 'custom_helpdesk_add_standard_fields'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        #'views/helpdesk_portal_templates.xml',
        #'views/helpdesk_portal_templates_client.xml',
        #'views/website_form_it.xml',
        #'views/website_form_rh.xml',
        'views/helpdesk_portal_rh_form.xml',
        'views/helpdesk_portal_templates_md.xml',
        'views/website_reponse_ticket.xml',
        'views/prestataire_templates.xml',

        'views/demande_recrutement_templates.xml',
        'views/demande_recrutement_template_demandeur.xml',
        'views/demande_recrutement_template_followup.xml',
        'views/demande_recrutement_template_rrh.xml',
        'views/demande_recrutement_template_rdrh.xml',
        'views/demande_recrutement_template_direction.xml',
        'views/demande_recrutement_template_drh.xml',

        'views/demande_recrutement_form_access.xml',

        'views/ticket_rh_front_templates.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
            'web.assets_frontend': [
                'custom_helpdesk_website/static/src/js/delete_attachment.js',
                'custom_helpdesk_website/static/src/js/change_domain_hr_jobs_create.js',
                'custom_helpdesk_website/static/src/js/change_domain_hr_jobs_open.js',
                'custom_helpdesk_website/static/src/js/change_domain_dr_metier_create.js',
                'custom_helpdesk_website/static/src/js/change_domain_dr_metier_open.js',
            ],
        },
    }
