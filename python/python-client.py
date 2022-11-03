# https://github.com/akhdaniel/Odoo-API.git

url = 'http://localhost:8069'
db = '14ee'
username = 'admin'
password = '1'

import xmlrpc.client
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
partner_ids = models.execute_kw(db, uid, password, 
    'res.partner', 'search', 
    [
        [['is_company', '=', True]]
    ], 
    {'offset': 0, 'limit': 5})
print(partner_ids)

count = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[['is_company', '=', True]]])
print(count)