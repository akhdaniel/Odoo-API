# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json

class partner(models.Model):
    _inherit = 'res.partner'

    def get_external_contacts(self):
        res = requests.get('https://reqres.in/api/users?page=2')
        response = res.text
        response_json = json.loads(response)
        data = response_json['data']
        for d in data:
            self.env['res.partner'].create({
                'parent_id': self.id,
                'type':'contact',
                'email': d['email'],
                'name': '{} {}'.format(d['first_name'],d['last_name']),
            })

