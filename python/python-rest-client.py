import requests

# r = requests.get('http://localhost:8069/vit_api/list/res.partner?fields=["id","email"]')
# print(r.text)

# r = requests.get('http://localhost:8069/vit_api/read/res.partner/10')
# print(r.text)

r = requests.post('http://localhost:8069/vit_api/create/res.partner',
        data={'data': '{"name":"Test API 2"}'}
    )
print(r.text)


