# -*- coding: utf-8 -*-
{
    'name' : 'TODO LIST WITH OWL FRAMWORK',
    'version' : '1.0',
    'summary': 'TODO LIST WITH OWL FRAMWORK',
    'sequence': -1,
    'description': """TODO LIST WITH OWL FRAMWORK""",
    'category': 'OWL',
    'depends' : ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_list.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'todo_list_with_owl_framework/static/src/components/*/*.js',
            'todo_list_with_owl_framework/static/src/components/*/*.xml',
            'todo_list_with_owl_framework/static/src/components/*/*.scss',
        ],
    },
}