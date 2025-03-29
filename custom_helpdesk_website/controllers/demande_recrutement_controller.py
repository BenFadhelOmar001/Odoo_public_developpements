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
import os

import logging

_logger = logging.getLogger(__name__)


class DemandeRecrutementController(http.Controller):





    @http.route(['/demande_recrutement/form_new'], type='http', auth="user", website=True)
    def demande_recrutement_form_new(self, **kw):

        
        _logger.info('++++++enter demande recrutement form new%s', kw)
        if request.session.uid:
            if request.env.user.group_demande_recrutement_demandeur:

                sujet = 'Demande de recrutement '+request.env.user.name


                return http.request.render('custom_helpdesk_website.demande_recrutement_form_new', {'demandeur_id': request.env.user.id,
                                                                                        'nom_du_demandeur_a_afficher': request.env.user.name,
                                                                                        'date_de_creation_a_afficher': date.today(),
                                                                                        'sujet': sujet,

                                                                                        })
            else:
                return request.render("http_routing.403", {})

        else:
            return request.render("custom_helpdesk_website.not_user", {})


    @http.route(['/demande_recrutement/save'], type='http', auth="user", website=True)
    def demende_recrutement_save(self, **kw):



        
        _logger.info('++++++kw create %s', kw)

        # _logger.info('*****env user %s', request.env.user)
        # _logger.info('*****env user.id %s', request.env.user.id)
        # _logger.info('*****env user.name %s', request.env.user.name)
        # _logger.info('*****session %s', request.session.uid)
        if request.session.uid:

            demande_recrutement_team = request.env['helpdesk.team'].sudo().search([('equipe', '=','demande_recrutement')], limit=1)
            stage_demande = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_demande')], limit=1)
            demandeur_user = request.env['res.users'].sudo().search([('id', '=',int(kw['demandeur_id']))])

            if kw['poste_a_choisir_autre']:

                kw_poste_a_choisir_autre = kw['poste_a_choisir_autre']
            else:

                kw_poste_a_choisir_autre = False

            if kw['direction_a_choisir_id']:

                kw_direction_a_choisir_id = int(kw['direction_a_choisir_id'])
            else:

                kw_direction_a_choisir_id = False

            if kw['metier_a_choisir_id']:

                kw_metier_a_choisir_id = int(kw['metier_a_choisir_id'])
            else:

                kw_metier_a_choisir_id = False

            if kw['manager_recrutement']:

                kw_manager_recrutement = int(kw['manager_recrutement'])
            else:

                kw_manager_recrutement = False

            if kw['poste_a_choisir']:

                kw_poste_a_choisir = int(kw['poste_a_choisir'])
            else:

                kw_poste_a_choisir = False

            if kw['date_de_debut_souhaite']:
                kw_date_de_debut_souhaite = datetime.strptime(kw['date_de_debut_souhaite'], '%Y-%m-%d').date()
            else:
                kw_date_de_debut_souhaite = False

            if kw['date_de_debut']:
                kw_date_de_debut = datetime.strptime(kw['date_de_debut'], '%Y-%m-%d').date()
            else:
                kw_date_de_debut= False

            if kw['date_de_fin']:
                kw_date_de_fin = datetime.strptime(kw['date_de_fin'], '%Y-%m-%d').date()
            else:
                kw_date_de_fin = False



            

            new_demande_recrutement = request.env['helpdesk.ticket'].sudo().create({
                                    'team_id': demande_recrutement_team.id,
                                    'stage_id': stage_demande.id,
                                    'date_de_creation_a_afficher': date.today(),
                                    'name': kw['name'],
                                    'partner_id': demandeur_user.partner_id.id,
                                    'manager_recrutement': kw_manager_recrutement,
                                    'etablissement': kw['etablissement'],
                                    'rrh': kw['rrh'],
                                    'direction_a_choisir_id': kw_direction_a_choisir_id,
                                    'metier_a_choisir_id': kw_metier_a_choisir_id,
                                    'poste_a_choisir': kw_poste_a_choisir,
                                    'poste_a_choisir_autre': kw_poste_a_choisir_autre,
                                    'commentaire_demandeur': kw['commentaire_demandeur'],
                                    'motif_de_recrutement': kw['motif_de_recrutement'],
                                    'si_remplacement_qui': kw['si_remplacement_qui'],
                                    'type_contrat': kw['type_contrat'],

                                    'date_de_debut_souhaite': kw_date_de_debut_souhaite,
                                    'date_de_debut': kw_date_de_debut,
                                    'date_de_fin': kw_date_de_fin,

                                    'missions_principales': kw['missions_principales'],

                                    'secteur_geographique': kw['secteur_geographique'],
                                    'specificite_clients': kw['specificite_clients'],
                                    'lieu_habitation_souhaite': kw['lieu_habitation_souhaite'],
                                    
                                    'chiffre_affaires_du_secteur_actuel': kw['chiffre_affaires_du_secteur_actuel'],
                                    'evaluation_remuneration_annuelle_actuel': kw['evaluation_remuneration_annuelle_actuel'],
                                    'garantie_de_salaire_actuel': kw['garantie_de_salaire_actuel'],
                                    'nombre_de_clients_actuel': kw['nombre_de_clients_actuel'],
                                    'panier_moyen_actuel': kw['panier_moyen_actuel'],
                                    
                                    'chiffre_affaires_du_secteur_vise': kw['chiffre_affaires_du_secteur_vise'],
                                    'evaluation_remuneration_annuelle_vise': kw['evaluation_remuneration_annuelle_vise'],
                                    'garantie_de_salaire_vise': kw['garantie_de_salaire_vise'],
                                    'nombre_de_clients_vise': kw['nombre_de_clients_vise'],
                                    'panier_moyen_vise': kw['panier_moyen_vise']

                                })

            demande_recrutement_base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            demande_recrutement_base_url += '/demande_recrutement/form_access/%s' % (new_demande_recrutement.id)
            new_demande_recrutement.demande_recrutement_link = demande_recrutement_base_url

            files = request.httprequest.files.getlist('upload_files')

            _logger.info('---- files %s', files)

            attachments = []
            for file in files:
                if file and file.filename:

                    file_data = file.read()
                    attachment = request.env['ir.attachment'].sudo().create({
                        'name': file.filename,
                        'datas': base64.b64encode(file_data),
                        'type': 'binary',
                        'res_model': 'helpdesk.ticket', 
                        'res_id': new_demande_recrutement.id,  
                    })
                    attachments.append(attachment)

            



            
            _logger.info('**************** %s', request.env.user)
            if request.session.uid:
                return request.render("custom_helpdesk_website.demande_recrutement_saved_succes", {'demande_recrutement': new_demande_recrutement,'current_user_group': 'demandeur',})

                
        else:
            return request.render("custom_helpdesk_website.not_user", {})



    @http.route(['/demande_recrutement/confirm'], type='http', auth="user", website=True)
    def demande_recrutement_confirm(self, **kw):
        
        _logger.info('++++++enter in confirm %s', kw)

        if request.session.uid:
            if request.env.user.group_demande_recrutement_demandeur:


                stage_traitement_rrh = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_traitemnt_rrh')], limit=1)

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])


                demande_recrutement.write({'stage_id': stage_traitement_rrh.id,})

                demande_recrutement_mail_template = request.env.ref('custom_helpdesk.email_template_demande_recrutement_rrh_link')

                user_rrh = request.env['res.users'].sudo().search([('name', '=',demande_recrutement.rrh)], limit=1)

                mail_context = {

                    'email_to': user_rrh.partner_id.email,
                }

                demande_recrutement_mail_template.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                
                return request.render("custom_helpdesk_website.demande_recrutement_confirmed_succes", {'demande_recrutement': demande_recrutement,})
        

        
                

            else:
                return request.render("http_routing.403", {})

        else:
            return request.render("custom_helpdesk_website.not_user", {})




    @http.route(['/demande_recrutement/form/<int:demande_recrutement_id>'], type='http', auth="user", website=True)
    def demande_recrutement_form(self,demande_recrutement_id):

        _logger.info('*********** call demande_recrutement_form *****%s', demande_recrutement_id)

        if request.session.uid:

            demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=',demande_recrutement_id)])

            if demande_recrutement:
                demande_recrutement_team = request.env['helpdesk.team'].sudo().search([('equipe', '=','demande_recrutement')], limit=1)

                if demande_recrutement.team_id.id == demande_recrutement_team.id:

                    if request.env.user.demande_recrutement_session == 'demandeur':

                        return http.request.render('custom_helpdesk_website.demande_recrutement_form_demandeur', {'demande_recrutement': demande_recrutement,})

                    if request.env.user.demande_recrutement_session == 'rrh':

                        return http.request.render('custom_helpdesk_website.demande_recrutement_form_rrh', {'demande_recrutement': demande_recrutement,})

                    if request.env.user.demande_recrutement_session == 'rdrh':

                        return http.request.render('custom_helpdesk_website.demande_recrutement_form_rdrh', {'demande_recrutement': demande_recrutement,})

                    if request.env.user.demande_recrutement_session == 'direction':

                        return http.request.render('custom_helpdesk_website.demande_recrutement_form_direction', {'demande_recrutement': demande_recrutement,})

                    if request.env.user.demande_recrutement_session == 'drh':

                        return http.request.render('custom_helpdesk_website.demande_recrutement_form_drh', {'demande_recrutement': demande_recrutement,})

                                                                                                    





            
        else:
            return request.render("custom_helpdesk_website.not_user", {})







                                                                                
        

        
        
        #demande_recrutemet.write({'numero_de_mobile': numero_de_mobile, 'code_sim': code_sim, 'numero_de_ligne_fixe': numero_de_ligne_fixe, 'adresse_mail': adresse_mail, 'mot_de_passe_windows': mot_de_passe_windows, 'commentaires_prestataires': commentaires_prestataires,})
        # _logger.info('**************** %s', request.env.user)
        # if request.env.user:
        #     return request.render("demande_recrutement.demande_recrutement_succes", {'demande_recrutement_id':demande_recrutemet.id})
        # else:
        #     return request.render("demande_recrutement.not_user", {})




    @http.route(['/demande_recrutement/update'], type='http', auth="user", website=True)
    def demende_recrutement_update(self, **kw):

        _logger.info('++++++kw update %s', kw)
        _logger.info('*****env user %s', request.env.user)
        _logger.info('*****env user.id %s', request.env.user.id)
        _logger.info('*****env user.name %s', request.env.user.name)
        _logger.info('*****session %s', request.session.uid)

        if request.session.uid:


            


            if request.env.user.demande_recrutement_session == 'rrh':

                if kw['poste_a_choisir_autre']:

                    kw_poste_a_choisir_autre = kw['poste_a_choisir_autre']
                else:

                    kw_poste_a_choisir_autre = False

                if kw['direction_a_choisir_id']:

                    kw_direction_a_choisir_id = int(kw['direction_a_choisir_id'])
                else:

                    kw_direction_a_choisir_id = False

                if kw['metier_a_choisir_id']:

                    kw_metier_a_choisir_id = int(kw['metier_a_choisir_id'])
                else:

                    kw_metier_a_choisir_id = False

                if kw['manager_recrutement']:

                    kw_manager_recrutement = int(kw['manager_recrutement'])
                else:

                    kw_manager_recrutement = False

                if kw['poste_a_choisir']:

                    kw_poste_a_choisir = int(kw['poste_a_choisir'])
                else:
                    kw_poste_a_choisir = False
                    
                if kw['date_de_debut_souhaite']:
                    kw_date_de_debut_souhaite = datetime.strptime(kw['date_de_debut_souhaite'], '%Y-%m-%d').date()
                else:
                    kw_date_de_debut_souhaite = False
                if kw['date_de_debut']:
                    kw_date_de_debut = datetime.strptime(kw['date_de_debut'], '%Y-%m-%d').date()
                else:
                    kw_date_de_debut= False
                if kw['date_de_fin']:
                    kw_date_de_fin = datetime.strptime(kw['date_de_fin'], '%Y-%m-%d').date()
                else:
                    kw_date_de_fin = False

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])

                demande_recrutement.sudo().write({

                                        'manager_recrutement': kw_manager_recrutement,
                                        'etablissement': kw['etablissement'],
                                        'rrh': kw['rrh'],
                                        'direction_a_choisir_id': kw_direction_a_choisir_id,
                                        'metier_a_choisir_id': kw_metier_a_choisir_id,
                                        'poste_a_choisir': kw_poste_a_choisir,
                                        'poste_a_choisir_autre': kw_poste_a_choisir_autre,
                                        'commentaire_demandeur': kw['commentaire_demandeur'],
                                        'motif_de_recrutement': kw['motif_de_recrutement'],
                                        'si_remplacement_qui': kw['si_remplacement_qui'],
                                        'type_contrat': kw['type_contrat'],
                                        'date_de_debut_souhaite': kw['date_de_debut_souhaite'],
                                        'date_de_debut': kw['date_de_debut'],
                                        'date_de_fin': kw['date_de_fin'],
                                        'missions_principales': kw['missions_principales'],
                                        'secteur_geographique': kw['secteur_geographique'],
                                        'specificite_clients': kw['specificite_clients'],
                                        'lieu_habitation_souhaite': kw['lieu_habitation_souhaite'],

                                        'chiffre_affaires_du_secteur_actuel': kw['chiffre_affaires_du_secteur_actuel'],
                                        'evaluation_remuneration_annuelle_actuel': kw['evaluation_remuneration_annuelle_actuel'],
                                        'garantie_de_salaire_actuel': kw['garantie_de_salaire_actuel'],
                                        'nombre_de_clients_actuel': kw['nombre_de_clients_actuel'],
                                        'panier_moyen_actuel': kw['panier_moyen_actuel'],

                                        'chiffre_affaires_du_secteur_vise': kw['chiffre_affaires_du_secteur_vise'],
                                        'evaluation_remuneration_annuelle_vise': kw['evaluation_remuneration_annuelle_vise'],
                                        'garantie_de_salaire_vise': kw['garantie_de_salaire_vise'],
                                        'nombre_de_clients_vise': kw['nombre_de_clients_vise'],
                                        'panier_moyen_vise': kw['panier_moyen_vise'],


                                        'poste_budgete': kw['poste_budgete'],
                                        'statut_a_choisir': kw['statut_a_choisir'],
                                        'temps_de_travail_a_choisir': kw['temps_de_travail_a_choisir'],
                                        'commentaires': kw['commentaires'],
                                        'confidentiel': kw['confidentiel'],
                                        'fourchette_de_remuneration_annuelle_debutant': kw['fourchette_de_remuneration_annuelle_debutant'],
                                        'fourchette_de_remuneration_annuelle_experimente': kw['fourchette_de_remuneration_annuelle_experimente'],
                                        
                                        })

                files = request.httprequest.files.getlist('upload_files')

                _logger.info('---- files %s', files)

                attachments = []
                for file in files:
                    if file and file.filename:

                        file_data = file.read()
                        attachment = request.env['ir.attachment'].sudo().create({
                            'name': file.filename,
                            'datas': base64.b64encode(file_data),
                            'type': 'binary',
                            'res_model': 'helpdesk.ticket', 
                            'res_id': demande_recrutement.id,  
                        })
                        attachments.append(attachment)

                

                
                _logger.info('**************** update done rrh%s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_saved_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'rrh',})


            if request.env.user.demande_recrutement_session == 'rdrh':

                if 'from_rdrh_ck_demandeur' in kw:

                    if kw['from_rdrh_ck_demandeur'] == 'on':
                        kw_from_rdrh_ck_demandeur = True
                    else:
                        kw_from_rdrh_ck_demandeur = False
                else:
                    kw_from_rdrh_ck_demandeur = False

                if 'from_rdrh_ck_rrh' in kw:

                    if kw['from_rdrh_ck_rrh'] == 'on':
                        kw_from_rdrh_ck_rrh = True
                    else:
                        kw_from_rdrh_ck_rrh = False
                else:
                    kw_from_rdrh_ck_rrh = False

                if kw['poste_a_choisir_autre']:

                    kw_poste_a_choisir_autre = kw['poste_a_choisir_autre']
                else:

                    kw_poste_a_choisir_autre = False

                if kw['direction_a_choisir_id']:

                    kw_direction_a_choisir_id = int(kw['direction_a_choisir_id'])
                else:

                    kw_direction_a_choisir_id = False

                if kw['metier_a_choisir_id']:

                    kw_metier_a_choisir_id = int(kw['metier_a_choisir_id'])
                else:

                    kw_metier_a_choisir_id = False
              

                if kw['manager_recrutement']:

                    kw_manager_recrutement = int(kw['manager_recrutement'])
                else:

                    kw_manager_recrutement = False

                if kw['poste_a_choisir']:

                    kw_poste_a_choisir = int(kw['poste_a_choisir'])
                else:
                    kw_poste_a_choisir = False
                    
                if kw['date_de_debut_souhaite']:
                    kw_date_de_debut_souhaite = datetime.strptime(kw['date_de_debut_souhaite'], '%Y-%m-%d').date()
                else:
                    kw_date_de_debut_souhaite = False
                if kw['date_de_debut']:
                    kw_date_de_debut = datetime.strptime(kw['date_de_debut'], '%Y-%m-%d').date()
                else:
                    kw_date_de_debut= False
                if kw['date_de_fin']:
                    kw_date_de_fin = datetime.strptime(kw['date_de_fin'], '%Y-%m-%d').date()
                else:
                    kw_date_de_fin = False

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])

                demande_recrutement.sudo().write({

                                        'manager_recrutement': kw_manager_recrutement,
                                        'etablissement': kw['etablissement'],
                                        'rrh': kw['rrh'],
                                        'direction_a_choisir_id': kw_direction_a_choisir_id,
                                        'metier_a_choisir_id': kw_metier_a_choisir_id,
                                        'poste_a_choisir': kw_poste_a_choisir,
                                        'poste_a_choisir_autre': kw_poste_a_choisir_autre,
                                        'commentaire_demandeur': kw['commentaire_demandeur'],
                                        'motif_de_recrutement': kw['motif_de_recrutement'],
                                        'si_remplacement_qui': kw['si_remplacement_qui'],
                                        'type_contrat': kw['type_contrat'],
                                        'date_de_debut_souhaite': kw['date_de_debut_souhaite'],
                                        'date_de_debut': kw['date_de_debut'],
                                        'date_de_fin': kw['date_de_fin'],
                                        'missions_principales': kw['missions_principales'],
                                        'secteur_geographique': kw['secteur_geographique'],
                                        'specificite_clients': kw['specificite_clients'],
                                        'lieu_habitation_souhaite': kw['lieu_habitation_souhaite'],

                                        'chiffre_affaires_du_secteur_actuel': kw['chiffre_affaires_du_secteur_actuel'],
                                        'evaluation_remuneration_annuelle_actuel': kw['evaluation_remuneration_annuelle_actuel'],
                                        'garantie_de_salaire_actuel': kw['garantie_de_salaire_actuel'],
                                        'nombre_de_clients_actuel': kw['nombre_de_clients_actuel'],
                                        'panier_moyen_actuel': kw['panier_moyen_actuel'],

                                        'chiffre_affaires_du_secteur_vise': kw['chiffre_affaires_du_secteur_vise'],
                                        'evaluation_remuneration_annuelle_vise': kw['evaluation_remuneration_annuelle_vise'],
                                        'garantie_de_salaire_vise': kw['garantie_de_salaire_vise'],
                                        'nombre_de_clients_vise': kw['nombre_de_clients_vise'],
                                        'panier_moyen_vise': kw['panier_moyen_vise'],


                                        'poste_budgete': kw['poste_budgete'],
                                        'statut_a_choisir': kw['statut_a_choisir'],
                                        'temps_de_travail_a_choisir': kw['temps_de_travail_a_choisir'],
                                        'commentaires': kw['commentaires'],
                                        'confidentiel': kw['confidentiel'],
                                        'fourchette_de_remuneration_annuelle_debutant': kw['fourchette_de_remuneration_annuelle_debutant'],
                                        'fourchette_de_remuneration_annuelle_experimente': kw['fourchette_de_remuneration_annuelle_experimente'],

                                        'rdrh_comment_complete': kw['rdrh_comment_complete'],
                                        'from_rdrh_ck_demandeur': kw_from_rdrh_ck_demandeur,
                                        'from_rdrh_ck_rrh': kw_from_rdrh_ck_rrh,
                                        
                                        
                                        })

                files = request.httprequest.files.getlist('upload_files')

                _logger.info('---- files %s', files)

                attachments = []
                for file in files:
                    if file and file.filename:

                        file_data = file.read()
                        attachment = request.env['ir.attachment'].sudo().create({
                            'name': file.filename,
                            'datas': base64.b64encode(file_data),
                            'type': 'binary',
                            'res_model': 'helpdesk.ticket', 
                            'res_id': demande_recrutement.id,  
                        })
                        attachments.append(attachment)


                
                _logger.info('**************** update done rdrh%s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_saved_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'rdrh',})


            if request.env.user.demande_recrutement_session == 'direction':

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])
                demande_recrutement.sudo().write({

                                        'direction_commentaire': kw['direction_commentaire'],
                                        
                                        })

                _logger.info('**************** update done direction%s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_saved_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'direction',})

            if request.env.user.demande_recrutement_session == 'drh':

                

                if 'from_drh_ck_demandeur' in kw:

                    if kw['from_drh_ck_demandeur'] == 'on':
                        kw_from_drh_ck_demandeur = True
                    else:
                        kw_from_drh_ck_demandeur = False
                else:
                    kw_from_drh_ck_demandeur = False

                if 'from_drh_ck_rrh' in kw:

                    if kw['from_drh_ck_rrh'] == 'on':
                        kw_from_drh_ck_rrh = True
                    else:
                        kw_from_drh_ck_rrh = False
                else:
                    kw_from_drh_ck_rrh = False

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])

                demande_recrutement.sudo().write({

                                        'drh_comment_complete': kw['drh_comment_complete'],
                                        'from_drh_ck_demandeur': kw_from_drh_ck_demandeur,
                                        'from_drh_ck_rrh': kw_from_drh_ck_rrh,
                                        
                                        })

                
                _logger.info('**************** update done drh%s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_saved_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'drh',})

                
        else:
            return request.render("custom_helpdesk_website.not_user", {})



    @http.route(['/demande_recrutement/demandeur_update'], type='http', auth="user", website=True)
    def demende_recrutement_demandeur_update(self, **kw):

        _logger.info('++++++kw update %s', kw)
        _logger.info('*****env user %s', request.env.user)
        _logger.info('*****env user.id %s', request.env.user.id)
        _logger.info('*****env user.name %s', request.env.user.name)
        _logger.info('*****session %s', request.session.uid)

        if request.session.uid:


            if request.env.user.group_demande_recrutement_demandeur:

                if kw['poste_a_choisir_autre']:

                    kw_poste_a_choisir_autre = kw['poste_a_choisir_autre']
                else:

                    kw_poste_a_choisir_autre = False

                if kw['direction_a_choisir_id']:

                    kw_direction_a_choisir_id = int(kw['direction_a_choisir_id'])
                else:

                    kw_direction_a_choisir_id = False

                if kw['metier_a_choisir_id']:

                    kw_metier_a_choisir_id = int(kw['metier_a_choisir_id'])
                else:

                    kw_metier_a_choisir_id = False

                if kw['manager_recrutement']:

                    kw_manager_recrutement = int(kw['manager_recrutement'])
                else:

                    kw_manager_recrutement = False

                if kw['poste_a_choisir']:

                    kw_poste_a_choisir = int(kw['poste_a_choisir'])
                else:
                    kw_poste_a_choisir = False
                    
                if kw['date_de_debut_souhaite']:
                    kw_date_de_debut_souhaite = datetime.strptime(kw['date_de_debut_souhaite'], '%Y-%m-%d').date()
                else:
                    kw_date_de_debut_souhaite = False
                if kw['date_de_debut']:
                    kw_date_de_debut = datetime.strptime(kw['date_de_debut'], '%Y-%m-%d').date()
                else:
                    kw_date_de_debut= False
                if kw['date_de_fin']:
                    kw_date_de_fin = datetime.strptime(kw['date_de_fin'], '%Y-%m-%d').date()
                else:
                    kw_date_de_fin = False


                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])

                demande_recrutement.sudo().write({

                                        'manager_recrutement': kw_manager_recrutement,
                                        'etablissement': kw['etablissement'],
                                        'rrh': kw['rrh'],
                                        'direction_a_choisir_id': kw_direction_a_choisir_id,
                                        'metier_a_choisir_id': kw_metier_a_choisir_id,
                                        'poste_a_choisir': kw_poste_a_choisir,
                                        'poste_a_choisir_autre': kw_poste_a_choisir_autre,
                                        'commentaire_demandeur': kw['commentaire_demandeur'],
                                        'motif_de_recrutement': kw['motif_de_recrutement'],
                                        'si_remplacement_qui': kw['si_remplacement_qui'],
                                        'type_contrat': kw['type_contrat'],
                                        'date_de_debut_souhaite': kw['date_de_debut_souhaite'],
                                        'date_de_debut': kw['date_de_debut'],
                                        'date_de_fin': kw['date_de_fin'],
                                        'missions_principales': kw['missions_principales'],
                                        'secteur_geographique': kw['secteur_geographique'],
                                        'specificite_clients': kw['specificite_clients'],
                                        'lieu_habitation_souhaite': kw['lieu_habitation_souhaite'],

                                        'chiffre_affaires_du_secteur_actuel': kw['chiffre_affaires_du_secteur_actuel'],
                                        'evaluation_remuneration_annuelle_actuel': kw['evaluation_remuneration_annuelle_actuel'],
                                        'garantie_de_salaire_actuel': kw['garantie_de_salaire_actuel'],
                                        'nombre_de_clients_actuel': kw['nombre_de_clients_actuel'],
                                        'panier_moyen_actuel': kw['panier_moyen_actuel'],

                                        'chiffre_affaires_du_secteur_vise': kw['chiffre_affaires_du_secteur_vise'],
                                        'evaluation_remuneration_annuelle_vise': kw['evaluation_remuneration_annuelle_vise'],
                                        'garantie_de_salaire_vise': kw['garantie_de_salaire_vise'],
                                        'nombre_de_clients_vise': kw['nombre_de_clients_vise'],
                                        'panier_moyen_vise': kw['panier_moyen_vise'],


                                        })

                files = request.httprequest.files.getlist('upload_files')

                _logger.info('---- files %s', files)

                attachments = []
                for file in files:
                    if file and file.filename:
                        
                        file_data = file.read()
                        attachment = request.env['ir.attachment'].sudo().create({
                            'name': file.filename,
                            'datas': base64.b64encode(file_data),
                            'type': 'binary',
                            'res_model': 'helpdesk.ticket', 
                            'res_id': demande_recrutement.id,  
                        })
                        attachments.append(attachment)

                

                
                _logger.info('****************  demandeur update done%s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_saved_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'demandeur',})


            

                
        else:
            return request.render("custom_helpdesk_website.not_user", {})






    @http.route(['/demande_recrutement/rrh_acceptation_valide'], type='http', auth="user", website=True)
    def demende_recrutement_rrh_acceptation_valide(self, **kw):

        if request.session.uid:

            if request.env.user.demande_recrutement_session == 'rrh':

                stage_rdrh = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_traitement_rdrh')], limit=1)

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])

                demande_recrutement.sudo().write({

                                        'rrh_acceptation': 'Valide',
                                        'stage_id': stage_rdrh.id,
                                        'rrh_acceptation_user': request.env.user.id,
                                        
                                        })

                demande_recrutement_mail_template_info = request.env.ref('custom_helpdesk.email_template_demande_recrutement_demandeur_info')
                mail_context = {'email_to': demande_recrutement.partner_id.email,}
                demande_recrutement_mail_template_info.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)



                demande_recrutement_mail_template_rdrh = request.env.ref('custom_helpdesk.email_template_demande_recrutement_rdrh_link')
                users_rdrh = request.env['res.users'].sudo().search([('group_demande_recrutement_rdrh', '=',True)])
                for user_rdrh in users_rdrh:

                    mail_context = {'email_to': user_rdrh.partner_id.email,}
                    demande_recrutement_mail_template_rdrh.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)


                

                
                _logger.info('**************** rrh acceptation valide %s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_rrh_acceptation_valide_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'rrh',})

        else:
            return request.render("custom_helpdesk_website.not_user", {})


    @http.route(['/demande_recrutement/rrh_acceptation_refuse'], type='http', auth="user", website=True)
    def demende_recrutement_rrh_acceptation_refuse(self, **kw):

        if request.session.uid:

            if request.env.user.demande_recrutement_session == 'rrh':

                stage_refuse = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_refuse')], limit=1)

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])

                demande_recrutement.sudo().write({

                                        'rrh_acceptation': 'Refuse',
                                        'stage_id': stage_refuse.id,
                                        'rrh_acceptation_user': request.env.user.id,
                                        
                                        })

                demande_recrutement_mail_template_info = request.env.ref('custom_helpdesk.email_template_demande_recrutement_refuse_info_from_rrh')
                mail_context = {'email_to': demande_recrutement.partner_id.email,}
                demande_recrutement_mail_template_info.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                demande_recrutement_mail_template_manager_notif = request.env.ref('custom_helpdesk.email_template_demande_recrutement_manager_notif_refuse')
                mail_context = {'email_to': demande_recrutement.manager_recrutement.email,}
                demande_recrutement_mail_template_manager_notif.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                
                _logger.info('**************** rrh acceptation refuse %s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_rrh_acceptation_refuse_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'rrh',})

        else:
            return request.render("custom_helpdesk_website.not_user", {})



    @http.route(['/demande_recrutement/rdrh_acceptation_valide'], type='http', auth="user", website=True)
    def demende_recrutement_rdrh_acceptation_valide(self, **kw):

        if request.session.uid:

            if request.env.user.demande_recrutement_session == 'rdrh':

                stage_direction = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_traitement_direction')], limit=1)

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])

                demande_recrutement.sudo().write({

                                        'rdrh_acceptation': 'Valide',
                                        'stage_id': stage_direction.id,
                                        'rdrh_acceptation_user': request.env.user.id,
                                        
                                        })

                demande_recrutement_mail_template_info = request.env.ref('custom_helpdesk.email_template_demande_recrutement_demandeur_info')
                mail_context = {'email_to': demande_recrutement.partner_id.email,}
                demande_recrutement_mail_template_info.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)



                demande_recrutement_mail_template_direction = request.env.ref('custom_helpdesk.email_template_demande_recrutement_direction_link')
                users_direction = request.env['res.users'].sudo().search([('group_demande_recrutement_direction', '=',True), ('direction_id', '=',demande_recrutement.direction_a_choisir_id.id)])
                for user_direction in users_direction:

                    mail_context = {'email_to': user_direction.partner_id.email,}
                    demande_recrutement_mail_template_direction.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                
                _logger.info('**************** rdrh acceptation valide %s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_rdrh_acceptation_valide_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'rdrh',})

        else:
            return request.render("custom_helpdesk_website.not_user", {})


    @http.route(['/demande_recrutement/rdrh_acceptation_refuse'], type='http', auth="user", website=True)
    def demende_recrutement_rdrh_acceptation_refuse(self, **kw):

        if request.session.uid:

            if request.env.user.demande_recrutement_session == 'rdrh':

                stage_refuse = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_refuse')], limit=1)

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])

                demande_recrutement.sudo().write({

                                        'rdrh_acceptation': 'Refuse',
                                        'stage_id': stage_refuse.id,
                                        'rdrh_acceptation_user': request.env.user.id,
                                        
                                        })
                demande_recrutement_mail_template_info = request.env.ref('custom_helpdesk.email_template_demande_recrutement_refuse_info_from_rdrh')
                mail_context = {'email_to': demande_recrutement.partner_id.email,}
                demande_recrutement_mail_template_info.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)


                demande_recrutement_mail_template_rrh = request.env.ref('custom_helpdesk.email_template_demande_recrutement_refuse_link_from_rdrh')
                mail_context = {'email_to': demande_recrutement.rrh_acceptation_user.partner_id.email,}
                demande_recrutement_mail_template_rrh.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                demande_recrutement_mail_template_manager_notif = request.env.ref('custom_helpdesk.email_template_demande_recrutement_manager_notif_refuse')
                mail_context = {'email_to': demande_recrutement.manager_recrutement.email,}
                demande_recrutement_mail_template_manager_notif.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                
                _logger.info('**************** rdrh acceptation refuse %s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_rdrh_acceptation_refuse_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'rdrh',})

        else:
            return request.render("custom_helpdesk_website.not_user", {})


    @http.route(['/demande_recrutement/direction_acceptation_valide'], type='http', auth="user", website=True)
    def demende_recrutement_direction_acceptation_valide(self, **kw):

        if request.session.uid:

            if request.env.user.demande_recrutement_session == 'direction':

                stage_drh = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_traitement_drh')], limit=1)

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])

                demande_recrutement.sudo().write({

                                        'direction_acceptation': 'Valide',
                                        'stage_id': stage_drh.id,
                                        'direction_acceptation_user': request.env.user.id,
                                        
                                        })

                demande_recrutement_mail_template_info = request.env.ref('custom_helpdesk.email_template_demande_recrutement_demandeur_info')
                mail_context = {'email_to': demande_recrutement.partner_id.email,}
                demande_recrutement_mail_template_info.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                demande_recrutement_mail_template_drh = request.env.ref('custom_helpdesk.email_template_demande_recrutement_drh_link')
                users_drh = request.env['res.users'].sudo().search([('group_demande_recrutement_drh', '=',True)])
                for user_drh in users_drh:

                    mail_context = {'email_to': user_drh.partner_id.email,}
                    demande_recrutement_mail_template_drh.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                
                _logger.info('**************** direction acceptation valide %s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_direction_acceptation_valide_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'direction',})

        else:
            return request.render("custom_helpdesk_website.not_user", {})


    @http.route(['/demande_recrutement/direction_acceptation_refuse'], type='http', auth="user", website=True)
    def demende_recrutement_direction_acceptation_refuse(self, **kw):

        if request.session.uid:

            if request.env.user.demande_recrutement_session == 'direction':

                stage_refuse = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_refuse')], limit=1)

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])

                demande_recrutement.sudo().write({

                                        'direction_acceptation': 'Refuse',
                                        'stage_id': stage_refuse.id,
                                        'direction_acceptation_user': request.env.user.id,
                                        
                                        })

                demande_recrutement_mail_template_info = request.env.ref('custom_helpdesk.email_template_demande_recrutement_refuse_info_from_direction')
                mail_context = {'email_to': demande_recrutement.partner_id.email,}
                demande_recrutement_mail_template_info.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)


                demande_recrutement_mail_template_rrh = request.env.ref('custom_helpdesk.email_template_demande_recrutement_refuse_link_from_direction')
                mail_context = {'email_to': demande_recrutement.rrh_acceptation_user.partner_id.email,}
                demande_recrutement_mail_template_rrh.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                demande_recrutement_mail_template_rdrh = request.env.ref('custom_helpdesk.email_template_demande_recrutement_refuse_link_from_direction')
                mail_context = {'email_to': demande_recrutement.rdrh_acceptation_user.partner_id.email,}
                demande_recrutement_mail_template_rdrh.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                demande_recrutement_mail_template_manager_notif = request.env.ref('custom_helpdesk.email_template_demande_recrutement_manager_notif_refuse')
                mail_context = {'email_to': demande_recrutement.manager_recrutement.email,}
                demande_recrutement_mail_template_manager_notif.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                
                _logger.info('**************** direction acceptation refuse %s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_direction_acceptation_refuse_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'direction',})

        else:
            return request.render("custom_helpdesk_website.not_user", {})



    @http.route(['/demande_recrutement/drh_acceptation_valide'], type='http', auth="user", website=True)
    def demende_recrutement_drh_acceptation_valide(self, **kw):

        if request.session.uid:

            if request.env.user.demande_recrutement_session == 'drh':

                stage_valide = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_valide')], limit=1)

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])

                demande_recrutement.sudo().write({

                                        'drh_acceptation': 'Valide',
                                        'stage_id': stage_valide.id,
                                        'drh_acceptation_user': request.env.user.id,
                                        
                                        })

                demande_recrutement_mail_template_info = request.env.ref('custom_helpdesk.email_template_demande_recrutement_valide_info')
                mail_context = {'email_to': demande_recrutement.partner_id.email,}
                demande_recrutement_mail_template_info.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                demande_recrutement_mail_template_manager_notif = request.env.ref('custom_helpdesk.email_template_demande_recrutement_manager_notif_valide')
                mail_context = {'email_to': demande_recrutement.manager_recrutement.email,}
                demande_recrutement_mail_template_manager_notif.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)


                demande_recrutement_mail_template_rrh = request.env.ref('custom_helpdesk.email_template_demande_recrutement_valide_link_from_drh')
                mail_context = {'email_to': demande_recrutement.rrh_acceptation_user.partner_id.email,}
                demande_recrutement_mail_template_rrh.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                demande_recrutement_mail_template_rdrh = request.env.ref('custom_helpdesk.email_template_demande_recrutement_valide_link_from_drh')
                mail_context = {'email_to': demande_recrutement.rdrh_acceptation_user.partner_id.email,}
                demande_recrutement_mail_template_rdrh.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                demande_recrutement_mail_template_direction = request.env.ref('custom_helpdesk.email_template_demande_recrutement_valide_link_from_drh')
                mail_context = {'email_to': demande_recrutement.direction_acceptation_user.partner_id.email,}
                demande_recrutement_mail_template_direction.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                

                
                _logger.info('**************** drh acceptation valide %s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_drh_acceptation_valide_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'drh',})

        else:
            return request.render("custom_helpdesk_website.not_user", {})


    @http.route(['/demande_recrutement/drh_acceptation_refuse'], type='http', auth="user", website=True)
    def demende_recrutement_drh_acceptation_refuse(self, **kw):

        if request.session.uid:

            if request.env.user.demande_recrutement_session == 'drh':

                stage_refuse = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_refuse')], limit=1)

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])

                demande_recrutement.sudo().write({

                                        'drh_acceptation': 'Refuse',
                                        'stage_id': stage_refuse.id,
                                        'drh_acceptation_user': request.env.user.id,
                                        
                                        })

                demande_recrutement_mail_template_info = request.env.ref('custom_helpdesk.email_template_demande_recrutement_refuse_info_from_drh')
                mail_context = {'email_to': demande_recrutement.partner_id.email,}
                demande_recrutement_mail_template_info.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)


                demande_recrutement_mail_template_rrh = request.env.ref('custom_helpdesk.email_template_demande_recrutement_refuse_link_from_drh')
                mail_context = {'email_to': demande_recrutement.rrh_acceptation_user.partner_id.email,}
                demande_recrutement_mail_template_rrh.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                demande_recrutement_mail_template_rdrh = request.env.ref('custom_helpdesk.email_template_demande_recrutement_refuse_link_from_drh')
                mail_context = {'email_to': demande_recrutement.rdrh_acceptation_user.partner_id.email,}
                demande_recrutement_mail_template_rdrh.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                demande_recrutement_mail_template_direction = request.env.ref('custom_helpdesk.email_template_demande_recrutement_refuse_link_from_drh')
                mail_context = {'email_to': demande_recrutement.direction_acceptation_user.partner_id.email,}
                demande_recrutement_mail_template_direction.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                demande_recrutement_mail_template_manager_notif = request.env.ref('custom_helpdesk.email_template_demande_recrutement_manager_notif_refuse')
                mail_context = {'email_to': demande_recrutement.manager_recrutement.email,}
                demande_recrutement_mail_template_manager_notif.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                
                _logger.info('**************** drh acceptation refuse %s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_drh_acceptation_refuse_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'drh',})

        else:
            return request.render("custom_helpdesk_website.not_user", {})






















    @http.route(['/demande_recrutement/rdrh_demande_infos'], type='http', auth="user", website=True)
    def demende_recrutement_rdrh_demande_infos(self, **kw):

        if request.session.uid:

            if request.env.user.demande_recrutement_session == 'rdrh':

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])

                if demande_recrutement.from_rdrh_ck_rrh == True and demande_recrutement.from_rdrh_ck_demandeur == True:

                    _logger.info('+++++ state to demande , mail to demandeur and rrh')

                    stage_demande = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_demande')], limit=1)
                    
                    demande_recrutement.write({'stage_id': stage_demande.id,})
                    demande_recrutement.write({'rrh_acceptation': False,})

                    demande_recrutement_mail_template = request.env.ref('custom_helpdesk.email_template_demande_recrutement_demande_infos_from_rdrh')

                    mail_context = {

                        'email_to': demande_recrutement.partner_id.email,
                    }

                    demande_recrutement_mail_template.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)



                    user_rrh = request.env['res.users'].sudo().search([('name', '=',demande_recrutement.rrh)], limit=1)
                    mail_context = {

                        'email_to': user_rrh.partner_id.email,
                    }

                    demande_recrutement_mail_template.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                elif demande_recrutement.from_rdrh_ck_rrh == True:

                    _logger.info('+++++ state to traitement rrh , mail to rrh only')

                    
                    stage_traitement_rrh = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_traitemnt_rrh')], limit=1)
                    
                    demande_recrutement.write({'stage_id': stage_traitement_rrh.id,})
                    demande_recrutement.write({'rrh_acceptation': False,})

                    demande_recrutement_mail_template = request.env.ref('custom_helpdesk.email_template_demande_recrutement_demande_infos_from_rdrh')

                    user_rrh = request.env['res.users'].sudo().search([('name', '=',demande_recrutement.rrh)], limit=1)

                    mail_context = {

                        'email_to': user_rrh.partner_id.email,
                    }

                    demande_recrutement_mail_template.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                elif demande_recrutement.from_rdrh_ck_demandeur == True:

                    _logger.info('+++++ state to demande , mail to demandeur only')

                    stage_demande = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_demande')], limit=1)
                    
                    demande_recrutement.write({'stage_id': stage_demande.id,})

                    demande_recrutement_mail_template = request.env.ref('custom_helpdesk.email_template_demande_recrutement_demande_infos_from_rdrh')

                    mail_context = {

                        'email_to': demande_recrutement.partner_id.email,
                    }

                    demande_recrutement_mail_template.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)


                _logger.info('**************** rdrh demande infos %s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_send_infos_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'rdrh',})

        else:
            return request.render("custom_helpdesk_website.not_user", {})



    @http.route(['/demande_recrutement/drh_demande_infos'], type='http', auth="user", website=True)
    def demende_recrutement_drh_demande_infos(self, **kw):

        if request.session.uid:

            if request.env.user.demande_recrutement_session == 'drh':

                demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['demande_recrutement_id'])])

                if demande_recrutement.from_drh_ck_rrh == True and demande_recrutement.from_drh_ck_demandeur == True:

                    _logger.info('+++++ state to demande , mail to demandeur and rrh')

                    stage_demande = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_demande')], limit=1)
                    
                    demande_recrutement.write({'direction_acceptation': False,})
                    demande_recrutement.write({'rdrh_acceptation': False,})
                    demande_recrutement.write({'rrh_acceptation': False,})

                    demande_recrutement_mail_template = request.env.ref('custom_helpdesk.email_template_demande_recrutement_demande_infos_from_drh')

                    mail_context = {

                        'email_to': demande_recrutement.partner_id.email,
                    }

                    demande_recrutement_mail_template.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)



                    user_rrh = request.env['res.users'].sudo().search([('name', '=',demande_recrutement.rrh)], limit=1)
                    mail_context = {

                        'email_to': user_rrh.partner_id.email,
                    }

                    demande_recrutement_mail_template.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                elif demande_recrutement.from_drh_ck_rrh == True:

                    _logger.info('+++++ state to traitement rrh , mail to rrh only')

                    
                    stage_traitement_rrh = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_traitemnt_rrh')], limit=1)
                    
                    demande_recrutement.write({'stage_id': stage_traitement_rrh.id,})
                    
                    demande_recrutement.write({'direction_acceptation': False,})
                    demande_recrutement.write({'rdrh_acceptation': False,})
                    demande_recrutement.write({'rrh_acceptation': False,})

                    demande_recrutement_mail_template = request.env.ref('custom_helpdesk.email_template_demande_recrutement_demande_infos_from_drh')

                    user_rrh = request.env['res.users'].sudo().search([('name', '=',demande_recrutement.rrh)], limit=1)

                    mail_context = {

                        'email_to': user_rrh.partner_id.email,
                    }

                    demande_recrutement_mail_template.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)

                elif demande_recrutement.from_drh_ck_demandeur == True:

                    _logger.info('+++++ state to demande , mail to demandeur only')

                    stage_demande = request.env['helpdesk.stage'].sudo().search([('etape', '=','dr_demande')], limit=1)
                    
                    demande_recrutement.write({'stage_id': stage_demande.id,})

                    demande_recrutement_mail_template = request.env.ref('custom_helpdesk.email_template_demande_recrutement_demande_infos_from_drh')

                    mail_context = {

                        'email_to': demande_recrutement.partner_id.email,
                    }

                    demande_recrutement_mail_template.sudo().send_mail(demande_recrutement.id, email_values=mail_context, force_send=True)


                _logger.info('**************** rdrh demande infos %s', request.env.user)
                if request.session.uid:
                    return request.render("custom_helpdesk_website.demande_recrutement_send_infos_succes", {'demande_recrutement': demande_recrutement,'current_user_group': 'drh',})

        else:
            return request.render("custom_helpdesk_website.not_user", {})
            







    ########################ATTACH


    @http.route('/download/file/<int:file_id>', type='http', auth="user", website=True)
    def download_file(self, file_id):
        attachment = request.env['ir.attachment'].sudo().browse(file_id)
        if attachment:
            file_content = base64.b64decode(attachment.datas)
            headers = [
                ('Content-Type', attachment.mimetype),
                ('Content-Disposition', f'attachment; filename={attachment.name}')
            ]
            return request.make_response(file_content, headers)
        return request.render("custom_helpdesk_website.not_user", {})



    @http.route('/delete/attachment', type='json', auth="user", methods=['POST'], website=True)
    def delete_attachment(self, attachment_id):
        try:
            attachment = request.env['ir.attachment'].sudo().search([('id', '=', int(attachment_id))], limit=1)
            if attachment:

                attachment.sudo().unlink()

                return {'status': 'success', 'message': 'Attachment deleted successfully'}
            else:
                return {'status': 'error', 'message': 'Attachment not found'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}












    @http.route(['/demande_recrutement/form_access/<int:demande_recrutement_id>'], type='http', auth="user", website=True)
    def demande_recrutement_form_access(self,demande_recrutement_id):

        _logger.info('*********** call demande_recrutement_form_access *****%s', demande_recrutement_id)

        if request.session.uid:

            demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=',demande_recrutement_id)])

            if demande_recrutement:
                demande_recrutement_team = request.env['helpdesk.team'].sudo().search([('equipe', '=','demande_recrutement')], limit=1)

                if demande_recrutement.team_id.id == demande_recrutement_team.id:

                    access_list = []

                    if request.env.user.group_demande_recrutement_demandeur:
                        access_list.append('demandeur')
                    if request.env.user.group_demande_recrutement_rrh:
                        access_list.append('rrh')
                    if request.env.user.group_demande_recrutement_rdrh:
                        access_list.append('rdrh')
                    if request.env.user.group_demande_recrutement_direction:
                        access_list.append('direction')
                    if request.env.user.group_demande_recrutement_drh:
                        access_list.append('drh')

                    _logger.info('++++access_list %s', access_list)

                    return http.request.render('custom_helpdesk_website.demande_recrutement_form_access', {'demande_recrutement': demande_recrutement, 'access_list': access_list,})
            
        else:
            return request.render("custom_helpdesk_website.not_user", {})




    @http.route(['/demande_recrutement/form_access_as'], type='http', auth="user", website=True)
    def demande_recrutement_form_access_as(self, **kw):

        

        _logger.info('*********** call demande_recrutement_form_access_as *****%s', kw['demande_recrutement_id'])
        _logger.info('*********** call demande_recrutement_form_access_as *****%s', kw['group'])

       

        if request.session.uid:

            demande_recrutement = request.env['helpdesk.ticket'].sudo().search([('id', '=',int(kw['demande_recrutement_id']))])

            if demande_recrutement:
                demande_recrutement_team = request.env['helpdesk.team'].sudo().search([('equipe', '=','demande_recrutement')], limit=1)

                if demande_recrutement.team_id.id == demande_recrutement_team.id:

                    
                    _logger.info('---- all good')

                    if kw['group'] == 'demandeur':

                        _logger.info('*****env user %s', request.env.user)
                        utilisateur = request.env.user
                        utilisateur.demande_recrutement_session = 'demandeur'

                        demande_recrutement_base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                        demande_recrutement_base_url += '/helpdesk/ticket_demande_recrutement/%s' % (int(kw['demande_recrutement_id']))
                        return request.redirect(demande_recrutement_base_url)


                    if kw['group'] == 'rrh':

                        _logger.info('*****env user %s', request.env.user)
                        utilisateur = request.env.user
                        utilisateur.demande_recrutement_session = 'rrh'

                        demande_recrutement_base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                        demande_recrutement_base_url += '/demande_recrutement/form/%s' % (int(kw['demande_recrutement_id']))
                        return request.redirect(demande_recrutement_base_url)


                    if kw['group'] == 'rdrh':

                        _logger.info('*****env user %s', request.env.user)
                        utilisateur = request.env.user
                        utilisateur.demande_recrutement_session = 'rdrh'

                        demande_recrutement_base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                        demande_recrutement_base_url += '/demande_recrutement/form/%s' % (int(kw['demande_recrutement_id']))
                        return request.redirect(demande_recrutement_base_url)

                    if kw['group'] == 'direction':

                        _logger.info('*****env user %s', request.env.user)
                        utilisateur = request.env.user
                        utilisateur.demande_recrutement_session = 'direction'

                        demande_recrutement_base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                        demande_recrutement_base_url += '/demande_recrutement/form/%s' % (int(kw['demande_recrutement_id']))
                        return request.redirect(demande_recrutement_base_url)


                    if kw['group'] == 'drh':

                        _logger.info('*****env user %s', request.env.user)
                        utilisateur = request.env.user
                        utilisateur.demande_recrutement_session = 'drh'

                        demande_recrutement_base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                        demande_recrutement_base_url += '/demande_recrutement/form/%s' % (int(kw['demande_recrutement_id']))
                        return request.redirect(demande_recrutement_base_url)

     
        else:
            return request.render("custom_helpdesk_website.not_user", {})


