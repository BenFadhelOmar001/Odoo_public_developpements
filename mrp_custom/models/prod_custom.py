# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import float_round
from collections import defaultdict


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"
    _check_company_auto = True

    """
    Extends the 'maintenance.request' model to add additional fields and behavior.
    """
    production_id = fields.Many2one(
        'mrp.production', string='Manufacturing Order', check_company=True)
    workorder_id = fields.Many2one(
        'mrp.workorder', string='Work Order', check_company=True)
    production_company_id = fields.Many2one(string='Production Company', related='production_id.company_id')
    company_id = fields.Many2one(domain="[('id', '=?', lproduction_company_id)]")

class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"
    _check_company_auto = True

    """
    Extends the 'maintenance.equipment' model to add additional fields and behavior.
    """
    workcenter_id = fields.Many2one(
        'mrp.workcenter', string='Work Center', check_company=True)


    #Opens a form view for the associated work center when the 'Work Centers' button is clicked for the equipement.
    def button_mrp_workcenter(self):
        self.ensure_one()
        return {
            'name': ('work centers'),
            'view_mode': 'form',
            'res_model': 'mrp.workcenter',
            'view_id': self.env.ref('mrp.mrp_workcenter_view').id,
            'type': 'ir.actions.act_window',
            'res_id': self.workcenter_id.id,
            'context': {
                'default_company_id': self.company_id.id
            }
        }    

class MrpWorkcenter(models.Model):
    _inherit = "mrp.workcenter"

    equipment_ids = fields.One2many('maintenance.equipment', 'workcenter_id', string="Maintenance Equipment",check_company=True)


