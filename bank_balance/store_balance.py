from bank_balance.library.bankininterface import BankinInterface
from bank_balance.library import PostGetErrors, pathfiles
from bank_balance.library.excelinterface import ExcelInterface
from bank_balance.library import OnedriveInterface
import bank_balance.library.parametersparsing as conf
from bank_balance.library.log import log
import getpass
import os


def store_balance():
    """ Main script to login, refresh the balance, save it in an excel file, logout"""

    # Check whether the setup is done
    if not os.path.exists(pathfiles.get_account_folder):
        log('Please run <python setup_oath.py> to setup your Onedrive and Bankin oauth configs')
        exit(0)

    # Read options
    options = conf.parse_setup_options(pathfiles.setup_options)

    # Open the login file and retrieve the personal data to login to Bankin account and Onedrive
    bankin_param = conf.parse_bankin_params(pathfiles.bankin_oauth)

    # Get the password in the console
    password = getpass.getpass('Type your bankin password: ')
    
    # Use the Bankin interface to login, refresh the balance, save it in an excel file, logout
    bankin_interface = BankinInterface(bankin_param['email'], password,
                                       bankin_param['client_id'], bankin_param['client_secret'])

    # Save the path in temp folder
    excel_path = path_files.data_temp_file

    if options['save'] == 'onedrive':
        onedrive_param = conf.parse_onedrive_params(pathfiles.onedrive_oauth)
        onedrive_interface = OnedriveInterface(onedrive_param['client_id'], onedrive_param['client_secret'],
                                               onedrive_param['onedrive_uri'])

        # Authenticate to onedrive
        if not onedrive_interface.authenticate():
            exit(0)

        # Download the file
        onedrive_interface.download_file(path_files.account_filename, path_files.data_temp_file)
    else:
        if options['local_path'] != 'none':
            excel_path = options['local_path']

    try:
        if bankin_interface.authenticate():
            if bankin_interface.refresh_items():
                data = bankin_interface.get_items_balance()  # Get the latest balance of all the bankin accounts
                bankin_interface.logout()
                excel_interface = ExcelInterface(excel_path, path_files.account_filename)
                excel_interface.save_in_excel(data)

                if options['save'] == 'onedrive':
                    onedrive_interface.upload_file(pathfiles.account_filename, pathfiles.data_temp_file)
                if options['send'] == 'email':
                    print('wip')
    except PostGetErrors as error:
        print('error: ' + error.message)


if __name__ == '__main__':
    store_balance()
