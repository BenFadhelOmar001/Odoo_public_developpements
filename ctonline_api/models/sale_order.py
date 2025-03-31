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
from dateutil.relativedelta import relativedelta

import time

import logging
_logger = logging.getLogger(__name__)


class sale_order(models.Model):
    _inherit = 'sale.order'

    def _get_ctonline_data(self, code_pts, start_date, end_date,x_api_key):

        url = f'https://api-public.servicectonline.fr/ctonline/center/{code_pts}/inspection/count'
        headers = {
            'accept': 'application/json',
            'X-API-KEY': x_api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            'startDate': start_date,
            'endDate': end_date
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
            data = response.json()
            
            if data.get('success'):
                _logger.info('+++ Succes :')
                _logger.info("Successfully retrieved data from CTonline for %s: %s", code_pts, data.get('item'))
                return data.get('item', 0)
            else:
                _logger.info('--- ERROR :')
                _logger.info("Failed to retrieve data from CTonline for %s. Messages: %s", code_pts, str(data.get('messages')))
                return False
                #raise UserError("Failed to retrieve data from CTonline: " + str(data.get('messages')))
        except requests.exceptions.RequestException as e:
            _logger.info('--- ERROR :')
            _logger.info("Error when calling CTonline API for %s: %s", code_pts, str(e))
            return False
            #raise UserError(f"Error when calling CTonline API: {str(e)}")
        




    def cronjob_subscriptions(self):
        start_time = time.time()

        _logger.info('++++++BEGIN TRANSACTION : calling cronjob_subscriptions')

        current_date = datetime.now()
        _logger.info('*** Curent calling Date : %s', current_date)

        x_api_key = self.env['ir.config_parameter'].sudo().get_param('ctonline_api.x_api_key')
        if x_api_key:


            previous_month_date = current_date - relativedelta(months=1)

            first_day_of_month = current_date.replace(day=1)
            last_day_of_month = datetime(current_date.year, current_date.month, calendar.monthrange(current_date.year, current_date.month)[1])


            first_day_of_previous_month = previous_month_date.replace(day=1)
            last_day_of_previous_month = previous_month_date.replace(day=calendar.monthrange(previous_month_date.year, previous_month_date.month)[1])

            _logger.info('*** Invoice date Intervals :')
            _logger.info('*** Start date %s', str(first_day_of_month.date()))
            _logger.info('*** End date %s', str(last_day_of_month.date()))

            _logger.info('*** API searching creterias date Intervals :')
            _logger.info('*** Start date %s', str(first_day_of_previous_month.date()))
            _logger.info('*** End date %s', str(last_day_of_previous_month.date()))

            subscription_records = self.env['sale.order'].search(['&', ('x_studio_abonnement_au_contrle', '=', True), ('next_invoice_date', '>=', str(first_day_of_month.date())), ('next_invoice_date', '<=', str(last_day_of_month.date()))])
            
            if subscription_records:
                _logger.info('+++ Subcriptions records for given intervals %s', subscription_records)
                is_controles_realises_product = self.env['product.template'].search([('is_controles_realises', '=', True)], limit=1)
                
                if is_controles_realises_product:
                    _logger.info('+++ Product as "Controles réalisés" %s', is_controles_realises_product)
                    _logger.info('+++ Product as "Controles réalisés" %s', is_controles_realises_product.id)

                    updated_subcriptions = []
                    non_updated_subcriptions = []

                    for sub in subscription_records:
                        update_subscription = False
                        _logger.info('+++ Subscription : %s  ID: %s', sub.name, sub)
                        _logger.info('+++ Partner : %s  ID: %s', sub.partner_id.name, sub.partner_id)

                        if sub.partner_id.ref:
                            _logger.info('+++ Code client : %s', sub.partner_id.ref)
                            response = self._get_ctonline_data(sub.partner_id.ref,str(first_day_of_previous_month.date()),str(last_day_of_previous_month.date()),x_api_key)
                            if response:
                                
                                _logger.info('+++ Api response items : %s', response)
                                for line in sub.order_line:
                                    _logger.info('******** line.product_template_id : %s', line.product_template_id)
                                    _logger.info('******** line.product_template_id.id : %s', line.product_template_id.id)
                                    if line.product_template_id.id == is_controles_realises_product.id:
                                        old_product_uom_qty = line.product_uom_qty
                                        old_price_unit = line.price_unit
                                        new_qty = 0
                                        if float(response) <= 60:
                                            new_qty = 60
                                            _logger.info('+++ Case <= 60 new quantity to update : %s', new_qty)
                                        else: 
                                            new_qty = float(response)
                                            _logger.info('+++ Case > 60 new quantity to update : %s', new_qty)

                                        line.sudo().write({'product_uom_qty': new_qty})
                                        line.sudo().write({'price_unit': old_price_unit})
                                        update_subscription = True
                                        
                                        _logger.info('*** New quantity : %s updated for line with ID : %s old quantity value : %s old price unit value rewrited %s', new_qty, line, old_product_uom_qty, old_price_unit )
                            

                        else:
                            _logger.info('--- Code client not defined for Partner : %s   with ID : %s', sub.partner_id.name, sub.partner_id)

                        if update_subscription == True:
                            updated_subcriptions.append(sub)

                        else:
                            non_updated_subcriptions.append(sub)

                    if updated_subcriptions:
                        _logger.info('+++ Updated subscription : %s   with TOTAL : %s', updated_subcriptions, len(updated_subcriptions))
                    if non_updated_subcriptions:
                        _logger.info('--- Non Updated subscription : %s   with TOTAL : %s', non_updated_subcriptions, len(non_updated_subcriptions))
                            
                    
                else:
                    _logger.info('--- No configured product as "Controles réalisés"')
            else:
                _logger.info('--- No subscriptions for given intervals')

        else:
            _logger.info('--- ERROR :')
            _logger.info("Should define CTonline X-API-KEY value in configuration ! ")
        _logger.info('++++++END TRANSACTION : calling cronjob_subscriptions')
        end_time = time.time()
        execution_duration = end_time - start_time
        _logger.info(f"***Transaction executed in {execution_duration:.4f} seconds")







        
    




