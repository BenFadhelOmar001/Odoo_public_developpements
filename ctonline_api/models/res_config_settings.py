# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import logging

import time
from datetime import datetime
from datetime import time as datetime_time
from dateutil import relativedelta

import babel

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)


class res_config_settings(models.TransientModel):
    _inherit = "res.config.settings"


    x_api_key = fields.Char(config_parameter="ctonline_api.x_api_key", string="X-API-KEY")




    



