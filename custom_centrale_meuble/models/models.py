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
    _name = "order.type"

    name = fields.Char(required=True)


class res_company(models.Model):
    _inherit = "sale.order"

    type = fields.Many2one('order.type')
    date_order = fields.Datetime(string='Date de la commande', readonly=False)

class res_company(models.Model):
    _inherit = "mrp.production"

    partner_id = fields.Many2one('res.partner')
