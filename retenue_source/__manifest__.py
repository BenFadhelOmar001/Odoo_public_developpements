# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: fasluca(<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

{
    'name': 'retenue_source',
    'version': '18.0.0.0',
    'category': 'Sales Management',
    'summary': "Discount on Total in Sale and Invoice With Discount Limit and Approval",
    'author': 'Exploit consult',
    'company': 'Exploit consult',
    'website': 'http://www.cybrosys.com',
    'description': """

Sale Discount for Total Amount
=======================
Module to manage discount on total amount in Sale.
        as an specific amount or percentage
""",
    'depends': ['base',
                'account',


                ],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
        'views/template.xml',


    ],
    'demo': [
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
}
