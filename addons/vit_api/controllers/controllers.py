# -*- coding: utf-8 -*-
# from odoo import http


# class /mnt/extra-addons/vitApi(http.Controller):
#     @http.route('//mnt/extra-addons/vit_api//mnt/extra-addons/vit_api/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//mnt/extra-addons/vit_api//mnt/extra-addons/vit_api/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/mnt/extra-addons/vit_api.listing', {
#             'root': '//mnt/extra-addons/vit_api//mnt/extra-addons/vit_api',
#             'objects': http.request.env['/mnt/extra-addons/vit_api./mnt/extra-addons/vit_api'].search([]),
#         })

#     @http.route('//mnt/extra-addons/vit_api//mnt/extra-addons/vit_api/objects/<model("/mnt/extra-addons/vit_api./mnt/extra-addons/vit_api"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/mnt/extra-addons/vit_api.object', {
#             'object': obj
#         })
