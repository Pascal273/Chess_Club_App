from time import sleep

import chess_club_app.controllers.menu_creator
import chess_club_app.controllers.tools as tools
from chess_club_app.controllers.database_operator import DatabaseOperator


class PlayerMenu:
    """Displays options for player related operations"""

    def __init__(self):
        """ PlayerMenu Constructor"""

        self.title = "Player Menu"
        self.options = {
            "Add a new player": AddNewPlayer,
            "Show all players": ShowAllPlayers,
            "Search Player": SearchPlayerMenu
        }
        self.player_main_menu()

    def player_main_menu(self):
        """Shows the player main menu"""

        tools.cls()
        tools.print_logo()
        menu = chess_club_app.controllers.menu_creator.MenuScreen(self.title, self.options, self.__class__.__name__)
        menu.print_menu()
        menu.user_action()


class AddNewPlayer:
    """New player creator"""

    def __init__(self):
        """New player constructor"""

        self.spacer = "\n                     "
        self.title = "Create new Player"

        self.first_name = ""
        self.last_name = ""
        self.birth_date = ""
        self.sex = ""
        self.rating = "-1"

        self.menu = chess_club_app.controllers.menu_creator.MenuScreen(title=self.title, current_site=self.__class__.__name__)
        self.enter_player_details()
        self.check_details()

    def enter_player_details(self):
        """ask user for the details of the new player"""

        tools.cls()
        tools.print_logo()
        self.menu.print_menu()

        while len(self.first_name) < 2:
            self.first_name = input(
                f"{self.spacer}Whats the players first name?:                ").capitalize()

        while len(self.last_name) < 2:
            self.last_name = input(
                f"{self.spacer}Whats the players last name?:                 ").capitalize()

        while not tools.valid_date(self.birth_date):
            self.birth_date = input(
                f"{self.spacer}Whats the players birth date? (DD.MM.YYYY)?:  ")

        while not tools.valid_sex(self.sex):
            self.sex = input(
                f"{self.spacer}Whats the players sex? (M/F):                 ").upper()

        while not tools.valid_rating(self.rating):
            self.rating = input(
                f"{self.spacer}Whats the players current rating?:            ")

    def check_details(self):
        """
        1. Displays the all the players details
        2. Asks user if it's all correct
        3. If user answers 'yes' the player gets saved.
           If if user answers 'no' the player doesn't get saved.
        """

        tools.cls()
        tools.print_logo()
        menu = chess_club_app.controllers.menu_creator.MenuScreen("Check and Approve")
        menu.print_menu()

        print(f"""
                Name:             {self.first_name} {self.last_name}
                Date of Birth:    {self.birth_date}
                Sex:              {self.sex}
                Rating:           {self.rating}
        """)

        if input(f"{self.spacer}Are details about the new player correct? (Y/N) "
                 ).lower() == "y":
            self.save_player()
            print(f"{self.spacer}{self.first_name} {self.last_name} added to the Database")
            sleep(3)
            PlayerMenu()
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


class ShowAllPlayers:

    def __init__(self):
        self.title = "List of all Players"
        self.options = {
            "Add a new player": AddNewPlayer,
            "Edit Player": SearchPlayerMenu,
            "Delete player": DeletePlayer
        }
        self.menu = chess_club_app.controllers.menu_creator.MenuScreen(self.title, self.options, self.__class__.__name__)
        self.all_players_list = DatabaseOperator().load_all_players()
        self.show_all()

    def show_all(self):
        tools.cls()
        tools.print_logo()
        self.menu.print_menu(title_only=True)

        if len(self.all_players_list) == 0:
            print("\n                     No Players in Database!")

        else:
            for player in self.all_players_list:
                print(tools.all_player_details(player))

        self.menu.print_menu(options_only=True)
        self.menu.user_action()


class SearchPlayerMenu:
    """ 1. Search for a player by asking the user for a key
        2. If more than one match: displays all players with a match
           and asks the user to pick a player
        3. Chosen Player gets displayed and the User gets
           to pick witch detail he wants to change.
        """

    def __init__(self):
        self.spacer = "\n                     "
        self.title = "Search Player"
        self.options = {
            "Search by First Name": self.search_first_name,
            "Search by Last Name": self.search_last_name,
            "Search by Birthdate": self.search_birth_date,
            "Search by Rating": self.search_rating,
            "Search by Sex": self.search_sex,
            "Get player directly by ID": self.get_by_id
        }
        self.menu = chess_club_app.controllers.menu_creator.MenuScreen(self.title, self.options, self.__class__.__name__)
        self.show_options()

    def show_options(self):
        """Displays the available Options"""

        tools.cls()
        tools.print_logo()
        self.menu.print_menu()
        self.menu.user_action()

    def search_first_name(self):
        self.search_for("first_name")

    def search_last_name(self):
        self.search_for("last_name")

    def search_birth_date(self):
        self.search_for("birth_date")

    def search_rating(self):
        self.search_for("rating")

    def search_sex(self):
        self.search_for("sex")

    def get_by_id(self):
        self.search_for("doc_id")

    def search_for(self, dict_key):

        tools.cls()
        tools.print_logo()
        self.menu.print_menu(title_only=True)
        wanted_value = input(
            f"{self.spacer}The wanted {dict_key.replace('_', ' ').title()}: ")

        if dict_key == "doc_id":
            player_found = DatabaseOperator().player_by_id(int(wanted_value))
            if player_found:
                EditOrDelete(player_found)
            else:
                print(f"{self.spacer}No Player with that ID found!")
                sleep(3)
                SearchPlayerMenu()

        else:
            matches = DatabaseOperator().search_for(dict_key, wanted_value.capitalize())

            if len(matches) == 0:
                print(f"{self.spacer}No Player with that {dict_key.replace('_', ' ').title()} found!")
                sleep(3)
                SearchPlayerMenu()

            elif len(matches) > 1:
                for player in matches:
                    print(tools.all_player_details(player))

                id_num = ""
                while not id_num.isnumeric():
                    id_num = input(
                        f"{self.spacer}Several matches found! Pick a player by ID!  ")
                EditOrDelete(matches[int(id_num) - 1])

            else:
                EditOrDelete(matches[0])


