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


class CustomerPortalInherit(portal.CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortalInherit, self)._prepare_portal_layout_values()
        _logger.info('*********** values %s', values)
        return values

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'ticket_count' in counters:
            if request.env.user.group_hr_manager_data:

                values['ticket_countt'] = (
                    request.env['helpdesk.ticket'].sudo().search_count(self._prepare_helpdesk_tickets_domainn())

                    if request.env['helpdesk.ticket'].check_access_rights('read', raise_exception=False)
                    else 0
                )

            else:
                values['ticket_countt'] = 0

            if request.env.user.group_it_manager_data:

                values['ticket_counttt'] = (
                    request.env['helpdesk.ticket'].sudo().search_count(self._prepare_helpdesk_tickets_domainnn())

                    if request.env['helpdesk.ticket'].check_access_rights('read', raise_exception=False)
                    else 0
                )
                values['ticket_count_md'] = (
                    request.env['helpdesk.ticket'].sudo().search_count(self._prepare_helpdesk_tickets_domain_md())

                    if request.env['helpdesk.ticket'].check_access_rights('read', raise_exception=False)
                    else 0
                )

            else:
                values['ticket_counttt'] = 0
                values['ticket_count_md'] = 0
                
            if request.env.user.group_demande_recrutement_demandeur:

                values['ticket_count_demande_recrutement'] = (
                    request.env['helpdesk.ticket'].sudo().search_count(self._prepare_helpdesk_tickets_domain_demande_recrutement())

                    if request.env['helpdesk.ticket'].check_access_rights('read', raise_exception=False)
                    else 0
                )
            else:

                values['ticket_count_demande_recrutement'] = 0

        

            # if request.env.user.group_it_manager_data and request.env.user.group_hr_manager_data:
            #
            #     values['ticket_count'] = (
            #         request.env['helpdesk.ticket'].sudo().search_count([])
            #
            #         if request.env['helpdesk.ticket'].check_access_rights('read', raise_exception=False)
            #         else 0
            #     )
            #
            # else:
            #     values['ticket_count'] = 0


        return values

    def _prepare_helpdesk_tickets_domainn(self):
        curent_user_id = request.env.user.id
        _logger.info('*********** curent_user_id %s', curent_user_id)
        curent_user_record = request.env['res.users'].sudo().search([('id', '=',curent_user_id )])
        _logger.info('*********** curent_user_record %s', curent_user_record)
        _logger.info('*********** curent_user_record.partner_id %s', curent_user_record.partner_id)



        return [('team_id.equipe', '=', 'support_rh'), ('partner_id', '=', curent_user_record.partner_id.id)]

    def _prepare_helpdesk_tickets_domainnn(self):
        curent_user_id = request.env.user.id
        _logger.info('*********** curent_user_id %s', curent_user_id)
        curent_user_record = request.env['res.users'].sudo().search([('id', '=',curent_user_id )])
        _logger.info('*********** curent_user_record %s', curent_user_record)
        _logger.info('*********** curent_user_record.partner_id %s', curent_user_record.partner_id)
        



        return [('team_id.equipe', '=', 'service_clientele'), ('partner_id', '=', curent_user_record.partner_id.id)]
        
    def _prepare_helpdesk_tickets_domain_md(self):
        curent_user_id = request.env.user.id
        _logger.info('*********** curent_user_id %s', curent_user_id)
        curent_user_record = request.env['res.users'].sudo().search([('id', '=',curent_user_id )])
        _logger.info('*********** curent_user_record %s', curent_user_record)
        _logger.info('*********** curent_user_record.partner_id %s', curent_user_record.partner_id)



        return [('team_id.equipe', '=', 'master_data'), ('partner_id', '=', curent_user_record.partner_id.id)]

    def _prepare_helpdesk_tickets_domain_demande_recrutement(self):
        curent_user_id = request.env.user.id
        _logger.info('*********** curent_user_id %s', curent_user_id)
        curent_user_record = request.env['res.users'].sudo().search([('id', '=',curent_user_id )])
        _logger.info('*********** curent_user_record %s', curent_user_record)
        _logger.info('*********** curent_user_record.partner_id %s', curent_user_record.partner_id)



        return [('team_id.equipe', '=', 'demande_recrutement'), ('partner_id', '=', curent_user_record.partner_id.id)]

    def _ticket_get_page_view_valuess(self, ticket, access_token, **kwargs):
        values = {
            'page_name': 'ticket',
            'ticket': ticket,
            'ticket_link_section': [],
        }
        return self._get_page_view_values(ticket, access_token, values, 'my_tickets_history', False, **kwargs)

    def _ticket_get_page_view_valuess_demande_recrutement(self, ticket, access_token, **kwargs):
        values = {
            'page_name': 'ticket',
            'ticket': ticket,
            'ticket_link_section': [],
        }
        return self._get_page_view_values(ticket, access_token, values, 'my_tickets_history', False, **kwargs)

    def _prepare_my_tickets_valuesss(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None, groupby='none', search_in='content'):
        values = self._prepare_portal_layout_values()
        domain = self._prepare_helpdesk_tickets_domainnn()

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'reference': {'label': _('Reference'), 'order': 'id'},
            'name': {'label': _('Subject'), 'order': 'name'},
            'user': {'label': _('Assigned to'), 'order': 'user_id'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
            'update': {'label': _('Last Stage Update'), 'order': 'date_last_stage_update desc'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'assigned': {'label': _('Assigned'), 'domain': [('user_id', '!=', False)]},
            'unassigned': {'label': _('Unassigned'), 'domain': [('user_id', '=', False)]},
            'open': {'label': _('Open'), 'domain': [('close_date', '=', False)]},
            'closed': {'label': _('Closed'), 'domain': [('close_date', '!=', False)]},
        }
        searchbar_inputs = {
            'content': {'input': 'content', 'label': Markup(_('Search <span class="nolabel"> (in Content)</span>'))},
            'id': {'input': 'id', 'label': _('Search in Reference')},
            'message': {'input': 'message', 'label': _('Search in Messages')},
            'user': {'input': 'user', 'label': _('Search in Assigned to')},
            'status': {'input': 'status', 'label': _('Search in Stage')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'stage': {'input': 'stage_id', 'label': _('Stage')},
            'user': {'input': 'user_id', 'label': _('Assigned to')},
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if filterby in ['last_message_sup', 'last_message_cust']:
            discussion_subtype_id = request.env.ref('mail.mt_comment').id
            messages = request.env['mail.message'].search_read([('model', '=', 'helpdesk.ticket'), ('subtype_id', '=', discussion_subtype_id)], fields=['res_id', 'author_id'], order='date desc')
            last_author_dict = {}
            for message in messages:
                if message['res_id'] not in last_author_dict:
                    last_author_dict[message['res_id']] = message['author_id'][0]

            ticket_author_list = request.env['helpdesk.ticket'].sudo().search_read(fields=['id', 'partner_id'])
            ticket_author_dict = dict([(ticket_author['id'], ticket_author['partner_id'][0] if ticket_author['partner_id'] else False) for ticket_author in ticket_author_list])

            last_message_cust = []
            last_message_sup = []
            ticket_ids = set(last_author_dict.keys()) & set(ticket_author_dict.keys())
            for ticket_id in ticket_ids:
                if last_author_dict[ticket_id] == ticket_author_dict[ticket_id]:
                    last_message_cust.append(ticket_id)
                else:
                    last_message_sup.append(ticket_id)

            if filterby == 'last_message_cust':
                domain = AND([domain, [('id', 'in', last_message_cust)]])
            else:
                domain = AND([domain, [('id', 'in', last_message_sup)]])

        else:
            domain = AND([domain, searchbar_filters[filterby]['domain']])

        if date_begin and date_end:
            domain = AND([domain, [('create_date', '>', date_begin), ('create_date', '<=', date_end)]])

        # search
        if search and search_in:
            search_domain = []
            if search_in == 'id':
                search_domain = OR([search_domain, [('id', 'ilike', search)]])
            if search_in == 'content':
                search_domain = OR([search_domain, ['|', ('name', 'ilike', search), ('description', 'ilike', search)]])
            if search_in == 'user':
                search_domain = OR([search_domain, [('user_id', 'ilike', search)]])
            if search_in == 'message':
                discussion_subtype_id = request.env.ref('mail.mt_comment').id
                search_domain = OR([search_domain, [('message_ids.body', 'ilike', search), ('message_ids.subtype_id', '=', discussion_subtype_id)]])
            if search_in == 'status':
                search_domain = OR([search_domain, [('stage_id', 'ilike', search)]])
            domain = AND([domain, search_domain])

        # pager
        tickets_count = request.env['helpdesk.ticket'].sudo().search_count(domain)
        pager = portal_pager(
            url="/my/ticketsss",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'search_in': search_in, 'search': search, 'groupby': groupby, 'filterby': filterby},
            total=tickets_count,
            page=page,
            step=self._items_per_page
        )

        tickets = request.env['helpdesk.ticket'].sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_tickets_history'] = tickets.ids[:100]

        if groupby != 'none':
            grouped_tickets = [request.env['helpdesk.ticket'].concat(*g) for k, g in groupbyelem(tickets, itemgetter(searchbar_groupby[groupby]['input']))]
        else:
            grouped_tickets = [tickets]

        values.update({
            'date': date_begin,
            'grouped_tickets': grouped_tickets,
            'page_name': 'ticket',
            'default_url': '/my/ticketsss',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_filters': searchbar_filters,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_groupby': searchbar_groupby,
            'sortby': sortby,
            'groupby': groupby,
            'search_in': search_in,
            'search': search,
            'filterby': filterby,
        })
        return values

    def _prepare_my_tickets_values_md(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None, groupby='none', search_in='content'):
        values = self._prepare_portal_layout_values()
        domain = self._prepare_helpdesk_tickets_domain_md()

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'reference': {'label': _('Reference'), 'order': 'id'},
            'name': {'label': _('Subject'), 'order': 'name'},
            'user': {'label': _('Assigned to'), 'order': 'user_id'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
            'update': {'label': _('Last Stage Update'), 'order': 'date_last_stage_update desc'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'assigned': {'label': _('Assigned'), 'domain': [('user_id', '!=', False)]},
            'unassigned': {'label': _('Unassigned'), 'domain': [('user_id', '=', False)]},
            'open': {'label': _('Open'), 'domain': [('close_date', '=', False)]},
            'closed': {'label': _('Closed'), 'domain': [('close_date', '!=', False)]},
        }
        searchbar_inputs = {
            'content': {'input': 'content', 'label': Markup(_('Search <span class="nolabel"> (in Content)</span>'))},
            'id': {'input': 'id', 'label': _('Search in Reference')},
            'message': {'input': 'message', 'label': _('Search in Messages')},
            'user': {'input': 'user', 'label': _('Search in Assigned to')},
            'status': {'input': 'status', 'label': _('Search in Stage')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'stage': {'input': 'stage_id', 'label': _('Stage')},
            'user': {'input': 'user_id', 'label': _('Assigned to')},
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if filterby in ['last_message_sup', 'last_message_cust']:
            discussion_subtype_id = request.env.ref('mail.mt_comment').id
            messages = request.env['mail.message'].search_read([('model', '=', 'helpdesk.ticket'), ('subtype_id', '=', discussion_subtype_id)], fields=['res_id', 'author_id'], order='date desc')
            last_author_dict = {}
            for message in messages:
                if message['res_id'] not in last_author_dict:
                    last_author_dict[message['res_id']] = message['author_id'][0]

            ticket_author_list = request.env['helpdesk.ticket'].sudo().search_read(fields=['id', 'partner_id'])
            ticket_author_dict = dict([(ticket_author['id'], ticket_author['partner_id'][0] if ticket_author['partner_id'] else False) for ticket_author in ticket_author_list])

            last_message_cust = []
            last_message_sup = []
            ticket_ids = set(last_author_dict.keys()) & set(ticket_author_dict.keys())
            for ticket_id in ticket_ids:
                if last_author_dict[ticket_id] == ticket_author_dict[ticket_id]:
                    last_message_cust.append(ticket_id)
                else:
                    last_message_sup.append(ticket_id)

            if filterby == 'last_message_cust':
                domain = AND([domain, [('id', 'in', last_message_cust)]])
            else:
                domain = AND([domain, [('id', 'in', last_message_sup)]])

        else:
            domain = AND([domain, searchbar_filters[filterby]['domain']])

        if date_begin and date_end:
            domain = AND([domain, [('create_date', '>', date_begin), ('create_date', '<=', date_end)]])

        # search
        if search and search_in:
            search_domain = []
            if search_in == 'id':
                search_domain = OR([search_domain, [('id', 'ilike', search)]])
            if search_in == 'content':
                search_domain = OR([search_domain, ['|', ('name', 'ilike', search), ('description', 'ilike', search)]])
            if search_in == 'user':
                search_domain = OR([search_domain, [('user_id', 'ilike', search)]])
            if search_in == 'message':
                discussion_subtype_id = request.env.ref('mail.mt_comment').id
                search_domain = OR([search_domain, [('message_ids.body', 'ilike', search), ('message_ids.subtype_id', '=', discussion_subtype_id)]])
            if search_in == 'status':
                search_domain = OR([search_domain, [('stage_id', 'ilike', search)]])
            domain = AND([domain, search_domain])

        # pager
        tickets_count = request.env['helpdesk.ticket'].sudo().search_count(domain)
        pager = portal_pager(
            url="/my/ticketsss",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'search_in': search_in, 'search': search, 'groupby': groupby, 'filterby': filterby},
            total=tickets_count,
            page=page,
            step=self._items_per_page
        )

        tickets = request.env['helpdesk.ticket'].sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_tickets_history'] = tickets.ids[:100]

        if groupby != 'none':
            grouped_tickets = [request.env['helpdesk.ticket'].concat(*g) for k, g in groupbyelem(tickets, itemgetter(searchbar_groupby[groupby]['input']))]
        else:
            grouped_tickets = [tickets]

        values.update({
            'date': date_begin,
            'grouped_tickets': grouped_tickets,
            'page_name': 'ticket',
            'default_url': '/my/ticketsss',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_filters': searchbar_filters,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_groupby': searchbar_groupby,
            'sortby': sortby,
            'groupby': groupby,
            'search_in': search_in,
            'search': search,
            'filterby': filterby,
        })
        return values

    def _prepare_my_tickets_values_demande_recrutement(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None, groupby='none', search_in='content'):
        values = self._prepare_portal_layout_values()
        domain = self._prepare_helpdesk_tickets_domain_demande_recrutement()

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'reference': {'label': _('Reference'), 'order': 'id'},
            'name': {'label': _('Subject'), 'order': 'name'},
            'user': {'label': _('Assigned to'), 'order': 'user_id'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
            'update': {'label': _('Last Stage Update'), 'order': 'date_last_stage_update desc'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'assigned': {'label': _('Assigned'), 'domain': [('user_id', '!=', False)]},
            'unassigned': {'label': _('Unassigned'), 'domain': [('user_id', '=', False)]},
            'open': {'label': _('Open'), 'domain': [('close_date', '=', False)]},
            'closed': {'label': _('Closed'), 'domain': [('close_date', '!=', False)]},
        }
        searchbar_inputs = {
            'content': {'input': 'content', 'label': Markup(_('Search <span class="nolabel"> (in Content)</span>'))},
            'id': {'input': 'id', 'label': _('Search in Reference')},
            'message': {'input': 'message', 'label': _('Search in Messages')},
            'user': {'input': 'user', 'label': _('Search in Assigned to')},
            'status': {'input': 'status', 'label': _('Search in Stage')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'stage': {'input': 'stage_id', 'label': _('Stage')},
            'user': {'input': 'user_id', 'label': _('Assigned to')},
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if filterby in ['last_message_sup', 'last_message_cust']:
            discussion_subtype_id = request.env.ref('mail.mt_comment').id
            messages = request.env['mail.message'].search_read([('model', '=', 'helpdesk.ticket'), ('subtype_id', '=', discussion_subtype_id)], fields=['res_id', 'author_id'], order='date desc')
            last_author_dict = {}
            for message in messages:
                if message['res_id'] not in last_author_dict:
                    last_author_dict[message['res_id']] = message['author_id'][0]

            ticket_author_list = request.env['helpdesk.ticket'].sudo().search_read(fields=['id', 'partner_id'])
            ticket_author_dict = dict([(ticket_author['id'], ticket_author['partner_id'][0] if ticket_author['partner_id'] else False) for ticket_author in ticket_author_list])

            last_message_cust = []
            last_message_sup = []
            ticket_ids = set(last_author_dict.keys()) & set(ticket_author_dict.keys())
            for ticket_id in ticket_ids:
                if last_author_dict[ticket_id] == ticket_author_dict[ticket_id]:
                    last_message_cust.append(ticket_id)
                else:
                    last_message_sup.append(ticket_id)

            if filterby == 'last_message_cust':
                domain = AND([domain, [('id', 'in', last_message_cust)]])
            else:
                domain = AND([domain, [('id', 'in', last_message_sup)]])

        else:
            domain = AND([domain, searchbar_filters[filterby]['domain']])

        if date_begin and date_end:
            domain = AND([domain, [('create_date', '>', date_begin), ('create_date', '<=', date_end)]])

        # search
        if search and search_in:
            search_domain = []
            if search_in == 'id':
                search_domain = OR([search_domain, [('id', 'ilike', search)]])
            if search_in == 'content':
                search_domain = OR([search_domain, ['|', ('name', 'ilike', search), ('description', 'ilike', search)]])
            if search_in == 'user':
                search_domain = OR([search_domain, [('user_id', 'ilike', search)]])
            if search_in == 'message':
                discussion_subtype_id = request.env.ref('mail.mt_comment').id
                search_domain = OR([search_domain, [('message_ids.body', 'ilike', search), ('message_ids.subtype_id', '=', discussion_subtype_id)]])
            if search_in == 'status':
                search_domain = OR([search_domain, [('stage_id', 'ilike', search)]])
            domain = AND([domain, search_domain])

        # pager
        tickets_count = request.env['helpdesk.ticket'].sudo().search_count(domain)
        pager = portal_pager(
            url="/my/ticketsss",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'search_in': search_in, 'search': search, 'groupby': groupby, 'filterby': filterby},
            total=tickets_count,
            page=page,
            step=self._items_per_page
        )

        tickets = request.env['helpdesk.ticket'].sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_tickets_history'] = tickets.ids[:100]

        if groupby != 'none':
            grouped_tickets = [request.env['helpdesk.ticket'].concat(*g) for k, g in groupbyelem(tickets, itemgetter(searchbar_groupby[groupby]['input']))]
        else:
            grouped_tickets = [tickets]

        values.update({
            'date': date_begin,
            'grouped_tickets': grouped_tickets,
            'page_name': 'ticket',
            'default_url': '/my/ticketsss',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_filters': searchbar_filters,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_groupby': searchbar_groupby,
            'sortby': sortby,
            'groupby': groupby,
            'search_in': search_in,
            'search': search,
            'filterby': filterby,
        })
        return values

    @http.route(['/my/ticketsss', '/my/ticketsss/page/<int:page>'], type='http', auth="user", website=True)
    def my_helpdesk_ticketsss(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None, groupby='none', search_in='content', **kw):
        values = self._prepare_my_tickets_valuesss(page, date_begin, date_end, sortby, filterby, search, groupby, search_in)
        return request.render("custom_helpdesk_website.portal_helpdesk_tickettt", values)

    @http.route(['/my/ticket_md', '/my/ticket_md/page/<int:page>'], type='http', auth="user", website=True)
    def my_helpdesk_ticket_md(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None, groupby='none', search_in='content', **kw):
        values = self._prepare_my_tickets_values_md(page, date_begin, date_end, sortby, filterby, search, groupby, search_in)
        return request.render("custom_helpdesk_website.portal_helpdesk_ticket_md", values)

    @http.route(['/my/ticket_demande_recrutement', '/my/ticket_demande_recrutement/page/<int:page>'], type='http', auth="user", website=True)
    def my_helpdesk_ticket_demande_recrutement(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None, groupby='none', search_in='content', **kw):
        values = self._prepare_my_tickets_values_demande_recrutement(page, date_begin, date_end, sortby, filterby, search, groupby, search_in)
        return request.render("custom_helpdesk_website.portal_helpdesk_ticket_demande_recrutement", values)




    @http.route([
        "/helpdesk/tickettt/<int:ticket_id>",
        "/helpdesk/tickettt/<int:ticket_id>/<access_token>",
        '/my/tickettt/<int:ticket_id>',
        '/my/tickettt/<int:ticket_id>/<access_token>'
    ], type='http', auth="public", website=True)
    def tickets_followuppp(self, ticket_id=None, access_token=None, **kw):


        ticket_sudo = request.env['helpdesk.ticket'].sudo().search([('id', '=', ticket_id)])

        values = self._ticket_get_page_view_valuess(ticket_sudo, access_token, **kw)

        return request.render("custom_helpdesk_website.tickets_followuppp", values)

    @http.route([
        "/helpdesk/ticket_md/<int:ticket_id>",
        "/helpdesk/ticket_md/<int:ticket_id>/<access_token>",
        '/my/ticket_md/<int:ticket_id>',
        '/my/ticket_md/<int:ticket_id>/<access_token>'
    ], type='http', auth="public", website=True)
    def tickets_followup_md(self, ticket_id=None, access_token=None, **kw):


        ticket_sudo = request.env['helpdesk.ticket'].sudo().search([('id', '=', ticket_id)])

        values = self._ticket_get_page_view_valuess(ticket_sudo, access_token, **kw)

        return request.render("custom_helpdesk_website.tickets_followup_md", values)

    @http.route([
        "/helpdesk/ticket_demande_recrutement/<int:ticket_id>",
        "/helpdesk/ticket_demande_recrutement/<int:ticket_id>/<access_token>",
        '/my/ticket_demande_recrutement/<int:ticket_id>',
        '/my/ticket_demande_recrutement/<int:ticket_id>/<access_token>'
    ], type='http', auth="public", website=True)
    def tickets_followup_demande_recrutement(self, ticket_id=None, access_token=None, **kw):


        ticket_sudo = request.env['helpdesk.ticket'].sudo().search([('id', '=', ticket_id)])

        values = self._ticket_get_page_view_valuess_demande_recrutement(ticket_sudo, access_token, **kw)

        return request.render("custom_helpdesk_website.tickets_followup_demande_recrutement", values)




    @http.route([
        "/helpdesk/reponse/tickett/<int:ticket_id>",
        "/helpdesk/reponse/tickett/<int:ticket_id>/<access_token>",
        '/reponse/tickett/<int:ticket_id>',
        '/reponse/tickett/<int:ticket_id>/<access_token>'
    ], type='http', auth="public", website=True)
    def reponse_ticket(self, ticket_id=None, access_token=None, **kw):

        ticket_sudo = request.env['helpdesk.ticket'].sudo().search([('id', '=', ticket_id)])

        values = self._ticket_get_page_view_valuess(ticket_sudo, access_token, **kw)

        return request.render("custom_helpdesk_website.tickets_reponse", values)

    # @http.route(['/update/ticket'], type='http', auth="public", website=True, sitemap=False)
    # def update_webticket(self, **kw):
    #     nomad = False
    #     start = False
    #     aucun = False
    #     etafi = False
    #     kiryba = False
    #     wecheck = False
    #     aucun_f = False
    #     if 'nomad' in kw:
    #         if kw['nomad']=='on':
    #             nomad = True
    #             kw.update({'nomad': nomad})
    #     if 'start' in kw:
    #         if kw['start'] == 'on':
    #             start = True
    #             kw.update({'start': start})
    #     if 'aucun' in kw:
    #         if kw['aucun'] == 'on':
    #             aucun = True
    #             kw.update({'aucun': aucun})
    #     if 'kiryba' in kw:
    #         if kw['kiryba'] == 'on':
    #             kiryba = True
    #             kw.update({'kiryba': kiryba})
    #     if 'wecheck' in kw:
    #         if kw['wecheck'] == 'on':
    #             wecheck = True
    #             kw.update({'wecheck': wecheck})
    #     if 'etafi' in kw:
    #         if kw['etafi'] == 'on':
    #             etafi = True
    #             kw.update({'etafi': etafi})
    #     if 'aucun_f' in kw:
    #         if kw['aucun_f'] == 'on':
    #             aucun_f = True
    #             kw.update({'aucun_f': aucun_f})
    #
    #     ticket = request.env['helpdesk.ticket'].sudo().search([('id', '=', kw['id'])])
    #     collaborateur_id = request.env['res.partner'].search([('name', '=', kw['collaborateur'])], limit=1).id
    #     stage_id = request.env['helpdesk.stage'].search([('etape', '=', 'preparation_coordinateur_it')], limit=1).id
    #     kw.update({'collaborateur': collaborateur_id})
    #     ticket.write({'stage_id': stage_id, 'collaborateur': collaborateur_id, 'pc_housse': kw['pc_housse'], 'clavier_souris': kw['clavier_souris'], 'x_studio_smartphone': kw['x_studio_smartphone'], 'tablette_chargeur_housse_clavier': kw['tablette_chargeur_housse_clavier'], 'nomad': nomad, 'start': start, 'aucun': aucun, 'etafi': etafi, 'kyriba': kiryba, 'wecheck': wecheck, 'aucun_f': aucun_f, 'logiciel_conge': kw['logiciel_conge'], 'logiciel_paye': kw['logiciel_paye'], 'logiciel_sap': kw['logiciel_sap'], 'nom': kw['nom'], 'logiciel_sap_analytic': kw['logiciel_sap_analytic'], 'justification': kw['justification'], 'vehicule': kw['vehicule'], 'personne_vehicule': kw['personne_vehicule'], 'acces_dossier': kw['acces_dossier'], 'nom_reseau': kw['nom_reseau'], 'besoin_imprimante': kw['besoin_imprimante'], 'besoin_epi': kw['besoin_epi'], 'comment_manager': kw['comment_manager']})
    #     return request.render("custom_helpdesk_website.ticket_thankss", {})
    #
    # @http.route([
    #     '/my/tickett/close/<int:ticket_id>',
    #     '/my/tickett/close/<int:ticket_id>/<access_token>',
    # ], type='http', auth="public", website=True)
    # def ticket_closee(self, ticket_id=None, access_token=None, **kw):
    #     try:
    #         ticket_sudo = self._document_check_access('helpdesk.ticket', ticket_id, access_token)
    #     except (AccessError, MissingError):
    #         return request.redirect('/my')
    #
    #     if not ticket_sudo.team_id.allow_portal_ticket_closing:
    #         raise UserError(_("The team does not allow ticket closing through portal"))
    #
    #     if not ticket_sudo.closed_by_partner:
    #         closing_stage = ticket_sudo.team_id._get_closing_stage()
    #         if ticket_sudo.stage_id != closing_stage:
    #             ticket_sudo.write({'stage_id': closing_stage[0].id, 'closed_by_partner': True})
    #         else:
    #             ticket_sudo.write({'closed_by_partner': True})
    #         body = _('Ticket closed by the customer')
    #         ticket_sudo.with_context(mail_create_nosubscribe=True).message_post(body=body, message_type='comment', subtype_xmlid='mail.mt_note')
    #
    #     return request.redirect('/my/tickett/%s/%s' % (ticket_id, access_token or ''))
