import os
import datetime

import chess_club_app.views.main_menu as main_menu
import chess_club_app.views.player_menus as player_menu
import chess_club_app.views.tournament_menus as tournament_menu


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


class MenuScreen:
    """Creates the menu incl. Title, available options
    and causes an action after the user choice

    Args:
         title = str
         options = dict of options(str): classes(obj) or List of Options(str)
         current_site = self.__class__.__name__
         (returns the name of the class that called it)

         If no current_site is given it will show the option to close the program.
         If no title is given, it will show no title.
         If no options are given, it will not show options.
         """

    def __init__(
            self,
            title: str = None,
            options: dict or list = None,
            current_site: str = None):

        self.title = title
        self.options = options
        self.current_site = current_site

        self.title_size = "---------------------"
        self.menu_spacer = "                     "
        self.dashes = int((len(self.title_size) - len(title)) / 2) * "-"
        self.title_layout = f"{self.menu_spacer}{self.dashes}{self.title}{self.dashes}"
        self.opt_num = 1
        self.option_rows = ""
        self.option_keys = []

    def print_menu(self, title_only: bool = False, options_only: bool = False):
        """Prints the menu and adds the option numbers automatically
            If title_only = True, only the title will be printed!
            If options_only = True, only the Options will be printed!

            Args:
                    title_only: bool (default set to False)
                    options_only: bool (default set to False)
        """

        if not self.options:
            self.options = {}

        turn_back_option = ""

        if not self.current_site:
            turn_back_option = "Return"

        elif self.current_site == "MainMenu":
            turn_back_option = "Close Program"

        elif self.current_site in ["PlayerMenu", "TournamentMenu"]:
            turn_back_option = "Return Home"

        elif self.current_site in [
            "AddNewPlayer",
            "ShowAllPlayers",
            "SearchPlayerMenu",
        ]:
            turn_back_option = "Return to Player Menu"

        elif self.current_site in [
            "EditPlayer",
            "DeletePlayer",
            "EditOrDelete"
        ]:
            turn_back_option = "Return to Search Player Menu"

        elif self.current_site in ["NewTournament", "LoadTournament", "DeleteTournament"]:
            turn_back_option = "Return to Tournament Menu"

        if len(self.options) == 0 or title_only:
            menu = f"\n{self.title_layout}\n"
            print(menu)

        else:
            if type(self.options) is list:
                for option in self.options:
                    self.option_rows += f"{self.menu_spacer}[{self.opt_num}] {option}\n"
                    self.option_keys.append(option)
                    self.opt_num += 1

            else:
                for option, command in self.options.items():
                    self.option_rows += f"{self.menu_spacer}[{self.opt_num}] {option}\n"
                    self.option_keys.append(option)
                    self.opt_num += 1

            if not self.title or options_only:
                menu = f"\n{self.option_rows}\n\n{self.menu_spacer}[0] {turn_back_option}\n"

            else:
                menu = f"\n{self.title_layout}\n\n{self.option_rows}\n\n{self.menu_spacer}[0] {turn_back_option}\n"

            print(menu)

    def user_action(self):

        answer = ""

        while not valid_menu_choice(answer, self.opt_num):
            answer = int(input(f"{self.menu_spacer}What would you like to do? "))

        if answer == 0:
            turn_back_to(self.current_site)

        else:
            self.options.get(self.option_keys[answer-1])()


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
        player_menu.PlayerMenu()

    elif current_class_name in [
        "EditPlayer",
        "DeletePlayer",
        "EditOrDelete"
    ]:
        player_menu.SearchPlayerMenu()

    elif current_class_name in [
        "NewTournament",
        "LoadTournament",
        "DeleteTournament"
    ]:
        tournament_menu.TournamentMenu()


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
