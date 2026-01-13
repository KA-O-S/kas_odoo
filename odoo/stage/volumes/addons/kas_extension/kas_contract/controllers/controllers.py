# -*- coding: utf-8 -*-
# from odoo import http


# class KasExtension(http.Controller):
#     @http.route('/kas_extension/kas_extension', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kas_extension/kas_extension/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kas_extension.listing', {
#             'root': '/kas_extension/kas_extension',
#             'objects': http.request.env['kas_extension.kas_extension'].search([]),
#         })

#     @http.route('/kas_extension/kas_extension/objects/<model("kas_extension.kas_extension"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kas_extension.object', {
#             'object': obj
#         })

