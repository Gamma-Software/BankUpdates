import os


get_account_folder = os.path.expanduser('~/.get_account/')
temp_folder = os.path.join(get_account_folder, 'temp_file/')
config_folder = os.path.join(get_account_folder, 'configs/')
bankin_oauth = os.path.join(config_folder, 'bankin_oauth.yml')
onedrive_oauth = os.path.join(config_folder, 'onedrive_oauth.yml')
setup_options = os.path.join(config_folder, 'setup_options.yml')
account_filename = '../accounts.xlsx'
data_temp_file = os.path.join(temp_folder, account_filename)
