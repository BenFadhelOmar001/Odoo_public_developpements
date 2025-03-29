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
    _inherit = "mrp.workorder"

    employee_id = fields.Many2one('hr.employee', store=True)

    current_user_id = fields.Many2one('res.users', string='Current User', compute='_compute_current_user')

    @api.model
    def _compute_current_user(self):
        for record in self:
            record.current_user_id = self.env.user.id

    current_employee_id = fields.Many2one('hr.employee', string='Current Employé', compute='_compute_current_employee')
    is_user = fields.Boolean(compute='_compute_current_employee', store=True)

    @api.depends('current_user_id')
    def _compute_current_employee(self):
        for record in self:
            employe = record.env['hr.employee'].search([('user_id', '=', record.current_user_id.id)], limit=1)
            if employe:
                record.current_employee_id = employe.id
            if record.employee_id == record.current_employee_id:
                record.is_user = True
            else:
                record.is_user = False