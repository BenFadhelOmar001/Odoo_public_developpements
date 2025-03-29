# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from datetime import timedelta

import logging
_logger = logging.getLogger(__name__)

class remarque_remarque(models.Model):
    _name = "remarque.remarque"

    name = fields.Char()


class MrpProductionInherit(models.Model):
    _inherit = 'mrp.production'



    date_planned_start_custom = fields.Datetime(
        'Date prévue', copy=False, compute="_get_default_date_planned_start_custom",
        help="Date at which you plan to start the production.",
        index=True)

    @api.depends('origin')
    def _get_default_date_planned_start_custom(self):
        for rec in self:
            _logger.info('***************** function ')
            picking = rec.env['stock.picking'].search([('origin', '=', rec.origin), ('state', '=', 'waiting')], limit=1)
            _logger.info('***************** picking %s', picking)
            date_planned_start = datetime.datetime.now()
            if picking:
                date_planned_start = picking.scheduled_date - timedelta(days=1) - timedelta(int(rec.product_id.produce_delay))
                _logger.info('***************** date_planned_start %s', date_planned_start)
                _logger.info('***************** timedelta(int(rec.product_id.produce_delay)) %s', timedelta(int(rec.product_id.produce_delay)))
                _logger.info('***************** picking.scheduled_date %s', picking.scheduled_date)

            rec.date_planned_start_custom = date_planned_start

    def _create_workorder(self):
        for production in self:
            if not production.bom_id or not production.product_id:
                continue
            workorders_values = []

            product_qty = production.product_uom_id._compute_quantity(production.product_qty, production.bom_id.product_uom_id)
            exploded_boms, dummy = production.bom_id.explode(production.product_id, product_qty / production.bom_id.product_qty, picking_type=production.bom_id.picking_type_id)

            for bom, bom_data in exploded_boms:
                # If the operations of the parent BoM and phantom BoM are the same, don't recreate work orders.
                if not (bom.operation_ids and (not bom_data['parent_line'] or bom_data['parent_line'].bom_id.operation_ids != bom.operation_ids)):
                    continue
                for operation in bom.operation_ids:
                    if operation._skip_operation_line(bom_data['product']):
                        continue
                    workorders_values += [{
                        'name': operation.name,
                        'production_id': production.id,
                        'workcenter_id': operation.workcenter_id.id,
                        'sequence': operation.sequence_center,
                        'product_uom_id': production.product_uom_id.id,
                        'operation_id': operation.id,
                        'state': 'pending',
                    }]
            production.workorder_ids = [(5, 0)] + [(0, 0, value) for value in workorders_values]
            for workorder in production.workorder_ids:
                workorder.duration_expected = workorder._get_duration_expected()









class mrp_routing_workcenter_inherit(models.Model):
    _inherit = 'mrp.routing.workcenter'

    sequence_center = fields.Integer()

class mrp_workorder_inherit(models.Model):
    _inherit = 'mrp.workorder'

    sequence = fields.Integer()
    demarage_action = fields.Boolean(default=True, compute='get_demarage_action')
    remarque_id = fields.Many2one('remarque.remarque')
    date_start = fields.Datetime(compute='get_date_start')
    date_finished = fields.Datetime()

    @api.depends('production_id')
    def get_date_start(self):
        for rec in self:
            rec.date_start = rec.production_id.date_planned_start_custom


    @api.depends('production_availability', 'date_finished')
    def _compute_state(self):
        # Force the flush of the production_availability, the wo state is modify in the _compute_reservation_state
        # It is a trick to force that the state of workorder is computed as the end of the
        # cyclic depends with the mo.state, mo.reservation_state and wo.state


        for workorder in self:
            if workorder.date_finished:
                workorder.state = 'done'
            if workorder.state not in ('waiting', 'ready'):
                continue
            if workorder.production_id.reservation_state not in ('waiting', 'confirmed', 'assigned'):
                continue
            if workorder.production_id.reservation_state == 'assigned' and workorder.state == 'waiting':
                workorder.state = 'ready'
            elif workorder.production_id.reservation_state != 'assigned' and workorder.state == 'ready':
                workorder.state = 'waiting'

    # @api.onchange('date_finished')
    # def onchage_state(self):
    #     for rec in self:
    #         rec.state = 'done'

    @api.model
    def get_demarage_action(self):
        for rec in self:
            rec.demarage_action = False
            workorders = rec.env['mrp.workorder'].search([('production_id', '=', rec.production_id.id), ('id', '!=', rec._origin.id)])
            demarrage = True
            first = True
            list_work = []
            for workorder in workorders:
                _logger.info('***************************** rec.sequence %s', rec.sequence)
                _logger.info('***************************** workorder %s', workorder.sequence)
            #     if workorder:
            #         list_work.append(workorder)
            # for workorder in list_work:
                if rec.sequence > workorder.sequence:
                    first = False

                    _logger.info('***************************** logger 1 %s', first)
                    if workorder.state == 'progress':

                        demarrage = False
                        _logger.info('***************************** logger 2 %s', demarrage)
                    elif workorder.state == 'waiting':
                        demarrage = False



            if demarrage :
                rec.demarage_action = True
            if first :
                rec.demarage_action = True