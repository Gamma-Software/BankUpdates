import requests
import time
from getAccounts.exceptions import PostGetErrors
from getAccounts.log import log
import pandas as pd


class BankinInterface:
    api_bankin_url = 'https://sync.bankin.com/v2/'
    authenticate_url = api_bankin_url+'authenticate'
    accounts_url = api_bankin_url+'accounts'
    items_url = api_bankin_url+'items'
    logout_url = api_bankin_url+'logout'
    settings_url = api_bankin_url+'users/me/settings'

    def __init__(self, email, password, client_id, client_secret):
        self.params = (
            ("email", email),
            ("password", password),
        )
        self.headers = {
            'bankin-version': '2019-02-18',
            'bankin-device': '1304aa81-936b-4a9a-bb48-22cf94b9e679',
            'client-id': client_id,
            'client-secret': client_secret
        }
        self.timeout = 20
        self.item = {}

    def authenticate(self):
        log("Authenticate")
        response = requests.post(self.authenticate_url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise PostGetErrors(response.status_code, "error raised on authenticate")
        self.headers.update({'Authorization': 'Bearer ' + response.json()['access_token']})
        return self.check_bankin_account()

    def refresh_item(self, item_to_refresh):
        log("Refresh bank account")
        response = requests.post(self.items_url + item_to_refresh + '/refresh', headers=self.headers)
        if response.status_code != 200:
            raise PostGetErrors(response.status_code, "error raised on refreshing")
        response = requests.get(self.items_url + item_to_refresh + '/refresh/status', headers=self.headers)
        self.timeout = 20
        while response.json()['status'] != 'finished':
            response = requests.get(self.items_url + item_to_refresh + '/refresh/status', headers=self.headers)
            print("Retrieving data from banks; timeout after " + str(self.timeout) + "s")
            time.sleep(1)
            self.timeout -= 1
            if self.timeout <= 0:
                return False
        log("Bank accounts updated")
        return True

    def refresh_items(self, items_to_refresh):
        for item_to_refresh in items_to_refresh:
            if not self.refresh_item(item_to_refresh):
                return False
        return True

    def get_items_ids(self):
        self.item = {}
        for account in self.get_items_response_json():
            self.item.update({'item': account.get('item').get('id')})

    def get_items_response_json(self):
        response = requests.get(self.accounts_url, headers=self.headers, params=(('limit', '200'),))
        if response.status_code != 200:
            raise PostGetErrors(response.status_code, "error raised on getting the items")
        return response.json()['resources']

    def get_items_balance(self):
        log("Retrieved items balance")
        data = []
        for account in self.get_items_response_json():
            data_to_add = {}
            data_to_add.update({'id': account.get('item').get('id')})
            data_to_add.update({'name': account.get('name')})
            data_to_add.update({'balance': account.get('balance')})
            data_to_add.update({'updated_at': account.get('updated_at')})
            data.append(data_to_add)
        return pd.from_dict(data)

    def logout(self):
        log("logout user")
        response = requests.post(self.logout_url, headers=self.headers)
        if response.status_code != 200:
            raise PostGetErrors(response.status_code, "error raised on logout")

    def check_bankin_account(self):
        log("check user")
        response = requests.get(self.settings_url, headers=self.headers)
        if response.status_code != 200:
            raise PostGetErrors(response.status_code, "error raised on checking the user's login")
        return response.json()['email_valid']

