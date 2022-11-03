# -*- coding: utf-8 -*-
from odoo import http
import json
from werkzeug import Response

class vitApi(http.Controller):

    @http.route('/vit_api/list/<string:model_name>', auth='public')
    def list(self, model_name, **kw):
        domain = kw.get('domain',[])
        fields = kw.get('fields','[]')
        fields=eval(fields)
        results = http.request.env[model_name].sudo().search_read(domain,fields=fields)
        headers = {'Content-Type': 'application/json'}
        return Response(json.dumps(results,indent=4, sort_keys=True, default=str), headers=headers)

    @http.route('/vit_api/read/<string:model_name>/<int:id>', auth='public')
    def read(self, model_name, id, **kw):
        results = http.request.env[model_name].sudo().search_read([('id','=',id)])
        headers = {'Content-Type': 'application/json'}
        return Response(json.dumps(results, indent=4, sort_keys=True, default=str), headers=headers)

    @http.route('/vit_api/create/<string:model_name>', auth='public', csrf=False)
    def create(self, model_name, **kw):
        data = kw.get('data', '{}')
        data = eval(data)
        results = http.request.env[model_name].sudo().create(data)
        headers = {'Content-Type': 'application/json'}
        return Response(json.dumps(results, indent=4, sort_keys=True, default=str), headers=headers)

