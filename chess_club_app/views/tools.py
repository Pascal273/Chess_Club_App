import os
import datetime

import chess_club_app.views.main_menu as _main_menu


def print_logo():
    logo = """
   .::.
   _::_                                            _()_
 _/____\\_                                        _/____\\_
 \\      /                                        \\      /
  \\____/                                          \\____/
  (____)                                          (____)
   |  |                                            |  |
   |__|                                            |__|
  /    \\          ___| |__   ___  ___ ___         /    \\
 (______)        / __| '_ \\ / _ \\/ __/ __|       (______)
(________)      | (__| | | |  __/\\__ \\__ \\      (________)
/________\\       \\___|_| |_|\\___||___/___/      /________\\
    """
    print(logo)


def cls():
    """Clears the terminal"""
    os.system("cls" if os.name == "nt" else "clear")


def back(current_site):
    """Return to previous page"""
    if current_site in ["PlayerMenu", "TournamentMenu"]:
        _main_menu.MainMenu()


def valid_date(date_text):
    """Checks if a date String is in a valid format and returns False or True"""
    try:
        datetime.datetime.strptime(date_text, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def valid_sex(sex_text):
    """Checks if a string is m or f and returns False or True"""

    if sex_text == "f" or sex_text == "m":
        return True
    else:
        return False