class EditOrDelete:
    """Takes a player object and ask´s the
       user if he wants to edit or delete it"""

    def __init__(self, player_obj):
        self.spacer = "\n                     "
        self.title = "Edit or Delete"
        self.options = {
            "Edit Player": self.edit,
            "Delete Player": self.delete,
        }
        self.menu = chess_club_app.controllers.menu_creator.MenuScreen(self.title, self.options, self.__class__.__name__)
        self.player_obj = player_obj

        tools.cls()
        tools.print_logo()
        self.menu.print_menu(title_only=True)
        print(tools.all_player_details(self.player_obj))
        self.menu.print_menu(options_only=True)
        self.menu.user_action()

    def edit(self):
        """Calls the player editor"""
        EditPlayer(self.player_obj)

    def delete(self):
        """Calls Delete Player"""
        DeletePlayer(self.player_obj)


class EditPlayer:
    """The Player Editor -> ask´s the user which
       Detail of the player he want to change"""

    def __init__(self, player_object):
        self.spacer = "\n                     "
        self.title = "Player Editor"
        self.options = {
            "Change First Name": self.update_first_name,
            "Change Last Name": self.update_lastname,
            "Change Birthdate": self.update_birth_date,
            "Change Sex": self.update_sex,
            "Change Rating": self.update_rating,
            "Delete the Player": self.open_delete_player
        }
        self.menu = chess_club_app.controllers.menu_creator.MenuScreen(self.title, self.options, self.__class__.__name__)
        self.player_object = player_object

        tools.cls()
        tools.print_logo()
        self.menu.print_menu(title_only=True)
        print(tools.all_player_details(self.player_object))
        self.menu.print_menu(options_only=True)
        self.menu.user_action()

    def update_first_name(self):
        new_first_name = ""
        while len(new_first_name) < 2:
            new_first_name = input(f"{self.spacer}New First Name:  ").capitalize()
        db = DatabaseOperator()
        db.update_player(
            player_id=self.player_object.doc_id,
            key="first_name",
            new_value=new_first_name)
        print(f"{self.spacer}{self.player_object['first_name']}´s "
              f"First Name successfully updated to {new_first_name}!")
        sleep(2)
        SearchPlayerMenu()

    def update_lastname(self):
        new_last_name = ""
        while len(new_last_name) < 2:
            new_last_name = input(f"{self.spacer}New Last Name:  ").capitalize()
        db = DatabaseOperator()
        db.update_player(
            player_id=self.player_object.doc_id,
            key="last_name",
            new_value=new_last_name)
        print(f"{self.spacer}{self.player_object['first_name']}´s "
              f"Last Name successfully updated to {new_last_name}!")
        sleep(2)
        SearchPlayerMenu()

    def update_birth_date(self):
        new_birth_date = ""
        while not tools.valid_date(new_birth_date):
            new_birth_date = input(f"{self.spacer}New Birth Date:  ").capitalize()
        db = DatabaseOperator()
        db.update_player(
            player_id=self.player_object.doc_id,
            key="birth_date",
            new_value=new_birth_date)
        print(f"{self.spacer}{self.player_object['first_name']}´s "
              f"Birth Date successfully updated to {new_birth_date}!")
        sleep(2)
        SearchPlayerMenu()

    def update_sex(self):
        new_sex = ""
        while not tools.valid_sex(new_sex):
            new_sex = input(f"{self.spacer}New Sex:  ").upper()
        db = DatabaseOperator()
        db.update_player(
            player_id=self.player_object.doc_id,
            key="sex",
            new_value=new_sex)
        print(f"{self.spacer}{self.player_object['first_name']}´s "
              f"Sex successfully updated to {new_sex}!")
        sleep(2)
        SearchPlayerMenu()

    def update_rating(self):
        new_rating = "-1"
        while not tools.valid_rating(new_rating):
            new_rating = input(f"{self.spacer}New Rating:  ")
        db = DatabaseOperator()
        db.update_player(
            player_id=self.player_object.doc_id,
            key="rating",
            new_value=new_rating)
        print(f"{self.spacer}{self.player_object['first_name']}´s "
              f"Rating successfully updated to {new_rating}!")
        sleep(2)
        SearchPlayerMenu()

    def open_delete_player(self):
        DeletePlayer(self.player_object).delete()


class DeletePlayer:
    """Player gets displayed and the User has to confirm
       that he wants to delete the player from the database."""

    def __init__(self, player_object):
        self.spacer = "\n                     "
        self.title = "Delete Player"
        self.options = {
            f"Please confirm: Delete the player {player_object['first_name']} "
            f"{player_object['last_name']} from the database!": self.delete
        }
        self.menu = chess_club_app.controllers.menu_creator.MenuScreen(self.title, self.options, self.__class__.__name__)
        self.player_object = player_object

        tools.cls()
        tools.print_logo()
        self.menu.print_menu(title_only=True)
        print(tools.all_player_details(self.player_object))
        self.menu.print_menu(options_only=True)
        self.menu.user_action()

    def delete(self):
        """Deletes the Player, prints confirmation and
           turns back to the search player menu."""
        DatabaseOperator().delete_player(self.player_object.doc_id)
        print(f"{self.spacer}The player: {self.player_object['first_name']} "
              f"{self.player_object['last_name']} successfully deleted!")
        sleep(2)
        SearchPlayerMenu()
