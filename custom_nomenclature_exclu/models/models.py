# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

# class product_template(models.Model):
#     _inherit = 'product.template'
#
#     nomenclature_exclu_ids = fields.One2many('nomenclature.exclu', 'product_tmpl_id')
#     champ_test = fields.Boolean(compute='get_nomenclarue_exclu', store=True)
#
#     @api.depends('sale_ok')
#     def get_nomenclarue_exclu(self):
#         self.champ_test = True
#         for rec in self:
#             _logger.info('**************** model function')
#             liste_bom_ids = self.env['nomenclature.exclu'].search([('product_tmpl_id', '=', rec.id)])
#             if liste_bom_ids:
#                 for element in liste_bom_ids:
#                     _logger.info(f"Attempting to delete record with ID {element.id}")
#                     try:
#                         _logger.info('**************** try %s', element)
#                         if element.exists():
#                             _logger.info('**************** element.exists() %s %s', element, element.exists())
#                             _logger.info('**************** element.unlink() %s', element.unlink())
#                             element.unlink()
#                             rec.env.cr.commit() # Commit the transaction _logger.info(f"Successfully deleted record with ID {element.id}")
#
#                         else: _logger.warning(f"Record with ID {element.id} does not exist.")
#                     except Exception as e:
#                         _logger.error(f"Error while deleting record with ID {element.id}: {e}")
#
#             boms = rec.env['mrp.bom'].search(
#                 [('product_tmpl_id', '=', rec.id)])
#             _logger.info('**************** boms %s', boms)
#             if boms:
#                 list_products = []
#                 for bom in boms:
#
#                     for line in bom.bom_line_ids:
#                         if line:
#                             list_products.append(line.product_id.id)
#                             products = rec.env['product.product'].search([('id', 'not in', list_products)])
#                             if products:
#                                 for product in products:
#                                     nomenclature_exclu = rec.env['nomenclature.exclu'].create({
#                                         'product_id': product.id,
#                                         'product_tmpl_id': bom.product_tmpl_id.id,
#                                     })
#                                     _logger.info('**************** nomenclature_exclu %s', nomenclature_exclu)
#
#             rec.champ_test = True
#
# class nomenclature_exclu(models.Model):
#     _name = 'nomenclature.exclu'
#
#
#     product_id = fields.Many2one('product.product')
#     product_tmpl_id = fields.Many2one('product.template')