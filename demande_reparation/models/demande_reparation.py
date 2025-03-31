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

class product_service(models.Model):
    _inherit = "product.product"

    reparation_id = fields.Many2one('demande.reparation')


class demande_reparation(models.Model):
    _name = "demande.reparation"

    fournisseur_id = fields.Many2one('res.partner')
    product_ids = fields.Many2one('product.product', 'reparation_id')




