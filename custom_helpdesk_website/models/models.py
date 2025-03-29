# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class HelpdeskTicketInherit(models.Model):
    _inherit = 'helpdesk.ticket'

    partner_id = fields.Many2one('res.partner', string='Customer', tracking=True, required=True)
    partner_email = fields.Char(string='Customer Email', compute='_compute_partner_email', inverse="_inverse_partner_email", store=True, readonly=False, required=True)

    @api.model_create_multi
    def create(self, values):
        the_ticket = super(HelpdeskTicketInherit, self).create(values)
        _logger.info('enter in create method')
        if the_ticket.team_id.equipe == 'master_data':
            _logger.info('enter in master data cond')
            if the_ticket.email_cc:
                _logger.info('***** email_cc %s', the_ticket.email_cc)
                the_emails_list = the_ticket.email_cc.split(',')
                partners = self.env['res.partner'].search([('email','in',the_emails_list)])
                _logger.info('***** partners %s', partners)

                if partners:
                    for partner in partners:
                        reg = { 
                               'res_id': the_ticket.id, 
                               'res_model': 'helpdesk.ticket', 
                               'partner_id': partner.id, 
                              } 
                        if not self.env['mail.followers'].search([('res_id','=',the_ticket.id),('res_model','=','helpdesk.ticket'),('partner_id','=',partner.id)]): 
                            follower_id = self.env['mail.followers'].create(reg)
                            
        if the_ticket.team_id.equipe == 'support_rh':
            
            dbname = request.env.cr.dbname
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            base_url += '/helpdesk/tickett/%s' % (the_ticket.id)
            #self.ticket_url = base_url
            reponse_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            reponse_url += '/helpdesk/reponse/tickett/%s' % (the_ticket.id)
            #self.reponse_url = reponse_url
            mail_template = the_ticket.env.ref('custom_helpdesk.email_template_traitement_manager')
            message_text = f'<p><strong>Bonjour,</strong></p> ' \
            f'<p><strong>Un nouvel utilisateur arrive chez Supergroup. Merci de vous connecter afin de créer son compte et préparer ses accès. vous pouvez vous connecter via le lien : <a href="'+str(base_url)+'">'+str(the_ticket.name)+'</a> </strong></p> ' \
            f'<br/><br/><br/><p><span style="color:red"><strong>Attention à bien être connecter pour remplir les informations du nouvel arrivant</strong></span></p> ' \
            f'<div><img src="https://intranet-supergroup.odoo.com/web/image/website/1/logo/Intranet-supergroup?unique=4ed9ab6" style="width: 250px;height: 150px;"/></div>' \
            
            
            
            vals = {
                        'body_html': message_text,
                        'subject': 'le ticket'+the_ticket.name+' est devenus '+the_ticket.stage_id.name,
                        'email_to': the_ticket.partner_email,
                        'auto_delete': False,
                        'email_from': mail_template.email_from,
                        }
            _logger.info('all params are OK')
            _logger.info('+++email_to %s', the_ticket.partner_email)
            _logger.info('+++email_from %s', mail_template.email_from)
            
            mail_id = self.env['mail.mail'].sudo().create(vals)
            _logger.info('+++mail_id %s', mail_id)
            test_sending = mail_id.sudo().send()
            _logger.info('+++test_sending %s', test_sending)
            _logger.info('mail OK')
        return the_ticket
        

      


    def action_compute_mail(self):
       
        _logger.info('**************** ommmmaaarrrrrrr')
        
        dbname = request.env.cr.dbname
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url += '/helpdesk/tickett/%s' % (self.id)
        #self.ticket_url = base_url
        reponse_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        reponse_url += '/helpdesk/reponse/tickett/%s' % (self.id)
        #self.reponse_url = reponse_url
        mail_template = self.env.ref('custom_helpdesk.email_template_traitement_manager')

        message_text = f'<p><strong>Voici le lien de votre ticket: <a href="'+str(base_url)+'">'+str(self.name)+'</a> </strong></p> ' \
                               f'<p><strong>Vous pouvez écrire votre réponse en cliquant sur ce lien: <a href="'+str(reponse_url)+'">'+str(self.name)+'</a </strong></p> ' \
                               

                

        mail_context = {

            'email_to': self.partner_email,
            'body': message_text,
            #'body_html': 'Voici le lien de votre ticket ' +base_url+'<br/>' 'Vous pouvez écrire votre réponse en cliquant sur ce lien '+reponse_url

        }

        #mail_template.sudo().send_mail(self.id, email_values=mail_context, force_send=True)
        
        vals = {
                    'body_html': message_text,
                    #'subject': mail_template.subject,
                    'email_to': self.partner_email,
                    'auto_delete': True,
                    'email_from': mail_template.email_from,
                    }
        mail_id = self.env['mail.mail'].sudo().create(vals)
        mail_id.sudo().send()





        
                

    
    # def write(self, vals):
    #     result = super(HelpdeskTicketInherit, self).write(vals)
    #     if 'team_id' in vals:
    #         _logger.info('**************** ommmmaaarrrrrrr')
    #         mail_template = self.env.ref('custom_helpdesk.email_template_traitement_manager')
    #         dbname = request.env.cr.dbname
    #         base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #         base_url += '/helpdesk/tickett/%s' % (self.id)
    #         self.ticket_url = base_url
    #         reponse_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #         reponse_url += '/helpdesk/reponse/tickett/%s' % (self.id)
    #         self.reponse_url = reponse_url
    #             # _logger.info(list_emails)
    
           
    #     return result
    # @api.model_create_multi
    # def create(self, list_value):
    #     # result = super(HelpdeskTicketInherit, self).create(list_value)
    #     # for vals in list_value:
    #     #     if self.team_id.equipe == 'support_rh' and 'x_studio_adresse_mail_du_n1' in vals:
    #     #         mail_template = self.env.ref('custom_helpdesk.email_template_traitement_manager')
    #     #         dbname = request.env.cr.dbname
    #     #         base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #     #         base_url += '/helpdesk/tickett/%s' % (self.id)
    #     #         self.ticket_url = base_url
    #     #         reponse_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #     #         reponse_url += '/helpdesk/reponse/tickett/%s' % (self.id)
    #     #         #self.reponse_url = reponse_url
    #     #             # _logger.info(list_emails)
    
    #     #         mail_context = {
    
    #     #                     'email_to': self.x_studio_adresse_mail_du_n1,
    #     #                     #'body_html': f"BODY FOR TRAITEMENT PRESTATAIRE TO C2S \n vous avez une nouvelle " + "<a href='" + base_url + "'>Ticket</a>" + " à remplir : "
    
    #     #                 }
    
    #     #         mail_template.sudo().send_mail(self.id, email_values=mail_context, force_send=True)
    #     now = fields.Datetime.now()
    #     # determine user_id and stage_id if not given. Done in batch.
    #     teams = self.env['helpdesk.team'].browse([vals['team_id'] for vals in list_value if vals.get('team_id')])
    #     team_default_map = dict.fromkeys(teams.ids, dict())
    #     for team in teams:
    #         team_default_map[team.id] = {
    #             'stage_id': team._determine_stage()[team.id].id,
    #             'user_id': team._determine_user_to_assign()[team.id].id
    #         }

    #     # Manually create a partner now since 'generate_recipients' doesn't keep the name. This is
    #     # to avoid intrusive changes in the 'mail' module
    #     # TDE TODO: to extract and clean in mail thread
    #     for vals in list_value:
    #         partner_id = vals.get('partner_id', False)
    #         partner_name = vals.get('partner_name', False)
    #         partner_email = vals.get('partner_email', False)
    #         if partner_name and partner_email and not partner_id:
    #             parsed_name, parsed_email = self.env['res.partner']._parse_partner_name(partner_email)
    #             if not parsed_name:
    #                 parsed_name = partner_name
    #             if vals.get('team_id'):
    #                 team = self.env['helpdesk.team'].browse(vals.get('team_id'))
    #                 company = team.company_id.id
    #             else:
    #                 company = False

    #             vals['partner_id'] = self.env['res.partner'].with_context(default_company_id=company).find_or_create(
    #                 tools.formataddr((parsed_name, parsed_email))
    #             ).id

    #     # determine partner email for ticket with partner but no email given
    #     partners = self.env['res.partner'].browse([vals['partner_id'] for vals in list_value if 'partner_id' in vals and vals.get('partner_id') and 'partner_email' not in vals])
    #     partner_email_map = {partner.id: partner.email for partner in partners}
    #     partner_name_map = {partner.id: partner.name for partner in partners}

    #     for vals in list_value:
    #         vals['ticket_ref'] = self.env['ir.sequence'].sudo().next_by_code('helpdesk.ticket')
    #         if vals.get('team_id'):
    #             team_default = team_default_map[vals['team_id']]
    #             if 'stage_id' not in vals:
    #                 vals['stage_id'] = team_default['stage_id']
    #             # Note: this will break the randomly distributed user assignment. Indeed, it will be too difficult to
    #             # equally assigned user when creating ticket in batch, as it requires to search after the last assigned
    #             # after every ticket creation, which is not very performant. We decided to not cover this user case.
    #             if 'user_id' not in vals:
    #                 vals['user_id'] = team_default['user_id']
    #             if vals.get('user_id'):  # if a user is finally assigned, force ticket assign_date and reset assign_hours
    #                 vals['assign_date'] = fields.Datetime.now()
    #                 vals['assign_hours'] = 0

    #         # set partner email if in map of not given
    #         if vals.get('partner_id') in partner_email_map:
    #             vals['partner_email'] = partner_email_map.get(vals['partner_id'])
    #         # set partner name if in map of not given
    #         if vals.get('partner_id') in partner_name_map:
    #             vals['partner_name'] = partner_name_map.get(vals['partner_id'])

    #         if vals.get('stage_id'):
    #             vals['date_last_stage_update'] = now
    #         vals['oldest_unanswered_customer_message_date'] = now

    #     # context: no_log, because subtype already handle this
            
    #     tickets = super(HelpdeskTicketInherit, self).create(list_value)

    #     # make customer follower
    #     for ticket in tickets:
    #         if ticket.partner_id:
    #             ticket.message_subscribe(partner_ids=ticket.partner_id.ids)

    #         ticket._portal_ensure_token()
    #         if ticket.team_id.equipe == 'support_rh' and ticket.x_studio_adresse_mail_du_n1 != '':
    #             mail_template = ticket.env.ref('custom_helpdesk.email_template_traitement_manager')
    #             dbname = request.env.cr.dbname
    #             base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #             base_url += '/helpdesk/tickett/%s' % (ticket.id)
    #             _logger.info('**************** logtgggggggggggg')
    #             ticket.write({'ticket_url': base_url})
                
    #             self.ticket_url = base_url
    #             _logger.info('**************** logtgggggggggggg %s %s', self.ticket_url, self.name)
    #             reponse_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #             reponse_url += '/helpdesk/reponse/tickett/%s' % (self.id)
    #             ticket.write({'reponse_url': reponse_url})
    #             self.reponse_url = reponse_url
    #                 # _logger.info(list_emails)
    
    #             mail_context = {
    
    #                         'email_to': ticket.x_studio_adresse_mail_du_n1,
    #                         #'body_html': f"BODY FOR TRAITEMENT PRESTATAIRE TO C2S \n vous avez une nouvelle " + "<a href='" + base_url + "'>Ticket</a>" + " à remplir : "
    
    #                     }
    
    #             mail_template.sudo().send_mail(self.id, email_values=mail_context, force_send=True)
    #             _logger.info('**************** logtgggggggggggg %s',  mail_template.sudo().send_mail(self.id, email_values=mail_context, force_send=True))

    #     # apply SLA
    #     tickets.sudo()._sla_apply()

    #     return tickets
            
