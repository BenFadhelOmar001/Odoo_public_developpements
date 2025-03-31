# -*- coding: utf-8 -*-


from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)
class JournalAccount(models.Model):
    _inherit = "account.journal"

    retenue_client = fields.Boolean()
    retenue_frs = fields.Boolean()

class AccountPayment(models.Model):
    _inherit = "account.payment"

    retenue_type = fields.Many2one('type.retenue', domain=[('state', '=', 'active')])
    pourcentage = fields.Float()
    retenue_base = fields.Float()
    retenue_brut = fields.Float()
    retenue_frs = fields.Boolean(compute='get_retenue', store=True)
    retenue_client = fields.Boolean(compute='get_retenue', store=True)
    types = fields.One2many('type.retenue', 'account_payment_id', compute='get_types', store=True)

    @api.depends('retenue_type')
    def get_types(self):
        for rec in self:
            rec.types = False
            types = rec.env['type.retenue'].search([('state', '=', 'active')])
            if types:
                for type in types:
                    rec.types += type

    @api.onchange('retenue_type')
    def get_pourcentage(self):
        for rec in self:
            if rec.retenue_type:
                rec.pourcentage = rec.retenue_type.pourcentage

    @api.depends('journal_id')
    def get_retenue(self):
        for rec in self:
            if rec.journal_id:
                rec.retenue_frs = rec.journal_id.retenue_frs
                rec.retenue_client = rec.journal_id.retenue_client
                _logger.info('************* retenue_client %s', rec.retenue_client)

    @api.onchange('retenue_base', 'pourcentage')
    def get_amount(self):
        for rec in self:
            if rec.retenue_type:
                rec.amount = (rec.retenue_base /100) * rec.pourcentage


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    retenue_type = fields.Many2one('type.retenue', domain=[('state', '=', 'active')])
    pourcentage = fields.Float()
    retenue_base = fields.Float()
    retenue_brut = fields.Float()
    retenue_frs = fields.Boolean(compute='get_retenue', store=True)
    retenue_client = fields.Boolean(compute='get_retenue', store=True)





    def _create_payment_vals_from_wizard(self, batch_result):
        payment_vals = {
            'date': self.payment_date,
            'amount': self.amount,
            'payment_type': self.payment_type,
            'partner_type': self.partner_type,
            #'ref': self.communication,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'partner_bank_id': self.partner_bank_id.id,
            'payment_method_line_id': self.payment_method_line_id.id,
            'destination_account_id': self.line_ids[0].account_id.id,
            'retenue_type': self.retenue_type.id,
            'pourcentage': self.pourcentage,
            'retenue_base': self.retenue_base,
            'retenue_brut': self.retenue_brut,
            'retenue_frs': self.retenue_frs,
            'retenue_client': self.retenue_client,
            # 'types': [(6, 0, self.types.ids)],
        }

        if not self.currency_id.is_zero(self.payment_difference) and self.payment_difference_handling == 'reconcile':
            payment_vals['write_off_line_vals'] = {
                'name': self.writeoff_label,
                'amount': self.payment_difference,
                'account_id': self.writeoff_account_id.id,
                'retenue_type': self.retenue_type.id,
                'pourcentage': self.pourcentage,
                'retenue_base': self.retenue_base,
                'retenue_brut': self.retenue_brut,
                'retenue_frs': self.retenue_frs,
                'retenue_client': self.retenue_client,
                # 'types': [(6, 0, self.types.ids)],
            }
        return payment_vals

    @api.depends('journal_id')
    def get_retenue(self):
        for rec in self:
            if rec.journal_id:
                rec.retenue_frs = rec.journal_id.retenue_frs
                rec.retenue_client = rec.journal_id.retenue_client
                _logger.info('************* retenue_client %s', rec.retenue_client)

    @api.onchange('retenue_type')
    def get_pourcentage(self):
        for rec in self:
            if rec.retenue_type:
                rec.pourcentage = rec.retenue_type.pourcentage

    @api.onchange('retenue_base', 'pourcentage')
    def get_amount(self):
        for rec in self:
            if rec.retenue_type:
                rec.amount = (rec.retenue_base /100) * rec.pourcentage


class TypeRetenue(models.Model):
    _name = "type.retenue"

    name = fields.Char()
    pourcentage = fields.Float()
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('active', 'Active'),


    ], default='draft')

    account_payment_id = fields.Many2one('account.payment')
    registration_payment_id = fields.Many2one('account.payment')

    def valide_progressbar(self):
        for rec in self:
            # rec.write({'state': 'valide',})
            rec.state = 'active'

    def cancel_progressbar(self):
        for rec in self:
            # rec.write({'state': 'valide',})
            rec.state = 'draft'




# class AccountInvoiceInherit(models.Model):
#     _inherit = "account.invoice"
#
#     margin_percentagee = fields.Char(string="Pourcentage marge Commerciale", compute="calcul_marge_commerciale", digits=(16, 2))
#     x_margin_percentagee = fields.Char(string="Pourcentage marge Brut", compute="calcul_marge_commerciale", digits=(16, 2))
#     x_margin_amountt = fields.Char(string="Marge brut", compute="calcul_marge_commercialee", digits=(16, 2))
#     margin_amountt = fields.Char(string="Marge commerciale", compute="calcul_marge_commercialee", digits=(16, 2))
#
#     # @api.depends('invoice_line_ids', 'amount_untaxed')
#     # def calcul_marge_commercialee(self):
#     #     for rec in self:
#     #         cout = 0
#     #         cout2 = 0
#     #         for line in rec.invoice_line_ids:
#     #
#     #             for line_cout in line.product_id.seller_ids:
#     #                 cout = line_cout.price * line.quantity
#     #             logistiques = rec.env['stock.valuation.adjustment.lines'].search([('product_id', '=', line.product_id.id)], order='	cost_id desc', limit=1)
#     #
#     #
#     #
#     #             cout2 += logistiques.former_cost_per_unit  * line.quantity
#     #         rec.x_margin_amountt = format(cout2, '.2f')
#     #         rec.margin_amountt = format(cout, '.2f')
#
#     @api.depends('invoice_line_ids', 'amount_untaxed')
#     def calcul_marge_commercialee(self):
#         for rec in self:
#             cout = 0
#             cout2 = 0
#             for line in rec.invoice_line_ids:
#                 cout += line.product_id.standard_price * line.quantity
#
#
#                 cout2 += line.product_id.last_purchase_price * line.quantity
#
#
#             rec.x_margin_amountt = format(rec.amount_untaxed - cout, '.2f')
#             rec.margin_amountt = format(rec.amount_untaxed - cout2, '.2f')
#
#     @api.depends('x_margin_amountt', 'margin_amountt', 'invoice_line_ids', 'amount_untaxed')
#     def calcul_marge_commerciale(self):
#         for rec in self:
#             if rec.amount_untaxed > 0:
#                 margin_percentage = (float(rec.margin_amountt) / rec.amount_untaxed) * 100
#                 rec.margin_percentagee = str(format(margin_percentage, '.2f')) + '%'
#                 x_margin_percentage = (float(rec.x_margin_amountt) / rec.amount_untaxed) * 100
#                 rec.x_margin_percentagee = str(format(x_margin_percentage, '.2f')) + '%'
#     #         # rec.margin_percentage ='200%'
#     #         # rec.x_margin_percentage ='200%'



