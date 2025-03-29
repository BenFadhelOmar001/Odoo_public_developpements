# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError
from dateutil.parser import parse
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import logging

_logger = logging.getLogger(__name__)


class XlsxReport(models.AbstractModel):
    """Abstract Model for report template.
    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = "report.print_products_components.products_components_xlsx"
    _inherit = "report.report_xlsx.abstract"



    @api.model
    def generate_xlsx_report(self, workbook, data, cycle):

        # ids = data.get("ids", [])
        # docs = self.env["cycle.production"].browse(ids)

        sheet = workbook.add_worksheet('Rapport technique')
        title = workbook.add_format({'bold':True, 'align':'center','border':1, 'color':'black','valign': 'vcenter'})
        full_bordered_center_bold = workbook.add_format({'border': 1, 'color': 'black', 'align': 'center', 'bold': True})
        data_cell = workbook.add_format({'border': 1, 'color': 'black', 'align': 'center'})
        sheet.set_column(0, 0, 30)
        sheet.set_column(1, 15, 30)

        row = 0
        col = 0

        sheet.write(row,col, 'Bon commandes', full_bordered_center_bold)
        sheet.write(row,col+1, 'Composants', full_bordered_center_bold)
        sheet.write(row,col+2, 'Quantité', full_bordered_center_bold)


        row = 1
        col = 0
        i = 0
        for list_orders in data['form']['list_orders']:

            sheet.write(row, col, list_orders, data_cell)


            row += 1


        row = 1
        col = 1

        for list_bom_article in data['form']['list_bom_article']:
            sheet.write(row, col, list_bom_article, data_cell)


            row += 1


        row = 1
        col = 2


        for list_bom in data['form']['list_bom']:
            sheet.write(row, col, list_bom, data_cell)


            row += 1




        
        


        




                    
            

















