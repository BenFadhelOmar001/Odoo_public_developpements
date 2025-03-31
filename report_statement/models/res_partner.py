# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError



import logging
_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _inherit = "res.partner"



    def open_releve_partner_wiz(self):
        wizard = self.env['releve.partner.wiz'].create({'partner_id': self.id})

        return {
               'name': _('Releve'),
               'type': 'ir.actions.act_window',
               'res_model': 'releve.partner.wiz',
               'view_mode': 'form',
               'res_id': wizard.id,
               'target': 'new'
           }







    
    



