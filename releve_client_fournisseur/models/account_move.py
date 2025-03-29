# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError



import logging
_logger = logging.getLogger(__name__)


class account_move(models.Model):
    _inherit = "account.move"



    total_en_dinar = fields.Float(compute="compute_total_en_dinar")

    montant_tva_exonere = fields.Float(compute="compute_montant_tva_exonere")


    mt_regle_dnt = fields.Float(compute="compute_mt_regle_dnt")
    solde_due_dnt = fields.Float(compute="compute_solde_due_dnt")

    related_pickings = fields.Text(compute="compute_related_pickings")



    @api.depends('amount_residual')
    def compute_solde_due_dnt(self):
        for rec in self:

            rec.solde_due_dnt = rec.amount_residual



    @api.depends('amount_total', 'amount_residual')
    def compute_mt_regle_dnt(self):
        for rec in self:

            rec.mt_regle_dnt = (rec.amount_total - rec.amount_residual)

    @api.depends('amount_total')
    def compute_total_en_dinar(self):
        for rec in self:

            rec.total_en_dinar = rec.amount_total_in_currency_signed


    @api.depends('amount_total')
    def compute_montant_tva_exonere(self):
        for rec in self:
            if rec.amount_total:

                rec.montant_tva_exonere = (rec.amount_total * 19) /100
            else:
                rec.montant_tva_exonere = False








