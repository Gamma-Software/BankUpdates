from get_account_api.bankin_interface import BankinInterface
from get_account_api.exceptions import PostGetErrors
from get_account_api.excel_interface import ExcelInterface
from get_account_api.onedrive_interface import OnedriveInterface
import get_account_api.parameters_parsing as conf
import getpass
import os


def store_balance():
    """ Main script to login, refresh the balance, save it in an excel file, logout"""

    # Open the login file and retrieve the personal data to login to Bankin account and Onedrive
    bankin_param = conf.parse_bankin_params("login/bankin_oauth.yml")
    onedrive_param = conf.parse_onedrive_params("login/onedrive_oauth.yml")

    # Get the password in the console
    password = getpass.getpass('Type your bankin password: ')
    
    # Use the Bankin interface to login, refresh the balance, save it in an excel file, logout
    bankin_interface = BankinInterface(bankin_param["email"], password,
                                       bankin_param["client_id"], bankin_param["client_secret"])
    onedrive_interface = OnedriveInterface(onedrive_param["client_id"], onedrive_param["client_secret"],
                                           onedrive_param["onedrive_uri"])

    # Authenticate to onedrive
    onedrive_interface.authenticate()

    # If the get_account folders exists then create folder
    if os.path.exists(os.path.join(os.getenv('HOME'), '/.get_account')):
        os.mkdir(os.path.join(os.getenv('HOME'), '/.get_account/temp_file'))

    # Download the file
    onedrive_interface.download_file('accounts.xlsx',
                                     os.path.join(os.getenv('HOME'), '/.get_account/temp_file/accounts.xlsx'))

    try:
        if bankin_interface.authenticate():
            if bankin_interface.refresh_items(bankin_interface.get_items_ids()):
                data = bankin_interface.get_items_balance()  # Get the latest balance of all the bankin accounts
                bankin_interface.logout()
                excel_interface = ExcelInterface('accounts.xlsx')
                excel_interface.save_in_excel(data)
                onedrive_interface.upload_file("accounts.xlsx", os.path.join(os.path.dirname(__file__), 'accounts.xlsx'))
    except PostGetErrors as error:
        print("error: " + error.message)


if __name__ == "__main__":
    store_balance()
