##############################################################################
#
#    Copyright (C) 2022-Present Speeduplight (<https://speeduplight.com>)
#
##############################################################################
from odoo import api, fields, models


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    cheque_information = fields.Boolean(string="Collects Cheque Information")
