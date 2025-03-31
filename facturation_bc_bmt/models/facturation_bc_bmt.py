# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'res.partner'

    invoiced = fields.Boolean()

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def go_to_picking(self):
        for order in self:
            order.ensure_one()

            picking_id = order.picking_ids and order.picking_ids[0] or False
            if picking_id:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Delivery Order',
                    'res_model': 'stock.picking',
                    'view_mode': 'form',
                    'res_id': picking_id.id,
                    'target': 'current',
                }

class SaleAdvancePaymentInvInherit(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    total_amount = fields.Float(compute='get_totals')

    @api.depends('sale_order_ids')
    def get_totals(self):
        for wizard in self:
            total_amount = 0
            for order in wizard.sale_order_ids:

                total_amount += order.amount_total
            wizard.total_amount = total_amount





    def create_invoices(self):
        for order in self.sale_order_ids:
            if order.partner_id.invoiced:
                if self.total_amount > 5000.000:
                    raise UserError(_('Vous ne pouvez pas facturer un montant supèrieur à 5000.000 DT pour ce client !'))
                    break
        self._check_amount_is_positive()
        invoices = self._create_invoices(self.sale_order_ids)
        return self.sale_order_ids.action_view_invoice(invoices=invoices)

