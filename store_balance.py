from bankin_interface import BankinInterface
from exceptions import PostGetErrors
import log


def store_balance():
    f = open("login.txt", "r")
    [email, password, client_id, client_secret, bankin_device, bankin_version] = f.read().splitlines()
    f.close()

    interface = BankinInterface(email, password, client_id, client_secret, bankin_device, bankin_version)
    try:
        if interface.authenticate():
            datas = interface.get_items_balance()
            interface.logout()
    except PostGetErrors as error:
        print("error: " + error.message)


if __name__ == "__main__":
    # execute only if run as a script
    store_balance()