class ProdCustom(models.Model):
    _inherit = "mrp.production"

    maintenance_count = fields.Integer(compute='_compute_maintenance_count', string="Number of maintenance requests")
    request_ids = fields.One2many('maintenance.request', 'production_id')
    product_qty = fields.Float(
        'Quantity To Produce',
        default=1.0, digits='Product Unit of Measure',
        readonly=True, required=True, tracking=True,
        states={'confirmed': [('readonly', False)]})
    split_mo_count = fields.Integer(default=0, compute='_compute_split_count')
    
    # Compute the number of maintenance requests associated with a production order.
    @api.depends('request_ids')
    def _compute_maintenance_count(self):
        for production in self:
            production.maintenance_count = len(production.request_ids)

    # Open a form to create a new Maintenance Request associated with the production order.        
    def button_maintenance_req(self):
        self.ensure_one()
        return {
            'name': 'New Maintenance Request',
            'view_mode': 'form',
            'res_model': 'maintenance.request',
            'type': 'ir.actions.act_window',
            'context': {
                'default_company_id': self.company_id.id,
                'default_production_id': self.id,
            },
            'domain': [('production_id', '=', self.id)],
        }

    # Open a view displaying Maintenance Requests associated with the production order.
    def open_maintenance_request_mo(self):
        self.ensure_one()
        action = {
            'name': 'Maintenance Requests',
            'view_mode': 'kanban,tree,form,pivot,graph,calendar',
            'res_model': 'maintenance.request',
            'type': 'ir.actions.act_window',
            'context': {
                'default_company_id': self.company_id.id,
                'default_production_id': self.id,
            },
            'domain': [('production_id', '=', self.id)],
        }
        if self.maintenance_count == 1:
            production = self.env['maintenance.request'].search([('production_id', '=', self.id)])
            action['view_mode'] = 'kanban,tree'
            action['res_id'] = production.id
        return action

    # Create a new stock move based on an existing move with adjusted quantity.
    def _create_move_from_existing_move(self, move, factor, location_id, location_dest_id):
        return self.env['stock.move'].create({
            'name': move.name,
            'date': move.create_date,
            'product_id': move.product_id.id,
            'product_uom_qty': move.product_uom_qty * factor,
            'product_uom': move.product_uom.id,
            'procure_method': 'make_to_stock',
            'location_dest_id': location_dest_id.id,
            'location_id': location_id.id,
            'warehouse_id': location_dest_id.warehouse_id.id,
            'company_id': move.company_id.id,
        })

    # Cancel done production order and related stock moves
    def button_cancel(self):

        consume_moves = self.env['stock.move']
        produce_moves = self.env['stock.move']
        finished_moves = self.move_finished_ids.filtered(lambda move: move.state == 'done')
        factor = self.product_qty / self.product_uom_id._compute_quantity(self.product_qty, self.product_uom_id)
        for finished_move in finished_moves:
            consume_moves += self._create_move_from_existing_move(finished_move, factor, finished_move.location_dest_id,
                                                                  finished_move.location_id)

        if len(consume_moves):
            consume_moves._action_confirm()

        raw_moves = self.move_raw_ids.filtered(lambda move: move.state == 'done')
        factor = self.product_qty / self.product_uom_id._compute_quantity(self.product_qty, self.product_uom_id)

        for raw_move in raw_moves:
            produce_moves += self._create_move_from_existing_move(raw_move, factor, raw_move.location_dest_id,
                                                                  self.location_dest_id)

        produce_moves._action_confirm()

        finished_moves = consume_moves.filtered(lambda m: m.product_id == self.product_id)
        consume_moves -= finished_moves

        for finished_move in finished_moves:
            if finished_move.has_tracking != 'none':
                self.env['stock.move.line'].create({
                    'move_id': finished_move.id,
                    'qty_done': finished_move.product_uom_qty,
                    'product_id': finished_move.product_id.id,
                    'product_uom_id': finished_move.product_uom.id,
                    'location_id': finished_move.location_id.id,
                    'location_dest_id': finished_move.location_dest_id.id,
                })
            else:
                finished_move.quantity_done = finished_move.product_uom_qty

        qty_already_used = defaultdict(float)

        for move in produce_moves | consume_moves:
            if move.has_tracking != 'none':
                original_move = move in produce_moves and self.move_raw_ids or self.move_finished_ids
                original_move = original_move.filtered(lambda m: m.product_id == move.product_id)
                needed_quantity = move.product_uom_qty
                moves_lines = original_move.mapped('move_line_ids')

                for move_line in moves_lines:
                    taken_quantity = min(needed_quantity, move_line.qty_done - qty_already_used[move_line])

                    if taken_quantity:
                        self.env['stock.move.line'].create({
                            'move_id': move.id,
                            'lot_id': move_line.lot_id.id,
                            'qty_done': taken_quantity,
                            'product_id': move.product_id.id,
                            'product_uom_id': move_line.product_uom_id.id,
                            'location_id': move.location_id.id,
                            'location_dest_id': move.location_dest_id.id,
                        })
                        needed_quantity -= taken_quantity
                        qty_already_used[move_line] += taken_quantity
            else:
                move.quantity_done = float_round(move.product_uom_qty, precision_rounding=move.product_uom.rounding)

        finished_moves._action_done()
        consume_moves._action_done()
        produce_moves._action_done()
        produced_move_line_ids = produce_moves.mapped('move_line_ids').filtered(lambda ml: ml.qty_done > 0)
        consume_moves.mapped('move_line_ids').write({'produce_line_ids': [(6, 0, produced_move_line_ids.ids)]})

        raw_moves.sudo().write({'state': 'cancel'})
        raw_moves.mapped('move_line_ids').sudo().write({'state': 'cancel'})

        if self.sudo().mapped('workorder_ids'):
            self.sudo().mapped('workorder_ids').write({'state': 'cancel'})

        self.write({'state': 'cancel'})


    # split manufacturing order by number of qty/split
    def _compute_split_count(self):
        for data in self:
            count = 0
            mrp_obj = data.search([('origin', '=', data.name)])
            if mrp_obj:
                for mrp_id in mrp_obj:
                    count = count + 1

            data.split_mo_count = count

    def btn_split_mo(self):
        return {'type': 'ir.actions.act_window',
                'name': 'Diviser l\'ordre de fabarication',
                'res_model': 'split.mo.wizard',
                'target': 'new',
                'view_id': self.env.ref('mrp_custom.split_mo_wizard_view_form').id,
                'view_mode': 'form',
                'view_type': 'form',
                'context': {}
                }

    def list_split_orders(self):
        return {'type': 'ir.actions.act_window',
                'name': 'Split Manufacturing Orders',
                'res_model': 'mrp.production',
                'target': 'current',
                'view_id': self.env.ref('mrp.mrp_production_tree_view').id,
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': False,
                'context': False,
                'domain': [('origin', '=', self.name)]
                }


