import requests
import time
settings = {
    'url':'http://localhost:8069',
    'db':'14ee',
    'login':'admin',
    'password':'1',

}

def vit_rest_login(settings):
    try:
        url="{}/session/auth/login".format(settings['url'])

        data = {
            'db':settings['db'],
            'login': settings['login'],
            'password': settings['password']
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        res = requests.post(url, json=data, headers=headers).json()
        return res['session']['sid']
    except Exception as e:
        print(str(e))        



def vit_rest_create_invoice(sid, settings):

    url = "{}/vit_rest/private/invoice/create".format(settings['url'])
    
    try:
        data = {
            "name": "INV/TEST/001",
            "ref": "INV/TEST/001",
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "description": "testing invoice create from API",
            "amount_due": 1000000,
            "currency":{
                "id":2,
                "name":"USD",
            },
            "partner": {
                "id": 7
            },
            "company": {
                "id": 1
            }
        }
        headers = {
            'X-Openerp-Session-Id': sid
        }
        json_data = requests.post(url, json=data, headers=headers).json()
        return json_data
        
    except Exception as e:
        print(str(e))


sid = vit_rest_login(settings)
print('sid',sid)
res = vit_rest_create_invoice(sid, settings)
print('res',res)

