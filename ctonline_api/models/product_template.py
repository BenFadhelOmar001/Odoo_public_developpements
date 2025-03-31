# -*- coding: utf-8 -*-

import base64
from datetime import datetime, timedelta

from odoo import models, fields, api, _
from odoo.exceptions import RedirectWarning, ValidationError, UserError
from odoo.tools import SQL, format_date

import json
import requests

from datetime import datetime
import calendar

import logging
_logger = logging.getLogger(__name__)


class product_template(models.Model):
    _inherit = 'product.template'

    is_controles_realises = fields.Boolean()


        
    




