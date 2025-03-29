# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class dr_metier(models.Model):
    _name = 'dr.metier'

    name = fields.Char(string="Metier")
    is_commerce = fields.Boolean(string="Commerce ?")
    is_autre = fields.Boolean(string="Autre ?")



    @api.model
    def get_metiers_by_direction(self, direction):
        if not direction:
            #_logger.info('------- not direction')
            return []

        try:
            # Use sudo to bypass access rights
            direction_record = request.env['dr.direction'].sudo().search([('id', '=',int(direction))], limit=1)
            #_logger.info('++++++direction_record%s', direction_record)
            #_logger.info('++++++direction_record.metier_ids%s', direction_record.metier_ids)
            return self.sudo().search_read([('id', 'in', direction_record.metier_ids.ids)], ['id', 'name'])
        except Exception as e:
            _logger.error(f"Error fetching metiers by direction: {e}")
            return []


