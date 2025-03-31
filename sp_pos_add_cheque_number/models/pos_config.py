##############################################################################
#
#    Copyright (C) 2022-Present Speeduplight (<https://speeduplight.com>)
#
##############################################################################
from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    cheque_information = fields.Boolean(string="Collects Cheque Information")
    bank = fields.Many2one('res.bank')
