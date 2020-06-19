from get_account_api.log import log
from get_account_api.onedrive_interface import OnedriveInterface
from get_account_api.bankin_interface import BankinInterface
import get_account_api.parameters_parsing as conf
import path_files
import getpass
import os
import yaml
import argparse


def init(parser):
    # If not created create the folders
    create_folders()

    parser.add_argument('--all', action='store_true', help='Setup the whole system')
    parser.add_argument('--oauth', type=str, choices=['bankin', 'onedrive'], help='Authentication setup')
    parser.add_argument('--save', type=str, choices=['local', 'onedrive'], help='Save the data in local or in onedrive')
    parser.add_argument('--send', type=str, choices=['email', 'none'], help='Set an option to send an email or not')
    args = parser.parse_args()
    if args.send == 'email':
        setup_options('send', 'email')
    if args.send == 'none':
        setup_options('send', 'none')
    if args.save == 'local':
        setup_options('save', 'local')
    if args.save == 'onedrive':
        setup_options('save', 'onedrive')
    if args.oauth == 'bankin':
        setup_bankin()
    if args.oauth == 'onedrive':
        setup_onedrive()
    else:
        setup_bankin()
        setup_onedrive()


def create_folders():
    # If the get_account folders exists then create folder
    if not os.path.exists(path_files.temp_folder):
        log('Create folders temps_file in ' + path_files.temp_folder)
        os.makedirs(path_files.temp_folder)

    if not os.path.exists(path_files.config_folder):
        log('Create folders configs in ' + path_files.config_folder)
        os.makedirs(path_files.config_folder)

    # Create empty yaml
    # Onedrive oauth
    onedrive_oauth = {'client_id': 'none', 'client_secret': 'none', 'onedrive_uri': 'none'}
    with open(path_files.onedrive_oauth, 'w') as file:
        yaml.dump(onedrive_oauth, file)

    # Bankin oauth
    bankin_oauth = {'email': 'none', 'client_id': 'none', 'client_secret': 'none'}
    with open(path_files.bankin_oauth, 'w') as file:
        yaml.dump(bankin_oauth, file)

    # Options
    options = {'send': 'none', 'save': 'local'}
    with open(path_files.setup_options, 'w') as file:
        yaml.dump(options, file)


def setup_options(option, value):
    log('Setup Options')

    # Read option Yaml or create
    options = conf.parse_setup_options(path_files.setup_options)

    # Replace the option
    options[option] = value
    log('Set '+option+' to: ' + value)

    # Save the option in the corresponding yaml
    with open(path_files.setup_options, 'w') as file:
        yaml.dump(options, file)


def setup_onedrive():
    log('Setup Onedrive Oauth')
    client_id = str(input('input onedrive client_id: '))
    client_secret = str(input('input onedrive client_secret: '))
    onedrive_uri = str(input('input onedrive onedrive_uri: '))

    onedrive_oauth = {'client_id': client_id, 'client_secret': client_secret, 'onedrive_uri': onedrive_uri}

    # Store in the corresponding yaml
    with open(path_files.onedrive_oauth, 'w') as file:
        yaml.dump(onedrive_oauth, file)

    # Test the connection
    onedrive_interface = OnedriveInterface(client_id, client_secret, onedrive_uri)
    if not onedrive_interface.authenticate():
        exit(0)
    else:
        log('Onedrive Oauth Successful')


def setup_bankin():
    log('Setup Bankin Oauth')
    email = str(input('input Bankin email: '))
    client_id = str(input('input Bankin client_id: '))
    client_secret = str(input('input Bankin client_secret: '))

    bankin_oauth = {'email': email, 'client_id': client_id, 'client_secret': client_secret}

    # Store in the corresponding yaml
    with open(path_files.bankin_oauth, 'w') as file:
        yaml.dump(bankin_oauth, file)

    # Test the connection
    # Get the password in the console
    password = getpass.getpass('Type your bankin password: ')
    bankin_interface = BankinInterface(email, password, client_id, client_secret)
    if bankin_interface.authenticate():
        exit(0)
    else:
        log('Onedrive Oauth Successful')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    init(parser)
