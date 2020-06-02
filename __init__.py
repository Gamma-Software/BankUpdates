import xlsxwriter
from getAccounts.bankin_interface import BankinInterface
from getAccounts.exceptions import PostGetErrors

f = open("login.txt", "r")
[email, password, client_id, client_secret, bankin_device, bankin_version] = f.read().splitlines()

interface = BankinInterface(email, password, client_id, client_secret, bankin_device, bankin_version)
try:
    if interface.authenticate():
        datas = interface.get_items_balance()
        interface.logout()
except PostGetErrors as error:
    print("error: "+error.message)

workbook = xlsxwriter.Workbook('accounts.xlsx')
worksheet = workbook.add_worksheet()

for i, data in enumerate(datas):
    worksheet.write(i, 0, data.get('id'))
    worksheet.write(i, 1, data.get('name'))
    worksheet.write(i, 2, data.get('balance'))
    worksheet.write(i, 3, data.get('updated_at'))

workbook.close()
