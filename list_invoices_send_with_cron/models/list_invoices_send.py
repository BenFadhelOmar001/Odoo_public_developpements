# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class list_invoices_send(models.Model):
    _name = 'list.invoices.send'

    invoice_id = fields.Many2one('account.move')


class accountmoveinherit(models.Model):
    _inherit = 'account.move'

    def action_send_and_print(self):
        invoices = self.env['list.invoices.send'].search([])
        if invoices:
            for invoice in invoices:
                invoice.unlink()
        for move in self.ids:
            self.env['list.invoices.send'].create({
                'invoice_id': move
            })
        return {
            'name': _("Print & Send"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move.send.wizard' if len(self) == 1 else 'account.move.send.batch.wizard',
            'target': 'new',
            'context': {
                'active_model': 'account.move',
                'active_ids': self.ids,
            },
        }

    @api.model
    def _cron_account_move_send(self, job_count=10):
        """ Process invoices generation and sending asynchronously.
        :param job_count: maximum number of jobs to process if specified.
        """

        def get_account_notification(moves, is_success: bool):
            _ = self.env._
            return [
                'account_notification',
                {
                    'type': 'success' if is_success else 'warning',
                    'title': _('Invoices sent') if is_success else _('Invoices in error'),
                    'message': _('Invoices sent successfully.') if is_success else _(
                        "One or more invoices couldn't be processed."),
                    'action_button': {
                        'name': _('Open'),
                        'action_name': _('Sent invoices') if is_success else _('Invoices in error'),
                        'model': 'account.move',
                        'res_ids': moves.ids,
                    },
                },
            ]

        limit = job_count + 1
        to_process = self.env['account.move'].search(
            [('sending_data', '!=', False)],
            limit=limit,
        )
        need_retrigger = len(to_process) > job_count
        if not to_process:
            return

        to_process = to_process[:job_count]
        if not self.env['res.company']._with_locked_records(to_process, allow_raising=False):
            return

        # Collect moves by res.partner that executed the Send & Print wizard, must be done before the _process
        # that modify sending_data.
        moves_by_partner = to_process.grouped(lambda m: m.sending_data['author_partner_id'])

        self.env['account.move.send']._generate_and_send_invoices(
            to_process,
            from_cron=True,
        )

        for partner_id, partner_moves in moves_by_partner.items():
            partner = self.env['res.partner'].browse(partner_id)
            partner_moves_error = partner_moves.filtered(lambda m: m.sending_data and m.sending_data.get('error'))
            if partner_moves_error:
                partner._bus_send(*get_account_notification(partner_moves_error, False))
            partner_moves_success = partner_moves - partner_moves_error
            if partner_moves_success:
                partner._bus_send(*get_account_notification(partner_moves_success, True))
            partner_moves_error.sending_data = False

        if need_retrigger:
            self.env.ref('account.ir_cron_account_move_send')._trigger()

###################################################################################################################################

        invoices = self.env['list.invoices.send'].search([])
        if invoices:
            for invoice in invoices:
                invoice.unlink()


        
    




