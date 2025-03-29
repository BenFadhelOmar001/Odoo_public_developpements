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

import logging

_logger = logging.getLogger(__name__)


class PrestataireController(http.Controller):




    @http.route('/helpdesk/prestataire/<int:ticket_id>', type='http', auth='user', website=True)
    def get_prestataire_form_for_given_ticket_id_url(self,ticket_id):

        _logger.info('*********** call controller ticket id %s', ticket_id)

        _logger.info('*********** request.session.uid %s', request.session.uid)


        



        access_for_numero_de_mobile = False
        access_for_code_sim = False
        access_for_numero_de_ligne_fixe = False
        access_for_adresse_mail = False
        access_for_mot_de_passe_windows = False
        access_for_commentaires_prestataires = False

        curent_user = request.env['res.users'].sudo().search([('id', '=',request.session.uid )])
        if curent_user:
            access_for_numero_de_mobile = curent_user.access_for_numero_de_mobile
            access_for_code_sim = curent_user.access_for_code_sim
            access_for_numero_de_ligne_fixe = curent_user.access_for_numero_de_ligne_fixe
            access_for_adresse_mail = curent_user.access_for_adresse_mail
            access_for_mot_de_passe_windows = curent_user.access_for_mot_de_passe_windows
            access_for_commentaires_prestataires = curent_user.access_for_commentaires_prestataires



        _logger.info('*********** curent_user %s', curent_user)

        the_ticket = request.env['helpdesk.ticket'].sudo().search([('id', '=',ticket_id )])

        _logger.info('*********** the_ticket %s', the_ticket)

        return http.request.render('custom_helpdesk_website.prestataire_form', {'access_for_numero_de_mobile' : access_for_numero_de_mobile,
                                                                                'access_for_code_sim' : access_for_code_sim,
                                                                                'access_for_numero_de_ligne_fixe' : access_for_numero_de_ligne_fixe,
                                                                                'access_for_adresse_mail' :access_for_adresse_mail,
                                                                                'access_for_mot_de_passe_windows' :access_for_mot_de_passe_windows,
                                                                                'access_for_commentaires_prestataires' : access_for_commentaires_prestataires,
                                                                                'the_ticket' : the_ticket,


                                                                                })




    @http.route(['/helpdesk/update_prestataire'], type='http', auth="user", website=True)
    def update_prestataire_form(self, **kw):
        
        _logger.info('++++++enter in update prestataire %s', kw)
        

        ticket = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['ticket_id'])])
        numero_de_mobile = ''
        code_sim = ''
        numero_de_ligne_fixe = ''
        adresse_mail = ''
        mot_de_passe_windows = ''
        commentaires_prestataires = ''
        
        if 'numero_de_mobile' in kw:
            numero_de_mobile = kw['numero_de_mobile']
            
        if 'code_sim' in kw:
            numero_de_mobile = kw['numero_de_mobile']

        if 'numero_de_ligne_fixe' in kw:
            numero_de_ligne_fixe = kw['numero_de_ligne_fixe']

        if 'adresse_mail' in kw:
            adresse_mail = kw['adresse_mail']

        if 'mot_de_passe_windows' in kw:
            mot_de_passe_windows = kw['mot_de_passe_windows']

        if 'commentaires_prestataires' in kw:
            commentaires_prestataires = kw['commentaires_prestataires']

        
        
        ticket.write({'numero_de_mobile': numero_de_mobile, 'code_sim': code_sim, 'numero_de_ligne_fixe': numero_de_ligne_fixe, 'adresse_mail': adresse_mail, 'mot_de_passe_windows': mot_de_passe_windows, 'commentaires_prestataires': commentaires_prestataires,})
        _logger.info('**************** %s', request.env.user)
        if request.env.user:
            return request.render("custom_helpdesk_website.prestataire_succes", {'ticket_id':ticket.id})
        else:
            return request.render("custom_helpdesk_website.not_user", {})






