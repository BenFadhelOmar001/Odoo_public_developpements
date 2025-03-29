# -*- coding: utf-8 -*-


from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)
class JournalAccount(models.Model):
    _inherit = "mrp.production"

    ref_bom = fields.Char(compute='get_ref_bom', store=True)

    @api.depends('bom_id')
    def get_ref_bom(self):
        for rec in self:
            if rec.bom_id.code:
                rec.ref_bom = rec.bom_id.code
            else:
                rec.ref_bom = ''
