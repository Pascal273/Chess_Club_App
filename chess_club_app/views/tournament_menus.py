import player_menus
from chess_club_app.controllers import menu_creator
from chess_club_app.controllers import tools
from chess_club_app.controllers import tournament_operator
from chess_club_app.controllers import database_operator
from chess_club_app.controllers.database_operator import DatabaseOperator

DEFAULT_ROUNDS = 4


class TournamentMenu:
    """Displays the tournament main menu"""

    def __init__(self):
        """TournamentMenu constructor"""

        self.title = "Tournament Menu"
        self.options = {
             "Create New Tournament": NewTournament,
             "Load Tournament": LoadTournament,
             "Edit Tournament": EditTournament,
             "Delete Tournament": DeleteTournament
        }
        tools.cls()
        tools.print_logo()
        menu = menu_creator.MenuScreen(
            self.title,
            self.options,
            self.__class__.__name__
        )
        menu.print_menu()
        menu.user_action()


class NewTournament:
    """Creates and saves a new tournament"""

    def __init__(self):
        self.spacer = "\n                     "
        self.title = "New Tournament"

        self.menu = menu_creator.MenuScreen(
            self.title,
            self.__class__.__name__
        )
        self.start_date = ""
        self.end_date = ""

        self.name = ""
        self.location = ""
        self.date = ""
        self.number_of_rounds = 0
        self.rounds = ""
        self.players = []
        self.time_control = ""
        self.description = ""

        self.enter_user_information()

    def enter_user_information(self):
        """lets the user enter all tournament data"""

        tools.cls()
        tools.print_logo()
        self.menu.print_menu()

        while len(self.name) < 3:
            self.name = input(f"{self.spacer}What´s the name of the Tournament?: ")

        while len(self.location) < 5:
            self.location = input(f"{self.spacer}What´s the location of the Tournament?: ")

        while not tools.valid_date(self.start_date):
            date = input(
                f"{self.spacer}What´s the start date of the Tournament? (DD.MM.YYYY)\n"
                f"{self.spacer}(For today you can type 'today'): ")
            if date == "today":
                self.start_date = tools.date_today()
            else:
                self.start_date = date
# TODO second date question should come at the end of the tournament!
        while not tools.valid_date(self.end_date):
            date = input(
                f"{self.spacer}What´s the start date of the Tournament? (DD.MM.YYYY)\n"
                f"{self.spacer}(For today you can type 'today'): ")
            if date == "today":
                self.end_date = tools.date_today()
            else:
                self.end_date = date

        if self.start_date == self.end_date:
            self.date = self.start_date
        else:
            self.date = tools.date_range(self.start_date, self.end_date)

        while self.number_of_rounds < 1:
            self.number_of_rounds = int(
                input(f"Number of rounds to play (default is {DEFAULT_ROUNDS}): ") or DEFAULT_ROUNDS)

        while len(self.players) < self.number_of_rounds * 2:
            self.players = SelectPlayers(self.number_of_rounds)


class SelectPlayers:
    """lets the user select a number of players, matching the number of rounds
       and returns them in a list"""

    def __init__(self, number_of_rounds: int):
        """Select Players Constructor"""

        self.title = "Select Participants"
        self.options = {
            "Show all Players": player_menus.ShowAllPlayers
        }


class LoadTournament:

    def __init__(self):
        pass


class EditTournament:

    def __init__(self):
        pass


class DeleteTournament:

    def __init__(self):
        pass


