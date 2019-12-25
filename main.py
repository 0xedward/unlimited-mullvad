import re
import sys
import requests
from bs4 import BeautifulSoup


def main():
    try:
        r = requests.get("https://mullvad.net/en/account/create/", timeout=25)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, features="html.parser")
            new_mullvad_account_number = soup.find("div", id="account-ticket-inner").find(
                "h1", "title is-1 is-family-monospace").text
            if re.search(r'[0-9]{4}\s[0-9]{4}\s[0-9]{4}\s[0-9]{4}$', new_mullvad_account_number):
                print(new_mullvad_account_number)
                sys.exit(0)
            else:
                print("Error: Unable to find account number in response from Mullvad")
                sys.exit(1)
        else:
            print("Error: Status code was not 200")
            sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: Request to Mullvad timed out")
        sys.exit(1)
    except requests.exceptions.RequestException:
        print("Error: Unhandled response from Mullvad")
        sys.exit(1)
    except AttributeError:
        print("Error: HTML could not parse account number")
        sys.exit(1)

if __name__ == "__main__":
    main()

""" TODO
- make a flag (-s) for automatically generating new account number and switching Mullvad client over to new account number
- automatically generate new account number at a set interval (i.e. -i 3hrs)

Write tests:
- run main.py random number of times and make sure each time the account number is unique
"""
