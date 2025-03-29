# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from datetime import date
import logging

_logger = logging.getLogger(__name__)



class ResContryInherit(models.Model):
    _inherit = "product.category"

    ref_sequence = fields.Char(limit=4)
    code = fields.Char()

class ProductProductInherit(models.Model):
    _inherit = "product.template"

    @api.onchange('categ_id')
    def get_default_code(self):
        for rec in self:
            # rec.default_code = ''
            if rec.categ_id.ref_sequence:
                sequence_list = list(str(rec.categ_id.ref_sequence))

                if rec.categ_id.parent_id.code:
                    rec.default_code = rec.categ_id.parent_id.code + rec.categ_id.code + rec.categ_id.ref_sequence
                elif rec.categ_id.code:
                    rec.default_code = rec.categ_id.code + rec.categ_id.ref_sequence

                

class ProductProductInherit(models.Model):
    _inherit = "product.product"

    #default_code = fields.Char('Référence interne', readonly=False)

    @api.model_create_multi
    def create(self, vals_list):
        _logger.info('**************************** tessssssssssst 2 %s', self)
        for vals in vals_list:
            self.product_tmpl_id._sanitize_vals(vals)

        products = super(ProductProductInherit, self.with_context(create_product_product=True)).create(vals_list)
        # `_get_variant_id_for_combination` depends on existing variants
        self.clear_caches()
        for rec in products:
            _logger.info('**************************** tessssssssssst 1')
            if rec.categ_id.ref_sequence:
                sequence_list = list(str(rec.categ_id.ref_sequence))

                if rec.categ_id.parent_id.code:
                    rec.default_code = rec.categ_id.parent_id.code + rec.categ_id.code + rec.categ_id.ref_sequence
                elif rec.categ_id.code:
                    rec.default_code = rec.categ_id.code + rec.categ_id.ref_sequence

                sequence_list = list(rec.categ_id.ref_sequence)
                num = ''
                i = len(sequence_list)
                j = 0
                bool = True
                _logger.info('******************** sequence_list %s', sequence_list)
                while j < i:
                    _logger.info('******************** sequence_list[j] %s', sequence_list[j])
                    if sequence_list[j] == '9' :
                        if j == len(sequence_list) - 1:
                            bool = False
                            sequence_list[j - 1] = str(int(sequence_list[j - 1]) + 1)
                            sequence_list[j] = 0
                            _logger.info('******************** on est ici 1')
                        elif j == len(sequence_list) - 2 and sequence_list[j + 1] == '9':
                            bool = False
                            sequence_list[j - 2] = str(int(sequence_list[j - 1]) + 1)
                            sequence_list[j-1] = 0
                            _logger.info('******************** on est ici 2')
                        elif j == len(sequence_list) - 3 and sequence_list[j + 2] == '9':
                            bool = False
                            sequence_list[j - 3] = str(int(sequence_list[j - 2]) + 1)
                            sequence_list[j-2] = 0
                            _logger.info('******************** on est ici 3')
                    j += 1
                if bool:
                    _logger.info('**************************** tessssssssssst')
                    sequence_list[len(sequence_list) - 1] = str(int(sequence_list[len(sequence_list) - 1]) + 1)

                num = ''
                for n in sequence_list:
                    num += str(n)

                categorie = rec.env['product.category'].search([('id', '=', rec.categ_id.id)])
                categorie.write({'ref_sequence': num})
                rec.categ_id.ref_sequence = num
            else:
                _logger.info('******************** nottttt sequence_list ')
        _logger.info('**************************** tessssssssssst 3 %s', products)


        return products

    # @api.onchange('categ_id')
    # def get_default_code(self):
    #     for rec in self:
    #         #rec.default_code = ''
    #         if rec.categ_id.ref_sequence:
    #             sequence_list = list(str(rec.categ_id.ref_sequence))
    #
    #             if rec.categ_id.parent_id:
    #                 rec.default_code = rec.categ_id.parent_id.name + rec.categ_id.name + rec.categ_id.ref_sequence
    #                 rec.product_tmpl_id.default_code = rec.categ_id.parent_id.name + rec.categ_id.name + rec.categ_id.ref_sequence
    #             else:
    #                 rec.default_code = rec.categ_id.name + rec.categ_id.ref_sequence
    #                 rec.product_tmpl_id.default_code = rec.categ_id.name + rec.categ_id.ref_sequence
    #
    #             sequence_list = list(rec.categ_id.ref_sequence)
    #             num = ''
    #             i= len(sequence_list)
    #             j=0
    #             bool = True
    #             while j < i:
    #                 if sequence_list[j] =='9':
    #                     bool = False
    #                     sequence_list[j-1] = str(int(sequence_list[j-1]) + 1)
    #                     sequence_list[j] = 0
    #                 j += 1
    #             if bool:
    #                 _logger.info('**************************** tessssssssssst')
    #                 sequence_list[len(sequence_list) - 1] = str(int(sequence_list[len(sequence_list) - 1]) + 1)
    #
    #             num = ''
    #             for n in sequence_list:
    #                 num += str(n)
    #
    #
    #             rec.categ_id.ref_sequence = num



    


