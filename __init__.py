from getAccounts.bankin_interface import BankinInterface
from getAccounts.exceptions import PostGetErrors
import sys


def usage():
    print()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hg:d", ["help", "store_balance", "show_balance"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in argv:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-st", "--store_balance"):
            f = open("login.txt", "r")
            [email, password, client_id, client_secret, bankin_device, bankin_version] = f.read().splitlines()

            interface = BankinInterface(email, password, client_id, client_secret, bankin_device, bankin_version)
            try:
                if interface.authenticate():
                    datas = interface.get_items_balance()
                    interface.logout()
            except PostGetErrors as error:
                print("error: " + error.message)
        elif opt in ("-sh", "--show_balance"):
            grammar = arg
        else:
            usage()
            sys.exit(2)


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)
