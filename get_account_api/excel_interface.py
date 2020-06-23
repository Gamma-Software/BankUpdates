import pandas as pd
from os import path


def clean_data(data):
    # Get the first item to create the base of the data frame
    account = data[0]
    name = account.get('name')
    if account.get('custom_name') is not None:
        name = account.get('custom_name')
    dataframe_to_return = pd.DataFrame({
        'timestamp': [pd.Timestamp(account.get('updated_at')).floor('min').tz_convert(None)],
        name + ': ' + str(account.get('item').get('id')): [account.get('balance')]})

    # Skip the first iteration
    iteraccount = iter(data)
    next(iteraccount)

    # Get the other items and merge them in the DataFrame
    for account in iteraccount:
        name = account.get('name')
        if account.get('custom_name') is not None:
            name = account.get('custom_name')
        df = pd.DataFrame({
            'timestamp': [pd.Timestamp(account.get('updated_at')).floor('min').tz_convert(None)],
            name + ': ' + str(account.get('item').get('id')): [account.get('balance')]})
        dataframe_to_return = pd.merge(dataframe_to_return, df, on='timestamp', how='outer')

    # Clean dataframe
    dataframe_to_return.sort_values(by='timestamp', inplace=True)
    return dataframe_to_return


class ExcelInterface:
    def __init__(self, path, file_name):
        self.file_name = file_name
        self.path = path

    def read_excel_in_pd(self):
        """ Read the current dataframe"""
        current_dataframe = pd.DataFrame()
        if path.exists(self.path):
            current_dataframe = pd.read_excel(self.path, index_col=None)
        return current_dataframe

    def save_in_excel(self, data):
        writer = pd.ExcelWriter(self.path, engine='xlsxwriter',
                                datetime_format='mmm d yyyy hh:mm:ss',
                                date_format='mmmm dd yyyy')

        # Clean the data frame
        cleaned_data = clean_data(data)

        # Read the current dataframe
        if not self.read_excel_in_pd().empty:
            current_dataframe = pd.read_excel(self.path, index_col=None)
            merged_dataframe = pd.merge(current_dataframe, cleaned_data, on='timestamp', how='outer')
        else:
            merged_dataframe = cleaned_data
        merged_dataframe.to_excel(writer, sheet_name='Sheet1', index=False)

        # Save and close
        writer.close()
