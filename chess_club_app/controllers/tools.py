import os
import datetime
from chess_club_app.views import main_menu
from chess_club_app.views import player_menus
from chess_club_app.views import tournament_menus


def print_logo():
    """Prints the ascii-logo"""
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


def valid_menu_choice(answer, opt_num):
    """Checks if the users choice is valid
       valid -> returns: True
       invalid -> returns: False"""

    try:
        if answer == "":
            return False
        elif int(answer) > opt_num:
            return False
        else:
            return True
    except ValueError:
        print("     Enter the number of an option!")
        return False


def turn_back_to(current_class_name: str):
    """Turns back to the last Menu by calling the last Class before the current one.
       If current class = MainMenu -> it closes the Program"""

    if current_class_name == "MainMenu":
        cls()
        exit()
    elif current_class_name in ["PlayerMenu", "TournamentMenu"]:
        main_menu.MainMenu()

    elif current_class_name in [
        "AddNewPlayer",
        "ShowAllPlayers",
        "SearchPlayerMenu",
    ]:
        player_menus.PlayerMenu()

    elif current_class_name in [
        "EditPlayer",
        "DeletePlayer",
        "EditOrDelete"
    ]:
        player_menus.SearchPlayerMenu()

    elif current_class_name in [
        "NewTournament",
        "LoadTournament",
        "DeleteTournament"
    ]:
        tournament_menus.TournamentMenu()


def all_player_details(player):
    """Takes a player object and returns all
       (for the app user relevant) Details in a printable table"""

    player_details = (f"""
                     ID:          {player.doc_id}
                     First Name:  {player["first_name"]}
                     Last Name :  {player["last_name"]}
                     Birth Date:  {player["birth_date"]}
                     Sex:         {player["sex"]}
                     Rating:      {player["rating"]}
        """)
    return player_details


def valid_date(date_text):
    """Checks if a date String is in a valid format and returns False or True"""

    try:
        datetime.datetime.strptime(date_text, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def valid_sex(sex_text):
    """Checks if a string is m or f and returns False or True"""

    if sex_text == "F" or sex_text == "M":
        return True
    else:
        return False


def valid_rating(number_string):
    """Checks if number is a valid, not negative, int or float
       and returns False or True"""

    try:
        if float(number_string) >= 0:
            return True
        else:
            return False

    except ValueError:
        print("\n                     It has to be a 0 or positive number!")
        return False
