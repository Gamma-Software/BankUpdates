import requests
import time
from bank_balance.library.exceptions import PostGetErrors
from bank_balance.library.log import log
import json


class BankinInterface:
    api_bankin_url = 'https://sync.bankin.com/v2/'
    authenticate_url = api_bankin_url+'authenticate'
    accounts_url = api_bankin_url+'accounts'
    bank_url = api_bankin_url+'banks'
    items_url = api_bankin_url+'items'
    logout_url = api_bankin_url+'logout'
    settings_url = api_bankin_url+'users/me/settings'

    def __init__(self, email, password, client_id, client_secret):
        self.params = (
            ('email', email),
            ('password', password),
        )
        self.headers = {
            'bankin-version': '2019-02-18',
            'bankin-device': '1304aa81-936b-4a9a-bb48-22cf94b9e679',
            'client-id': client_id,
            'client-secret': client_secret
        }
        self.timeout = 120
        self.item = {}

    def authenticate(self):
        """ Authenticate the user"""
        log('Authenticate')
        response = requests.post(self.authenticate_url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise PostGetErrors(response.status_code, 'error raised on authenticate')
        self.headers.update({'Authorization': 'Bearer ' + response.json()['access_token']})
        return self.check_bankin_account()

    def refresh_items(self):
        """ Refresh all the items"""
        log('Refresh bank accounts')

        # Store the url
        url = self.items_url + '/refresh'

        # Ask for item refresh
        response = requests.post(url, headers=self.headers)
        if response.status_code != 200 and response.status_code != 202:
            raise PostGetErrors(response.status_code, 'error raised on refreshing')

        refreshed = False
        while not refreshed:
            # Check if the item is refreshed
            response = requests.get(url + '/status', headers=self.headers)

            # While the item is not refreshed check for its status every second for 20 seconds
            refresh_response = json.loads(response.content.decode('utf-8'))['resources']

            refreshed = True
            for response in refresh_response:
                if response['status'] == 'finished':
                    continue
                if response['status'] != 'finished':
                    refreshed = False
                if response['status'] == 'finished_error':
                    print("Error on refresh")
                    return True

            print('Retrieving data from banks; timeout after ' + str(self.timeout) + 's')
            time.sleep(1)
            self.timeout -= 1
            if self.timeout <= 0:
                print('Retrieving data from banks; Timeout ! Please try to connect to your bankin account'
                      ' on the web and understand the issue')
                return False
        log('Bank accounts updated')
        return True

    def get_items_ids(self):
        """ Get all the items ids"""
        items_id = []
        for account in self.get_items_response_json():
            items_id.append(account.get('item').get('id'))
        return items_id

    def get_items_response_json(self):
        """ Get all the items response"""
        response = requests.get(self.accounts_url, headers=self.headers, params=(('limit', '200'),))
        if response.status_code != 200:
            raise PostGetErrors(response.status_code, "error raised on getting the items")
        return response.json()['resources']

    def get_items_balance(self):
        """ Get all the items balance and store them in a useful DataFrame"""
        log('Retrieved items balance')
        items = self.get_items_response_json()
        return items

    def logout(self):
        """ Logout the user"""
        log('logout user')
        response = requests.post(self.logout_url, headers=self.headers)
        if response.status_code != 200:
            raise PostGetErrors(response.status_code, 'error raised on logout')

    def check_bankin_account(self):
        """ Check the validity of the user's email"""
        log('check user')
        response = requests.get(self.settings_url, headers=self.headers)
        if response.status_code != 200:
            raise PostGetErrors(response.status_code, "error raised on checking the user's login")
        return response.json()['email_valid']

