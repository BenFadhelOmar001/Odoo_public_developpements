# -*- coding: utf-8 -*-
from odoo import http

# class ViewListForProjects(http.Controller):
#     @http.route('/view_list_for_projects/view_list_for_projects/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/view_list_for_projects/view_list_for_projects/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('view_list_for_projects.listing', {
#             'root': '/view_list_for_projects/view_list_for_projects',
#             'objects': http.request.env['view_list_for_projects.view_list_for_projects'].search([]),
#         })

#     @http.route('/view_list_for_projects/view_list_for_projects/objects/<model("view_list_for_projects.view_list_for_projects"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('view_list_for_projects.object', {
#             'object': obj
#         })