from get_account_api.log import log
from get_account_api.onedrive_interface import OnedriveInterface
from get_account_api.bankin_interface import BankinInterface
import path_files
import getpass
import os
import yaml


def init():
    create_folders()
    setup_onedrive()
    setup_bankin()


def create_folders():
    # If the get_account folders exists then create folder
    if not os.path.exists(path_files.temp_folder):
        log("Create folders temps_file in " + path_files.temp_folder)
        os.makedirs(path_files.temp_folder)

    if not os.path.exists(path_files.config_folder):
        log("Create folders configs in " + path_files.config_folder)
        os.makedirs(path_files.config_folder)


def setup_onedrive():
    log("Setup Onedrive Oauth")
    client_id = str(input("input onedrive client_id: "))
    client_secret = str(input("input onedrive client_secret: "))
    onedrive_uri = str(input("input onedrive onedrive_uri: "))

    onedrive_oauth = {'client_id': client_id, 'client_secret': client_secret, 'onedrive_uri': onedrive_uri}

    # Store in the corresponding yaml
    with open(path_files.onedrive_oauth, 'w') as file:
        yaml.dump(onedrive_oauth, file)

    # Test the connection
    onedrive_interface = OnedriveInterface(client_id, client_secret, onedrive_uri)
    if not onedrive_interface.authenticate():
        exit(0)
    else:
        log("Onedrive Oauth Successful")


def setup_bankin():
    log("Setup Bankin Oauth")
    email = str(input("input Bankin email: "))
    client_id = str(input("input Bankin client_id: "))
    client_secret = str(input("input Bankin client_secret: "))

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
        log("Onedrive Oauth Successful")


if __name__ == "__main__":
    init()
