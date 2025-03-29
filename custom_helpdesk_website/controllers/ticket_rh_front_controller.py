# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from operator import itemgetter

from markupsafe import Markup

from odoo import http
from odoo.exceptions import AccessError, MissingError, UserError
from odoo.http import request
from odoo.tools.translate import _
from odoo.tools import groupby as groupbyelem
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.osv.expression import OR, AND

from datetime import datetime
from datetime import date

import base64

import logging

_logger = logging.getLogger(__name__)


class TicketRhFrontController(http.Controller):


    @http.route(['/ticket_rh/form_new'], type='http', auth="user", website=True)
    def ticket_rh_form_new(self, **kw):

        
        _logger.info('++++++enter ticket rh form new%s', kw)
        if request.session.uid:
            

            return http.request.render('custom_helpdesk_website.ticket_rh_form_new', {'user_form_id': request.env.user.id,'current_date': date.today(),})

        else:
            return request.render("custom_helpdesk_website.not_user", {})


    @http.route(['/ticket_rh/save'], type='http', auth="user", website=True)
    def ticket_rh_save(self, **kw):

        
        _logger.info('++++++kw create ticket rh %s', kw)

        if request.session.uid:

            ticket_rh_team = request.env['helpdesk.team'].sudo().search([('equipe', '=','support_rh')], limit=1)
            stage_traitement_manager = request.env['helpdesk.stage'].sudo().search([('etape', '=','traitement_manager')], limit=1)

            if kw['x_studio_date_de_naissance']:
                kw_x_studio_date_de_naissance = datetime.strptime(kw['x_studio_date_de_naissance'], '%Y-%m-%d').date()
            else:
                kw_x_studio_date_de_naissance = False

            if kw['x_studio_date_de_cration']:
                kw_x_studio_date_de_cration = datetime.strptime(kw['x_studio_date_de_cration'], '%Y-%m-%d').date()
            else:
                kw_x_studio_date_de_cration = False

            if kw['x_studio_date_darrive']:
                kw_x_studio_date_darrive = datetime.strptime(kw['x_studio_date_darrive'], '%Y-%m-%d').date()
            else:
                kw_x_studio_date_darrive = False

            if kw['x_studio_date_de_depart']:
                kw_x_studio_date_de_depart = datetime.strptime(kw['x_studio_date_de_depart'], '%Y-%m-%d').date()
            else:
                kw_x_studio_date_de_depart = False

            if kw['personne_remplace']:
                kw_personne_remplace = kw['personne_remplace']
            else:
                kw_personne_remplace = False

            new_ticket_rh = request.env['helpdesk.ticket'].sudo().create({

                                    'team_id': ticket_rh_team.id,
                                    'stage_id': stage_traitement_manager.id,

                                    'name': kw['name'],
                                    'partner_id': int(kw['partner_id']),
                                    'partner_email': kw['partner_email'],


                                    'x_studio_type_de_recrutement': kw['x_studio_type_de_recrutement'],
                                    'x_studio_type_de_contrat': kw['x_studio_type_de_contrat'],
                                    'personne_remplace': kw_personne_remplace,
                
                                    'x_studio_matricule': kw['x_studio_matricule'],
                                    'x_studio_centre_de_cot': kw['x_studio_centre_de_cot'],
                                    'x_studio_site_de_rattachement': kw['x_studio_site_de_rattachement'],
                                    'x_studio_direction': kw['x_studio_direction'],
                                    'x_studio_type_de_fontion': kw['x_studio_type_de_fontion'],

                                    'x_studio_civilit_1': kw['x_studio_civilit_1'],
                                    'x_studio_nom_2': kw['x_studio_nom_2'],
                                    'x_studio_prnom': kw['x_studio_prnom'],
                                    'x_studio_date_de_naissance': kw_x_studio_date_de_naissance,
                                    'x_studio_date_adresse_1': kw['x_studio_date_adresse_1'],
                                    'num_professionnel': kw['num_professionnel'],
                                    'x_studio_date_de_cration': kw_x_studio_date_de_cration,
                                    'x_studio_date_darrive': kw_x_studio_date_darrive,
                                    'x_studio_date_de_depart': kw_x_studio_date_de_depart,

                                })
 
            _logger.info('**************** %s', request.env.user)
            if request.session.uid:
                return request.render("custom_helpdesk_website.ticket_rh_saved_succes", {'ticket_rh': new_ticket_rh,})
                
        else:
            return request.render("custom_helpdesk_website.not_user", {})

