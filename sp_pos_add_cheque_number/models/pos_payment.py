##############################################################################
#
#    Copyright (C) 2022-Present Speeduplight (<https://speeduplight.com>)
#
##############################################################################
from odoo import api, fields, models


class PosPayment(models.Model):
    _inherit = "pos.payment"

    cheque_owner_name = fields.Char(string="Bank")
    cheque_bank = fields.Many2one('res.bank', string="Bank")
    bank_account = fields.Char(string="Date d'echéance")
    cheque_number = fields.Integer(string="Numéro de chaque")
