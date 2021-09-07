# -*- coding: utf-8 -*-
from odoo import http

# class XxxXxx(http.Controller):
#     @http.route('/xxx_xxx/xxx_xxx/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/xxx_xxx/xxx_xxx/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('xxx_xxx.listing', {
#             'root': '/xxx_xxx/xxx_xxx',
#             'objects': http.request.env['xxx_xxx.xxx_xxx'].search([]),
#         })

#     @http.route('/xxx_xxx/xxx_xxx/objects/<model("xxx_xxx.xxx_xxx"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('xxx_xxx.object', {
#             'object': obj
#         })