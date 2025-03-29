# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError



import logging
_logger = logging.getLogger(__name__)


class account_move(models.Model):
    _inherit = "account.move"




    # nbre_colis = fields.Integer()
    # poids_total_brut = fields.Float()
    # poids_total_net = fields.Float()


    #total_en_dinar = fields.Float(compute="compute_total_en_dinar")

    #total_lettre_dinar = fields.Char(compute="compute_total_lettre_dinar")


    # total_lettre = fields.Char(compute="compute_total_lettre")
    #
    # montant_tva_exonere = fields.Float(compute="compute_montant_tva_exonere")

    #cours = fields.Char(compute="compute_cours")

    #cours_float = fields.Float(compute="compute_cours_float")

    # mode_de_paiement = fields.Char()
    # mode_de_livraison = fields.Char()


    mt_regle_dnt = fields.Float(compute="compute_mt_regle_dnt")
    solde_due_dnt = fields.Float(compute="compute_solde_due_dnt")


    @api.depends('amount_residual')
    def compute_solde_due_dnt(self):
        for rec in self:

            rec.solde_due_dnt = rec.amount_residual
            


    @api.depends('amount_total', 'amount_residual')
    def compute_mt_regle_dnt(self):
        for rec in self:

            rec.mt_regle_dnt = rec.amount_total - rec.amount_residual
            





    # @api.depends('currency_id', 'invoice_date')
    # def compute_cours(self):
    #     for rec in self:
    #         to_convert_currency_id = rec.env['res.currency'].search([('is_dinar', '=', True)])
    #         if to_convert_currency_id and rec.invoice_date:
    #
    #             rec.cours = str(to_convert_currency_id._get_rates(rec.company_id, rec.invoice_date).get(to_convert_currency_id.id))[0:6]
    #
    #         else:
    #             rec.cours = False


    # @api.depends('currency_id', 'invoice_date')
    # def compute_cours_float(self):
    #     for rec in self:
    #         to_convert_currency_id = rec.env['res.currency'].search([('is_dinar', '=', True)])
    #         if to_convert_currency_id and rec.invoice_date:
    #
    #             rec.cours_float = to_convert_currency_id._get_rates(rec.company_id, rec.invoice_date).get(to_convert_currency_id.id)
    #
    #         else:
    #             rec.cours_float = 0



    @api.depends('amount_total')
    def compute_montant_tva_exonere(self):
        for rec in self:
            if rec.amount_total:

                rec.montant_tva_exonere = (rec.amount_total * 19) /100
            else:
                rec.montant_tva_exonere = False




    #@api.depends('total_en_dinar')
    # def compute_total_lettre_dinar(self):
    #     for rec in self:
    #         if rec.total_en_dinar:
    #             to_convert_currency_id = rec.env['res.currency'].search([('is_dinar', '=', True)])
    #             if to_convert_currency_id:
    #                 rec.total_lettre_dinar = to_convert_currency_id.amount_to_text(rec.total_en_dinar)
    #             else:
    #                 rec.total_lettre_dinar = False
    #
    #
    #         else:
    #             rec.total_lettre_dinar = False

    # @api.depends('amount_total')
    # def compute_total_lettre(self):
    #     for rec in self:
    #         if rec.amount_total:
    #             rec.total_lettre = rec.currency_id.amount_to_text(rec.amount_total)
    #         else:
    #             rec.total_lettre = False



    # @api.depends('amount_total')
    # def compute_total_en_dinar(self):
    #     for rec in self:
    #
    #         to_convert_currency_id = rec.env['res.currency'].search([('is_dinar', '=', True)])
    #
    #         if to_convert_currency_id:
    #
    #             rec.total_en_dinar = rec.currency_id._convert(rec.amount_total, to_convert_currency_id, rec.company_id, rec.invoice_date or fields.Date.today())
    #         else:
    #             rec.total_en_dinar = False



