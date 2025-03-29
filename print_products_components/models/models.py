# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class res_company(models.Model):
    _inherit = "sale.order"

    def action_generate_components(self):
        list_bom_article = []
        list_orders = []
        list_bom = []
        selected_ids = self.env.context.get('active_ids', [])
        if selected_ids:


            orders = self.env['sale.order'].search([('id', 'in', selected_ids)])
            confirme = True
            for order in orders:
                if order.state != 'sale':
                    confirme = False
            if confirme:
                for order in orders:
                    _logger.info('************* order.name %s', order.name)
                    list_orders.append(order.name)
                    for line in order.order_line:
                        if line:
                            mrp_boms = self.env['mrp.bom'].search([('product_tmpl_id', '=', line.product_id.product_tmpl_id.id)])

                            if mrp_boms:
                                for mrp_bom in mrp_boms:
                                    for bom_line in mrp_bom.bom_line_ids:
                                        list_bom_article.append(bom_line.product_id.name)
                                        list_bom.append(bom_line.product_qty * mrp_bom.product_qty)
            else:
                raise ValidationError("Il faut que tous bons de commandes séléctionnés sont confirmés !!")

            _logger.info('list_orders %s, list_bom_article %s, list_bom %s', list_orders, list_bom_article, list_bom )
            data = {
                'ids': self.ids,
                'model': 'print.stock.wizard',
                'form': {
                    'list_orders': list_orders,
                    'list_bom_article': list_bom_article,
                    'list_bom': list_bom,

                }
            }
            return self.env.ref('print_products_components.components_report_xlsx').report_action(self, data=data)