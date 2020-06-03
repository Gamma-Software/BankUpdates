from bankin_interface import BankinInterface
from exceptions import PostGetErrors
import log


def store_balance():
    """ Main script to login, refresh the balance, save it in an excel file, logout"""

    # Open the login file and retrieve the personal data to login to Bankin account
    f = open("login.txt", "r")
    [email, password, client_id, client_secret, bankin_device, bankin_version] = f.read().splitlines()
    f.close()

    # Use the Bankin interface to login, refresh the balance, save it in an excel file, logout
    interface = BankinInterface(email, password, client_id, client_secret, bankin_device, bankin_version)
    try:
        if interface.authenticate():
            datas = interface.get_items_balance() # Get the latest balance of all the bankin accounts
            interface.logout()
    except PostGetErrors as error:
        print("error: " + error.message)


if __name__ == "__main__":
    # execute only if run as a script
    store_balance()
