import xlsxwriter
import pandas as pd


def save_in_excel(data: pd.DataFrame):
    writer = pd.ExcelWriter('accounts.xlsx', engine='xlsxwriter', datetime_format='mmm d yyyy hh:mm:ss',
                        date_format='mmmm dd yyyy')

    data.to_excel(writer, sheet_name='Sheet1', index=False)

    writer.save()
