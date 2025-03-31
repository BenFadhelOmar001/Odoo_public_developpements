# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError

from datetime import datetime

import logging
_logger = logging.getLogger(__name__)


class releve_partner_wiz(models.TransientModel):
    _name = "releve.partner.wiz"




    partner_id = fields.Many2one('res.partner')
    date_debut = fields.Date(required=True, default=datetime.today())
    date_fin = fields.Date(required=True, default=datetime.today())

    the_move_type = fields.Selection([('client', 'Factures client'), ('fournisseur', 'Factures fournisseur')],default='client', required=True)



    def generer_releve_report(self):

        data = {"ids": [self.id], "form": self.read()[0]}
        return self.env.ref("report_statement.action_report_releve_partner_wiz").report_action(
            self, data=data
        )



class ReportRelevePartnerWiz(models.AbstractModel):
    """Abstract Model for report template.
    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = "report.report_statement.releve_partner_wiz_report"


    def get_records(self, record):
        date_from = record.date_debut
        date_to = record.date_fin
        partner_id = record.partner_id
        the_move_type = record.the_move_type

        if the_move_type == 'client':
            domain = [
            ("date", "<=", date_to),
            ("date", ">=", date_from),
            ("state", "=", "posted"),
            ("partner_id", "=", partner_id.id),
            ("move_type", "in", ['out_invoice','out_refund'])
            
        ]

        if the_move_type == 'fournisseur':
            domain = [
            ("date", "<=", date_to),
            ("date", ">=", date_from),
            ("state", "=", "posted"),
            ("partner_id", "=", partner_id.id),
            ("move_type", "in", ['in_invoice','in_refund'])
            
        ]


        
        
        line_ids = self.env["account.move"].search(domain, order="invoice_date")
        return line_ids





    def total_amount_total(self, record):
        date_from = record.date_debut
        date_to = record.date_fin
        partner_id = record.partner_id
        the_move_type = record.the_move_type

        if the_move_type == 'client':
            domain = [
            ("date", "<=", date_to),
            ("date", ">=", date_from),
            ("state", "=", "posted"),
            ("partner_id", "=", partner_id.id),
            ("move_type", "in", ['out_invoice','out_refund'])
            
        ]

        if the_move_type == 'fournisseur':
            domain = [
            ("date", "<=", date_to),
            ("date", ">=", date_from),
            ("state", "=", "posted"),
            ("partner_id", "=", partner_id.id),
            ("move_type", "in", ['in_invoice','in_refund'])
            
        ]


        
        
        line_ids = self.env["account.move"].search(domain, order="invoice_date")
        total_amount_total = 0
        if line_ids:
            
            for enreg in line_ids:
                total_amount_total = total_amount_total + enreg.amount_total
        return total_amount_total



    # def total_dinar_ht(self, record):
    #     date_from = record.date_debut
    #     date_to = record.date_fin
    #     partner_id = record.partner_id
    #     the_move_type = record.the_move_type
    #
    #     if the_move_type == 'client':
    #         domain = [
    #         ("date", "<=", date_to),
    #         ("date", ">=", date_from),
    #         ("state", "=", "posted"),
    #         ("partner_id", "=", partner_id.id),
    #         ("move_type", "in", ['out_invoice','out_refund'])
    #
    #     ]
    #
    #     if the_move_type == 'fournisseur':
    #         domain = [
    #         ("date", "<=", date_to),
    #         ("date", ">=", date_from),
    #         ("state", "=", "posted"),
    #         ("partner_id", "=", partner_id.id),
    #         ("move_type", "in", ['in_invoice','in_refund'])
    #
    #     ]
    #
    #
    #
    #
    #     line_ids = self.env["account.move"].search(domain, order="invoice_date")
    #     total_dinar_ht = 0
    #     if line_ids:
    #
    #         for enreg in line_ids:
    #             total_dinar_ht = total_dinar_ht + enreg.total_en_dinar
    #     return total_dinar_ht



    def total_mt_regle_dnt(self, record):
        date_from = record.date_debut
        date_to = record.date_fin
        partner_id = record.partner_id
        the_move_type = record.the_move_type

        if the_move_type == 'client':
            domain = [
            ("date", "<=", date_to),
            ("date", ">=", date_from),
            ("state", "=", "posted"),
            ("partner_id", "=", partner_id.id),
            ("move_type", "in", ['out_invoice','out_refund'])
            
        ]

        if the_move_type == 'fournisseur':
            domain = [
            ("date", "<=", date_to),
            ("date", ">=", date_from),
            ("state", "=", "posted"),
            ("partner_id", "=", partner_id.id),
            ("move_type", "in", ['in_invoice','in_refund'])
            
        ]


        
        
        line_ids = self.env["account.move"].search(domain, order="invoice_date")
        total_mt_regle_dnt = 0
        if line_ids:
            
            for enreg in line_ids:
                total_mt_regle_dnt = total_mt_regle_dnt + enreg.mt_regle_dnt
        return total_mt_regle_dnt


    def total_solde_due_dnt(self, record):
        date_from = record.date_debut
        date_to = record.date_fin
        partner_id = record.partner_id
        the_move_type = record.the_move_type

        if the_move_type == 'client':
            domain = [
            ("date", "<=", date_to),
            ("date", ">=", date_from),
            ("state", "=", "posted"),
            ("partner_id", "=", partner_id.id),
            ("move_type", "in", ['out_invoice','out_refund'])
            
        ]

        if the_move_type == 'fournisseur':
            domain = [
            ("date", "<=", date_to),
            ("date", ">=", date_from),
            ("state", "=", "posted"),
            ("partner_id", "=", partner_id.id),
            ("move_type", "in", ['in_invoice','in_refund'])
            
        ]


        
        
        line_ids = self.env["account.move"].search(domain, order="invoice_date")
        total_solde_due_dnt = 0
        if line_ids:
            
            for enreg in line_ids:
                total_solde_due_dnt = total_solde_due_dnt + enreg.solde_due_dnt
        return total_solde_due_dnt




    def get_reglement_from_move(self, record,move):
        
        domain = [

            ("ref", "=", move.name),
        ]
        payment_ids = self.env["account.payment"].search(domain ,order="date")
        str_reglement = ''
        if payment_ids:
            for enreg in payment_ids:
                mois = datetime.strftime(datetime.strptime(str(enreg.date), "%Y-%m-%d"), "%m")
                jour = datetime.strftime(datetime.strptime(str(enreg.date), "%Y-%m-%d"), "%d")

                reg = str(jour)+'/'+str(mois) +' '+ str(enreg.payment_method_line_id.name) + '**'
                str_reglement = str_reglement + reg
        
        return str_reglement



    @api.model
    def _get_report_values(self, docids, data=None):
        """Get report values."""
        ids = data.get("ids", [])
        docs = self.env["releve.partner.wiz"].browse(ids)
        return {
            "doc_ids": ids,
            "doc_model": "releve.partner.wiz",
            "docs": docs,
            "get_records": self.get_records,
            "total_amount_total": self.total_amount_total,
            #"total_dinar_ht": self.total_dinar_ht,
            "total_mt_regle_dnt": self.total_mt_regle_dnt,
            "total_solde_due_dnt": self.total_solde_due_dnt,
            "get_reglement_from_move": self.get_reglement_from_move,
            


            

            
        }


