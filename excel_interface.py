import pandas as pd


class ExcelInterface:
    def __init__(self, file_name):
        self.file_name = file_name

    def clean_data(self, data):
        # Get the first item to create the base of the data frame
        account = data[0]
        name = account.get('name')
        if account.get('custom_name') is not None:
            name = name + '  ' + account.get('custom_name')
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
                name = name + '  ' + account.get('custom_name')
            df = pd.DataFrame({
                'timestamp': [pd.Timestamp(account.get('updated_at')).floor('min').tz_convert(None)],
                name + ': ' + str(account.get('item').get('id')): [account.get('balance')]})
            dataframe_to_return = pd.merge(dataframe_to_return, df, on='timestamp', how='outer')

        # Clean dataframe
        dataframe_to_return.sort_values(by='timestamp', inplace=True)
        return dataframe_to_return

    def save_in_excel(self, data):
        writer = pd.ExcelWriter(self.file_name, engine='xlsxwriter',
                                datetime_format='mmm d yyyy hh:mm:ss',
                                date_format='mmmm dd yyyy')

        # Read the current dataframe
        current_dataframe = pd.read_excel(self.file_name, index_col=None)
        print(current_dataframe)

        merged_dataframe = pd.merge(current_dataframe, self.clean_data(data), on='timestamp', how='outer')

        merged_dataframe.to_excel(writer, sheet_name='Sheet1', index=False)

        writer.save()
