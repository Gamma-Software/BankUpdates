import xlsxwriter
import pandas as pd


def save_in_excel(data: pd.DataFrame):
    writer = pd.ExcelWriter('accounts.xlsx', engine='xlsxwriter', datetime_format='mmm d yyyy hh:mm:ss',
                        date_format='mmmm dd yyyy')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    data.to_excel("accounts.xlsx", sheet_name='Sheet1')

    writer.save()
