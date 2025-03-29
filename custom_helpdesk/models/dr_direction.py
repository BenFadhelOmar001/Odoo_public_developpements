# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class dr_direction(models.Model):
    _name = 'dr.direction'

    name = fields.Char(string="Direction")
    metier_ids = fields.Many2many('dr.metier', string='Metiers', widget='many2many_tags')





