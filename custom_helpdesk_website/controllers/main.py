# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import base64
import io
import re
from datetime import date
import logging

_logger = logging.getLogger(__name__)

class WebsiteTicket(http.Controller):

    @http.route(['/ticket_webform'], type='http', auth="public", website=True, sitemap=False)
    def ticket_webform(self, **kw):
        if request.env.user.has_group('custom_helpdesk.group_it_manager_data') or request.env.user.group_it_manager_data:
            return http.request.render('custom_helpdesk_website.create_ticket', {})
        else:
            return http.request.render('portal.portal_my_home', {})

    #@http.route(['/ticket_webform_rh'], type='http', auth="public", website=True, sitemap=False)

    # def ticket_webformm(self, **kw):
    #     if request.env.user.has_group('custom_helpdesk.group_hr_user_data'):
    #         return http.request.render('custom_helpdesk_website.create_ticket_rh', {})
    #
    #     else:
    #         return http.request.render('portal.portal_my_home', {})

    # @http.route(['/create/ticket_rh'], type='http', auth="public", website=True, sitemap=False)
    # def create_webtickett(self, **kw):
    #
    #     if not kw['x_studio_date_de_depart']:
    #         kw.pop('x_studio_date_de_depart')
    #     if not kw['x_studio_date_de_cration']:
    #         kw.pop('x_studio_date_de_cration')
    #     if not kw['x_studio_date_de_naissance']:
    #         kw.pop('x_studio_date_de_naissance')
    #     if not kw['x_studio_date_darrive']:
    #         kw.pop('x_studio_date_darrive')
    #     if 'x_studio_pc_housse_sourisclavier' in kw:
    #         if kw['x_studio_pc_housse_sourisclavier']=='on':
    #             x_studio_pc_housse_sourisclavier = True
    #             kw.update({'x_studio_pc_housse_sourisclavier': x_studio_pc_housse_sourisclavier})
    #     if 'x_studio_ecran' in kw:
    #         if kw['x_studio_ecran'] == 'on':
    #             x_studio_ecran = True
    #             kw.update({'x_studio_ecran': x_studio_ecran})
    #     if 'x_studio_ecran_supplmentaire' in kw:
    #         if kw['x_studio_ecran_supplmentaire'] == 'on':
    #             x_studio_ecran_supplmentaire = True
    #             kw.update({'x_studio_ecran_supplmentaire': x_studio_ecran_supplmentaire})
    #
    #     job_id = request.env['hr.job'].search([('name', '=', kw['x_studio_type_de_fontion'])], limit=1).id
    #     kw.update({'x_studio_type_de_fontion': job_id})
    #
    #
    #     ticket = request.env['helpdesk.ticket'].sudo().create(kw)
    #     team_id = request.env['helpdesk.team'].search([('equipe', '=', 'support_rh')], limit=1).id
    #     if team_id:
    #         ticket.write({'team_id': team_id})
    #     dbname = request.env.cr.dbname
    #     base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #     base_url += '/helpdesk/tickett/%s' % (ticket.id)
    #     ticket.write({'ticket_url': base_url})
    #     reponse_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #     reponse_url += '/helpdesk/reponse/tickett/%s' % (ticket.id)
    #     ticket.write({'reponse_url': reponse_url})
    #
    #
    #     mail_template = request.env.ref('custom_helpdesk.email_template_traitement_manager')
    #
    #     mail_context = {
    #
    #         'email_to': kw['x_studio_adresse_mail_du_n1'],
    #         #'body_html': f"BODY FOR TRAITEMENT PRESTATAIRE TO C2S \n vous avez une nouvelle " + "<a href='" + base_url + "'>Ticket</a>" + " à remplir : "
    #
    #     }
    #
    #     mail_template.sudo().send_mail(ticket.id, email_values=mail_context, force_send=True)
    #
    #
    #
    #     return http.request.render('custom_helpdesk_website.ticket_thanksss', {})

    @http.route(['/create/ticket'], type='http', auth="public", website=True, sitemap=False)
    def create_webticket(self, **kw):
        # employee_id = request.env['hr.employee'].search([('name', '=', kw['employee_id'])], limit=1).id
        # kw.update({'employee_id': employee_id})
        piece = kw.get('piece')
        kw.update({'piece': piece})
        piece_master_data = kw.get('piece_master_data')
        priority = ''
        if kw.get('seul_impacte') == 'oui' and kw.get('travaille') == 'oui':
            priority = '1'
        if kw.get('seul_impacte') == 'oui' and kw.get('travaille') == 'non':
            priority = '3'
        if kw.get('seul_impacte') == 'non' and kw.get('travaille') == 'non':
            priority = '3'
        if kw.get('seul_impacte') == 'non' and kw.get('travaille') == 'oui':
            priority = '2'

        piece_master = kw.get('piece_master_data')
        piece = kw.get('piece')

        if piece_master:
            binary_data = base64.b64encode(piece_master.read()).decode('utf-8')

            # Remove invalid characters from base64 string
            cleaned_base64 = re.sub('[^A-Za-z0-9+/=]', '', binary_data)

            # Add padding if necessary
            padding = '=' * (4 - (len(cleaned_base64) % 4))
            piece_master_data = cleaned_base64 + padding
            kw.update({'piece_master_data': piece_master_data})

        if piece:
            binary_data = base64.b64encode(piece.read()).decode('utf-8')

            # Remove invalid characters from base64 string
            cleaned_base64 = re.sub('[^A-Za-z0-9+/=]', '', binary_data)

            # Add padding if necessary
            padding = '=' * (4 - (len(cleaned_base64) % 4))
            piecee = cleaned_base64 + padding
            kw.update({'piece': piecee})
        ticket = request.env['helpdesk.ticket'].sudo().create(kw)
        ticket.write({'priority': priority})
        team_id = request.env['helpdesk.team'].search([('equipe', '=', 'service_clientele')], limit=1).id
        if team_id:
            ticket.write({'team_id': team_id})
        dbname = request.env.cr.dbname
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url += '/web?db=%s#id=%d&view_type=form&model=%s' % (dbname, ticket.id, ticket._name)
        ticket.write({'ticket_url': base_url})
        reponse_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        reponse_url += '/helpdesk/reponse/tickett/%s' % (ticket.id)
        ticket.write({'reponse_url': reponse_url})


        if kw['materiel']=='pc' or kw['logiciel']=='argu' or kw['logiciel']=='start' or kw['logiciel']=='pc' or kw['num_imprimante']=='*LEKXMARK*':

            mail_template = request.env.ref('custom_helpdesk.email_template_materiel_pc_logiciel_start')

            mail_context = {

                #'email_to': 'exploitconsult2022@gmail.com, omar@exploit-consult.com',
                #'body_html': f"BODY FOR materiel pc logiciel start TO C2S \n vous avez une nouvelle " + "<a href='" + base_url + "'>Ticket</a>" + " à remplir : "

            }

            mail_template.sudo().send_mail(ticket.id, email_values=mail_context, force_send=True)
        if kw['materiel']=='reseau_sasety':

            mail_template = request.env.ref('custom_helpdesk.email_template_reseau_sasety')

            mail_context = {

                #'email_to': 'exploitconsult2022@gmail.com, omar@exploit-consult.com',
                #'body_html': f"BODY FOR Si Réseau sasety \n vous avez une nouvelle " + "<a href='" + base_url + "'>Ticket</a>" + " à remplir : "

            }

            mail_template.sudo().send_mail(ticket.id, email_values=mail_context, force_send=True)
        if kw['logiciel'] == 'sap':

            mail_template = request.env.ref('custom_helpdesk.email_template_si_sap_si_keu')

            mail_context = {

                #'email_to': 'exploitconsult2022@gmail.com, omar@exploit-consult.com',
                #'body_html': f" BODY FOR Si SAP :Si KEU USER/CP SAP \n vous avez une nouvelle " + "<a href='" + base_url + "'>Ticket</a>" + " à remplir : "

            }

            mail_template.sudo().send_mail(ticket.id, email_values=mail_context, force_send=True)



        if kw['logiciel'] == 'vim':

            mail_template = request.env.ref('custom_helpdesk.email_template_si_sap_si_keu_transaction_vim')

            mail_context = {

                #'email_to': 'exploitconsult2022@gmail.com, omar@exploit-consult.com',
                #'body_html': f" BODY FOR Si transaction VIM \n vous avez une nouvelle " + "<a href='" + base_url + "'>Ticket</a>" + " à remplir : "

            }

            mail_template.sudo().send_mail(ticket.id, email_values=mail_context, force_send=True)


        if kw['logiciel'] == 'edi':
            mail_template = request.env.ref('custom_helpdesk.email_template_logiciel_edi')

            mail_context = {

                #'email_to': 'exploitconsult2022@gmail.com, omar@exploit-consult.com',
                #'body_html': f" BODY FOR Si LOGICIEL EDI \n vous avez une nouvelle réclamation client, vous pouvez l'appeler sur ce numéro " + kw['partner_phone']

            }

            mail_template.sudo().send_mail(ticket.id, email_values=mail_context, force_send=True)


        if kw['logiciel'] == 'nomad':
            mail_template = request.env.ref('custom_helpdesk.email_template_logiciel_nomad')

            mail_context = {

                #'email_to': 'exploitconsult2022@gmail.com, omar@exploit-consult.com',
                #'body_html': f" BODY FOR Si LOGICIEL Nomad \n vous avez une nouvelle réclamation client, vous pouvez l'appeler sur ce numéro " + kw['partner_phone']

            }

            mail_template.sudo().send_mail(ticket.id, email_values=mail_context, force_send=True)



        if kw['materiel'] == 'flasheuse':
            mail_template = request.env.ref('custom_helpdesk.email_template_materiel_Type_flasheuse')

            mail_context = {

                #'email_to': 'exploitconsult2022@gmail.com, omar@exploit-consult.com',
                #'body_html': f"BODY FOR Si matériel Type flasheuse \n vous avez une nouvelle réclamation client, vous pouvez l'appeler sur ce numéro " + kw['partner_phone']

            }

            mail_template.sudo().send_mail(ticket.id, email_values=mail_context, force_send=True)


        if kw['materiel'] == 'voice_picking':
            mail_template = request.env.ref('custom_helpdesk.email_template_appareil_voice_picking')

            mail_context = {

                #'email_to': 'exploitconsult2022@gmail.com, omar@exploit-consult.com',
                #'body_html': f"BODY FOR Si Appareil Voice Picking \n vous avez une nouvelle réclamation client, vous pouvez l'appeler sur ce numéro " + kw['partner_phone']

            }

            mail_template.sudo().send_mail(ticket.id, email_values=mail_context, force_send=True)


        if kw['materiel'] == 'smartphone' or kw['materiel'] == 'ipad':
            mail_template = request.env.ref('custom_helpdesk.email_template_appareil_materiel_smartphone_ipad')

            mail_context = {

                #'email_to': 'exploitconsult2022@gmail.com, omar@exploit-consult.com',
                #'body_html': f"BODY FOR Si matériel smartphone et ou ipad \n vous avez une nouvelle réclamation client, vous pouvez l'appeler sur ce numéro " + kw['partner_phone']

            }

            mail_template.sudo().send_mail(ticket.id, email_values=mail_context, force_send=True)

        return http.request.render('custom_helpdesk_website.ticket_thanks', {})

    @http.route(['/reponse/ticket'], type='http', auth="public", website=True, sitemap=False)
    def reponse_webticket(self, **kw):




        ticket = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['id'])])

        ticket.write({'reponse': kw['mail']})


        return http.request.render('custom_helpdesk_website.ticket_thanks_response', {})


