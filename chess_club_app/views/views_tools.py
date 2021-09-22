import os
import datetime

import chess_club_app.views.main_menu as _main_menu
import chess_club_app.views.player_menus as _player_menu
import chess_club_app.views.tournament_menus as _tournament_menus


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


def print_menu(title="title", options="dict of options: classes", current_site="MainMenu"):
    """Prints the menu and adds the option numbers automatically
       If no current_site is given it will show the option to close the program.
       If no title is given, it will show no title.
       If no options are given, it will not show options.

       Args:
           Headline = str
           options = dict of options: classes
           current_site = self.__class__.__name__
    """

    turn_back_option = "Close Program"

    if options == "dict of options: classes":
        options = {}

    if current_site in ["PlayerMenu", "TournamentMenu"]:
        turn_back_option = "Return Home"

    elif current_site in ["AddNewPlayer", "ShowAllPlayers", "EditPlayer", "DeletePlayer"]:
        turn_back_option = "Return to Player Menu"

    elif current_site in ["NewTournament", "LoadTournament", "DeleteTournament"]:
        turn_back_option = "Return to Tournament Menu"

    title_size = "---------------------"
    menu_spacer = "                     "
    dashes = int((len(title_size) - len(title)) / 2) * "-"
    title_layout = f"{menu_spacer}{dashes}{title}{dashes}"
    opt_num = 1
    option_rows = ""
    option_keys = []
    if len(options) == 0:
        menu = f"\n{title_layout}\n"
        print(menu)

    else:
        for option, command in options.items():
            option_rows += f"{menu_spacer}[{opt_num}] {option}\n"
            option_keys.append(option)
            opt_num += 1

        if title == "title":
            menu = f"\n{option_rows}\n\n{menu_spacer}[0] {turn_back_option}\n"

        else:
            menu = f"\n{title_layout}\n\n{option_rows}\n\n{menu_spacer}[0] {turn_back_option}\n"
        print(menu)

        answer = ""

        while not valid_menu_answer(answer, opt_num):
            answer = int(input("                  What would you like to do? "))

        if answer == 0:
            turn_back_to(current_site)

        else:
            options.get(option_keys[answer-1])()


def all_player_details(player):
    player_details = (f"""
                     ID:          {player.doc_id}
                     First Name:  {player["first_name"]}
                     Last Name :  {player["last_name"]}
                     Birth Date:  {player["birth_date"]}
                     Sex:         {player["sex"]}
                     Rating:      {player["rating"]}
        """)
    return player_details


def home_screen():
    """Opens the MainMenu """

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


def valid_number(number_string):
    """Checks if number is a valid, not negative, int or float
    and returns False or True"""

    try:
        if float(number_string) >= 0:
            return True
        else:
            return False
    except ValueError:
        print("     It has to be a positive number")
        return False


def valid_menu_answer(answer, opt_num):
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


def turn_back_to(current_site=str):
    """Turns back to the last Menu by calling a Class"""
    if current_site == "MainMenu":
        cls()
        exit()
    elif current_site in ["PlayerMenu", "TournamentMenu"]:
        _main_menu.MainMenu()

    elif current_site in ["AddNewPlayer", "ShowAllPlayers", "EditPlayer", "DeletePlayer"]:
        _player_menu.PlayerMenu()

    elif current_site in ["NewTournament", "LoadTournament", "DeleteTournament"]:
        _tournament_menus.TournamentMenu()
