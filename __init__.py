import requests
import time
import xlsxwriter

f = open("login.txt", "r")
[email, password, client_id, client_secret, bankin_device, bankin_version] = f.read().splitlines()

params = (
    ('email', email),
    ('password', password),
)

headers = {
    'Bankin-Version': bankin_version,
    'bankin-device': bankin_device,
    'Client-Id': client_id,
    'Client-Secret': client_secret,
}

response = requests.post('https://sync.bankin.com/v2/authenticate', headers=headers, params=params)
print(response.json())

token = response.json()['access_token']

headers = {
    'Bankin-Version': bankin_version,
    'Client-Id': client_id,
    'Client-Secret': client_secret,
    'Authorization': 'Bearer '+token,
}

workbook = xlsxwriter.Workbook('accounts.xlsx')
worksheet = workbook.add_worksheet()



get_account_balance_url = 'https://sync.bankin.com/v2/accounts'
r = requests.get(get_account_balance_url, headers=headers, params=(('limit', '200'),))
var = r.json()['resources']
for i in range(len(var)):
    worksheet.write(i, 0, var[i].get('id'))
    worksheet.write(i, 1, var[i].get('name'))
    worksheet.write(i, 2, var[i].get('balance'))
    worksheet.write(i, 3, var[i].get('updated_at'))
    print(var[i].get('id'))
    print(var[i].get('name'))
    print(var[i].get('balance'))
    print(var[i].get('updated_at'))

workbook.close()

response = requests.post('https://sync.bankin.com/v2/items/'+str(var[1].get('item').get('id'))+'/refresh', headers=headers)
print(response.status_code)
response = requests.get('https://sync.bankin.com/v2/items/'+str(var[1].get('item').get('id'))+'/refresh/status', headers=headers)
print(response.json())
while response.json()['status'] != 'finished':
    response = requests.get('https://sync.bankin.com/v2/items/'+str(var[1].get('item').get('id'))+'/refresh/status', headers=headers)
    print("retrieving data from banks")
    time.sleep(1)



