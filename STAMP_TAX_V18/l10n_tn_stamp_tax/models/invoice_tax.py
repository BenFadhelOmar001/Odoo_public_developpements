# -*- coding: utf-8 -*-

from odoo import models, fields, api, http
import logging

_logger = logging.getLogger(__name__)


class AccountTax(models.Model):
    _inherit = "account.tax"

    is_stamp = fields.Boolean("Is Stamp Tax")
    fodec = fields.Boolean("FODEC")


class AccountTax(models.Model):
    _inherit = "account.tax"

    is_stamp = fields.Boolean("Is Stamp Tax")
    fodec = fields.Boolean("FODEC")

class account_move_line(models.Model):
    _inherit = 'account.move.line'

    is_timbre = fields.Boolean()

    

class InvoiceStampTax(models.Model):
    _inherit = 'account.move'

    stamp_tax = fields.Many2one('account.tax',string="Stamp Tax")
    #stamp_tax = fields.Many2one('account.tax',string="Stamp Tax", domain=[('is_stamp', '=', True)])
    fodec = fields.Many2one('account.tax',string="FODEC", domain=[('fodec', '=', True)])

    
    def action_post(self):
    # Disabled by default to avoid breaking automated action flow
        res = super(InvoiceStampTax, self).action_post()
        for rec in self:
            stamp = False
            line_timbre_ids = rec.env['account.move.line'].search([('move_id', '=', rec.id)])
            if line_timbre_ids:
                for line_timbre in line_timbre_ids:
                    for tax in line_timbre.tax_ids:
                        if tax.is_stamp == True:
                            stamp = True
            if stamp == False:

                context = self._context
                _logger.info("****res.get('default_move_type') %s", context.get('default_move_type'))
                _logger.info("****res.get('default_move_type')")
                taxes_vente = rec.env['account.tax'].search([('is_stamp', '=', True), ('type_tax_use', '=', 'sale')], limit=1)
                taxes_achat = rec.env['account.tax'].search([('is_stamp', '=', True), ('type_tax_use', '=', 'purchase')], limit=1)

                
                
                _logger.info("*************** context.get('default_move_type') %s", context.get('default_move_type'))
                if context.get('default_move_type') == 'in_invoice':
                    _logger.info("*************** in_invoice ")
                    if taxes_achat:
                        _logger.info("*************** taxes_achat %s", taxes_achat)
                        line_id = rec.env['account.move.line'].create({'tax_ids': [(4, taxes_achat.id)],
                                                                       'move_id': rec._origin.id})
                if context.get('default_move_type') == 'out_invoice':
                    _logger.info("*************** out_invoice ")
                    if taxes_vente:
                        
                        _logger.info("*************** taxes_vente %s", taxes_vente)
                        _logger.info("*************** rec.id %s", rec.id)
                        _logger.info("*************** rec._origin.id %s", rec._origin.id)
                        _logger.info("*************** rec._origin %s", rec._origin)
                        #line_id.write({'tax_ids': [(4, taxes_vente.id)]})
                       


                        line_id = rec.env['account.move.line'].create({'tax_ids': [(4, taxes_vente.id)],
                                                                        'move_id':rec._origin.id})
        return False

    