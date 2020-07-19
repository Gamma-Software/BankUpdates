from bank_balance.library.log import log
from bank_balance.library import pathfiles
from bank_balance.library.exceptions import PostGetErrors
from bank_balance.library.bankininterface import BankinInterface
from bank_balance.library.onedriveinterface import OnedriveInterface
import bank_balance.library.parametersparsing as conf
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
    elif args.send == 'none':
        setup_options('send', 'none')
    elif args.save == 'local':
        setup_options('save', 'local')
    elif args.save == 'onedrive':
        setup_options('save', 'onedrive')
    elif args.oauth == 'bankin':
        setup_bankin()
    elif args.oauth == 'onedrive':
        setup_onedrive()
    else:
        setup_bankin()
        if input('Do you want to setup onedrive ? (y/n)') == 'y':
            setup_onedrive()


def create_folders():
    # If the get_account folders exists then create folder
    if not os.path.exists(pathfiles.temp_folder):
        log('Create folders temps_file in ' + pathfiles.temp_folder)
        os.makedirs(pathfiles.temp_folder)

    if not os.path.exists(pathfiles.config_folder):
        log('Create folders configs in ' + pathfiles.config_folder)
        os.makedirs(pathfiles.config_folder)

    # Create empty yaml
    # Onedrive oauth
    onedrive_oauth = {'client_id': 'none', 'client_secret': 'none', 'onedrive_uri': 'none'}
    with open(pathfiles.onedrive_oauth, 'w') as file:
        yaml.dump(onedrive_oauth, file)

    # Bankin oauth
    bankin_oauth = {'email': 'none', 'client_id': 'none', 'client_secret': 'none'}
    with open(pathfiles.bankin_oauth, 'w') as file:
        yaml.dump(bankin_oauth, file)

    # Options
    options = {'send': 'none', 'save': 'local', 'local_path': 'none'}
    yaml.dump(options, file)


def setup_options(option, value):
    log('Setup Options')

    # Read option Yaml or create
    options = conf.parse_setup_options(pathfiles.setup_options)

    # Replace the option
    options[option] = value
    log('Set '+option+' to: ' + value)

    # Ask where to save in local
    if value == 'local':
        if input('Do you want to change the path ? (current local path: ' + options['local_path'] + ') yes/no: ') \
                != 'no':
            path_to_save_local = input('Where do you want to save in local: ')
            options['local_path'] = path_to_save_local
            log('Set local_path to: ' + path_to_save_local)
        print(options)

    # Save the option in the corresponding yaml
    with open(pathfiles.setup_options, 'w') as file:
        yaml.dump(options, file)


def setup_onedrive():
    log('Setup Onedrive Oauth')
    client_id = str(input('input onedrive client_id: '))
    client_secret = str(input('input onedrive client_secret: '))
    onedrive_uri = str(input('input onedrive onedrive_uri: '))

    onedrive_oauth = {'client_id': client_id, 'client_secret': client_secret, 'onedrive_uri': onedrive_uri}

    # Store in the corresponding yaml
    with open(pathfiles.onedrive_oauth, 'w') as file:
        yaml.dump(onedrive_oauth, file)

    # Test the connection
    onedrive_interface = OnedriveInterface(client_id, client_secret, onedrive_uri)
    if not onedrive_interface.authenticate():
        log('Onedrive Oauth unsuccessful')
        if input('Do you want to try again ? (y/n)') == 'y':
            setup_bankin()
    else:
        log('Onedrive Oauth Successful')


def setup_bankin():
    log('Setup Bankin Oauth')
    email = str(input('input Bankin email: '))
    client_id = str(input('input Bankin client_id: '))
    client_secret = str(input('input Bankin client_secret: '))

    bankin_oauth = {'email': email, 'client_id': client_id, 'client_secret': client_secret}

    # Store in the corresponding yaml
    with open(pathfiles.bankin_oauth, 'w') as file:
        yaml.dump(bankin_oauth, file)

    # Test the connection
    # Get the password in the console
    password = getpass.getpass('Type your bankin password: ')
    bankin_interface = BankinInterface(email, password, client_id, client_secret)
    try:
        if bankin_interface.authenticate():
            log('Bankin Oauth Successful')
    except PostGetErrors:
        log('Bankin Oauth unsuccessful')
        if input('Do you want to try again ? (y/n)') == 'y':
            setup_bankin()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    init(parser)
