##############################################################################
#
#    Copyright (C) 2022-Present Speeduplight (<https://speeduplight.com>)
#
##############################################################################
{
    "name": "Collects cheque payments information from POS",
    "version": '18.0.0.0',
    'sequence': -10,
    "category": "Point of Sale",
    'license': 'OPL-1',
    "author": "Speeduplight",
    "description": """POS check pos cheque information on pos cheque information on point of sale payment detail filled with
    cheque number pos cheque number print pos order report with cheque number print order with check number add bank detail in 
    point of sale pos bank detail with cheque number cheque details point of sale check print cheque information on the 
    receipt in pos print cheque number on pos receipt check info pos receipt cheque info pos payment with cheque info. display cheque in pos display cheque number in pos
    POS cheque number: A unique identification code assigned to a point-of-sale (POS) transaction involving a cheque payment check information. 
    This number helps track and verify the transaction, ensuring accuracy and transparency in financial records. cheque pos point of sale cheque cheque point of sale""",
    'summary': """POS check pos cheque information on pos cheque information on point of sale payment detail filled with
    cheque number pos cheque number print pos order report with cheque number print order with check number add bank detail in 
    point of sale pos bank detail with cheque number cheque details point of sale check print cheque information on the 
    receipt in pos print cheque number on pos receipt check info pos receipt cheque info pos payment with cheque info. display cheque in pos display cheque number in pos
    POS cheque number: A unique identification code assigned to a point-of-sale (POS) transaction involving a cheque payment check information. 
    This number helps track and verify the transaction, ensuring accuracy and transparency in financial records. cheque pos point of sale cheque cheque point of sale""",
    "website": "https://speeduplight.com",
    "depends": ['base', 'point_of_sale'],
    "data": [
        'views/pos_config.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'sp_pos_add_cheque_number/static/src/js/Popups/ChequePopUp.js',
            'sp_pos_add_cheque_number/static/src/js/PaymentScreen.js',
        ],
        'web.assets_qweb': [
            'sp_pos_add_cheque_number/static/src/xml/pos.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 10,
    'currency': 'USD',
    'images': ['static/description/pos_cheque_number_banner.png']
}
