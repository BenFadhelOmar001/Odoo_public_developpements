# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource
from odoo.addons import decimal_precision as dp
from odoo import exceptions
import logging
_logger = logging.getLogger(__name__)


class liste_sale_order(models.Model):
    _name = "liste.sale.order"

    bom_id = fields.Many2one('mrp.bom')
    order_id = fields.Many2one('sale.order')

    def open_sale_order(self):
        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        action['views'] = [
            (self.env.ref('sale.view_order_form').id, 'form'),

        ]
        action['res_id'] = self.order_id.id
        return action

class liste_mrp_bom(models.Model):
    _name = "liste.mrp.bom"

    order_id = fields.Many2one('sale.order')
    bom_id = fields.Many2one('mrp.bom')
    code = fields.Char(related='bom_id.code')

    def open_mrp_bom(self):
        action = self.env.ref('mrp.mrp_bom_form_action').read()[0]
        action['views'] = [
            (self.env.ref('mrp.mrp_bom_form_view').id, 'form'),

        ]
        action['res_id'] = self.bom_id.id
        return action

class sale_order(models.Model):
    _inherit = "sale.order"

    liste_bom_ids = fields.One2many('liste.mrp.bom', 'order_id')


class mrp_bom(models.Model):
    _inherit = "mrp.bom"

    liste_order_ids = fields.One2many('liste.sale.order', 'bom_id')

    def action_liste_sale_order_tree_view_readonly(self):
        action = self.env.ref('custom_liste_nomenclature_devis.menu_liste_sale_order_action').read()[0]
        action['views'] = [
            (self.env.ref('custom_liste_nomenclature_devis.view_liste_sale_order_tree').id, 'tree'),

        ]

        #action['context'] = {'search_default_group_date_malle': 1}
        action['domain'] = [('bom_id', 'in', self.ids)]
        return action


class sale_order_line(models.Model):
    _inherit = "sale.order"

    def action_liste_mrp_bom_tree_view_readonly(self):
        action = self.env.ref('custom_liste_nomenclature_devis.menu_liste_mrp_action').read()[0]
        action['views'] = [
            (self.env.ref('custom_liste_nomenclature_devis.view_liste_mrp_bom_tree').id, 'tree'),

        ]

        #action['context'] = {'search_default_group_date_malle': 1}
        action['domain'] = [('order_id', 'in', self.ids)]
        return action

class sale_order_line(models.Model):
    _inherit = "sale.order.line"

    champ_test = fields.Boolean(compute='set_bom_ids_in_order', store=True)



    @api.depends('order_id', 'product_id')
    def set_bom_ids_in_order(self):
        self.champ_test = True

        for rec in self:
            liste_bom_ids = self.env['liste.mrp.bom'].search([('order_id', '=', rec.order_id._origin.id)])
            if liste_bom_ids:
                for element in liste_bom_ids:
                    _logger.info(f"Attempting to delete record with ID {element.id}")
                    try:
                        _logger.info('**************** try %s', element)
                        if element.exists():
                            _logger.info('**************** element.exists() %s %s', element, element.exists())
                            _logger.info('**************** element.unlink() %s', element.unlink())
                            element.unlink()
                            rec.env.cr.commit() # Commit the transaction _logger.info(f"Successfully deleted record with ID {element.id}")

                        else: _logger.warning(f"Record with ID {element.id} does not exist.")
                    except Exception as e:
                        _logger.error(f"Error while deleting record with ID {element.id}: {e}")
                # rec.env.cr.execute("DELETE FROM liste_mrp_bom WHERE order_id = %s", (rec.order_id._origin.id,))
                # rec.env.cr.commit()
            lines = rec.env['sale.order.line'].search([('product_id', '=', rec.product_id.id), ('order_id', '=', rec.order_id._origin.id)])
            for line in lines:
                for bom in line.product_id.bom_ids:

                    liste_mrp = rec.env['liste.mrp.bom'].create({
                        'bom_id': bom.id,
                        'order_id': rec.order_id._origin.id,
                    })
                    bom_id = rec.env['mrp.bom'].search([('id', '=', bom.id)])
                    if bom_id:
                        # liste_order_ids = rec.env['liste.sale.order'].search([('bom_id', '=', bom_id.id)])
                        # if liste_order_ids:
                        #     for element in liste_order_ids:
                        #         _logger.info(f"Attempting to delete record with ID {element.id}")
                        #         try:
                        #             _logger.info('**************** try %s', element)
                        #             if element.exists():
                        #                 _logger.info('**************** element.exists() %s %s', element,
                        #                              element.exists())
                        #                 _logger.info('**************** element.unlink() %s', element.unlink())
                        #                 element.unlink()
                        #                 rec.env.cr.commit()  # Commit the transaction _logger.info(f"Successfully deleted record with ID {element.id}")
                        #
                        #             else:
                        #                 _logger.warning(f"Record with ID {element.id} does not exist.")
                        #         except Exception as e:
                        #             _logger.error(f"Error while deleting record with ID {element.id}: {e}")
                        liste_order = rec.env['liste.sale.order'].create({
                            'bom_id': bom_id.id,
                            'order_id': rec.order_id._origin.id,
                        })

            rec.champ_test = True


