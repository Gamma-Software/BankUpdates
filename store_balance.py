from getAccounts.bankin_interface import BankinInterface
from getAccounts.exceptions import PostGetErrors
from getAccounts.excel_interface import ExcelInterface


def store_balance():
    """ Main script to login, refresh the balance, save it in an excel file, logout"""

    # Open the login file and retrieve the personal data to login to Bankin account
    f = open("login.txt", "r")
    [email, password, client_id, client_secret] = f.read().splitlines()
    f.close()

    # Use the Bankin interface to login, refresh the balance, save it in an excel file, logout
    bankin_interface = BankinInterface(email, password, client_id, client_secret)
    try:
        if bankin_interface.authenticate():
            if bankin_interface.refresh_items(bankin_interface.get_items_ids()):
                data = bankin_interface.get_items_balance()  # Get the latest balance of all the bankin accounts
                bankin_interface.logout()
                excel_interface = ExcelInterface('accounts.xlsx')
                excel_interface.save_in_excel(data)
    except PostGetErrors as error:
        print("error: " + error.message)


if __name__ == "__main__":
    # execute only if run as a script
    store_balance()
