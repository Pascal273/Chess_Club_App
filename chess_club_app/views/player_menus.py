from time import sleep

import chess_club_app.views.views_tools as tools
from chess_club_app.controllers.database_operator import DatabaseOperator


class PlayerMenu:
    """Displays options for player operations"""

    def __init__(self):
        """ PlayerMenu Constructor"""

        self.title = "Player Menu"
        self.options = {
            "Add a new player": AddNewPlayer,
            "Show all players": ShowAllPlayers,
            "Edit Player": EditPlayer,
            "Delete player": DeletePlayer
        }
        self.player_main_menu()

    def player_main_menu(self):
        """Shows the player main menu"""

        tools.cls()
        tools.print_logo()
        tools.print_menu(self.title, self.options, self.__class__.__name__)


class AddNewPlayer:
    """New player creator"""

    def __init__(self):
        """New player constructor"""

        self.title = "Create new Player"

        self.first_name = ""
        self.last_name = ""
        self.birth_date = ""
        self.sex = ""
        self.rating = "-1"

        self.enter_player_details()
        self.check_details()

    def enter_player_details(self):
        """ask user for the details of the new player"""

        tools.cls()
        tools.print_logo()
        tools.print_menu(title=self.title, current_site=self.__class__.__name__)

        while len(self.first_name) < 2:
            self.first_name = input(
                "     Whats the players first name?:                ").capitalize()

        while len(self.last_name) < 2:
            self.last_name = input(
                "     Whats the players last name?:                 ").capitalize()

        while not tools.valid_date(self.birth_date):
            self.birth_date = input(
                "     Whats the players birth date? (DD.MM.YYYY)?:  ")

        while not tools.valid_sex(self.sex):
            self.sex = input(
                "     Whats the players sex? (M/F):                 ").lower()

        while not tools.valid_number(self.rating):
            self.rating = input(
                "     Whats the players current rating?:            ")

    def check_details(self):
        """1. Displays the all the players details
        2. Asks user if it's all correct
        3. If user answers 'yes' the player gets saved.
           If if user answers 'no' the player doesn't get saved.
        """

        tools.print_menu(title=self.title)

        print(f"""
        Name:             {self.first_name} {self.last_name}
        Date of Birth:    {self.birth_date}
        Sex:              {self.sex}
        Rating:           {self.rating}
        """)

        if input("     Are details about the new player correct? (Y/N) "
                 ).lower() == "y":
            self.save_player()
        else:
            PlayerMenu()

    def save_player(self):
        """Saves new Player in the database"""

        DatabaseOperator().save_player(
            first_name=self.first_name,
            last_name=self.last_name,
            birth_date=self.birth_date,
            sex=self.sex,
            rating=self.rating
        )
        print(f"     {self.first_name} {self.last_name} added to the Database")
        sleep(3)
        PlayerMenu()


class ShowAllPlayers:

    def __init__(self):
        self.title = "List of all Players"
        self.options = {
            "Add a new player": AddNewPlayer,
            "Edit Player": EditPlayer,
            "Delete player": DeletePlayer
        }
        self.all_players_list = DatabaseOperator().load_all_players()
        self.show_all()

    def show_all(self):
        tools.cls()
        tools.print_logo()
        tools.print_menu(title=self.title)

        for player in self.all_players_list:
            print(tools.all_player_details(player))

        tools.print_menu(options=self.options, current_site=self.__class__.__name__)


class EditPlayer:
    """ 1. Search for a player after taking any information
        2. If mor than one match: displays all players with a match
           and asks to pick a player
        3. User gets to pick witch detail he wants to change.
        """

    def __init__(self):
        self.title = "Edit Player"
        self.options = [
            "Search for First Name",
            "Search for Last Name",
            "Search for Birthdate",
            "Search for Rating",
            "Search for Sex"
        ]
        self.show_options()
        self.ask_user()

    def show_options(self):
        """Displays the available Options"""

        tools.cls()
        tools.print_logo()
        tools.print_menu(title=self.title)

    def ask_user(self):
        answer = input("                What would you like to do? ")

        if answer == "1":
            self.search_for("first_name")

        elif answer == "2":
            self.search_for("last_name")

        elif answer == "3":
            self.search_for("birth_date")

        elif answer == "4":
            self.search_for("rating")

        elif answer == "5":
            self.search_for("sex")

        else:
            self.ask_user()

    def search_for(self, wanted_key):
        wanted_value = input(
            f"\n                Player {wanted_key.replace('_', ' ').capitalize()}: ")
        matches = DatabaseOperator().search_for(wanted_key, wanted_value)

        if len(matches) == 0:
            print("     No Player with that first name found!")
            sleep(3)
            EditPlayer()

        elif len(matches) > 1:
            for player in matches:
                print(tools.all_player_details(player))

            id_num = ""
            while not id_num.isnumeric():
                id_num = input("     Several matches found! Pick a player by ID!  ")
            self.player_editor(matches[int(id_num) - 1])

        else:
            self.player_editor(matches[0])

    def player_editor(self, player_object):
        title = "Player Editor"
        options = [
            "First Name",
            "Last Name",
            "Birthdate",
            "Sex",
            "Ranking"
        ]
        tools.cls()
        tools.print_logo()
        tools.print_menu(title, options, self.__class__.__name__)
        print(tools.all_player_details(player_object))


class DeletePlayer:

    def __init__(self):
        pass
