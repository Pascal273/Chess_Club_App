from chess_club_app.controllers import menu_creator
from chess_club_app.controllers import tools
from chess_club_app.controllers import tournament_operator
from chess_club_app.controllers.database_operator import DatabaseOperator as Db

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
                f"{self.spacer}(If it´s today you can type 'today'): ")
            if date == "today":
                self.start_date = tools.date_today()
            else:
                self.start_date = date
# TODO second date question should come at the end of the tournament!
        while not tools.valid_date(self.end_date):
            date = input(
                f"{self.spacer}What´s the start date of the Tournament? (DD.MM.YYYY)\n"
                f"{self.spacer}(If´s today you can type 'today'): ")
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

        self.players = SelectPlayers(self.number_of_rounds)


class SelectPlayers:
    """lets the user select a number of players, matching the number of rounds
       and returns them in a list"""

    def __init__(self, number_of_rounds: int = DEFAULT_ROUNDS):
        """Select Players Constructor"""
        self.spacer = "\n                     "

        self.player_ids = []
        self.number_of_participants = number_of_rounds * 2

        self.show_players = ShowPlayers()
        self.show_players.order()   # user pick´s the order the players will be displayed

        self.selection()

    def selection(self):

        while len(self.player_ids) < self.number_of_participants:

            picked = "0"
            while not tools.valid_id(picked) or picked in self.player_ids:
                self.show_players.show_all(not_show=self.player_ids)
                print(f"{self.spacer}Players in Tournament {len(self.player_ids)} / {self.number_of_participants}")
                picked = input(f"{self.spacer}Add to tournament (Enter ID): ")
                print("\033[A \033[A \033[A \033[A", end="")  # moves cursor 4 lines up (update effect)
            self.player_ids.append(int(picked))

        participants = [Db().player_by_id(player_id) for player_id in self.player_ids]
        return participants


class ShowPlayers:

    def __init__(self):
        self.title = "Show all Players"
        self.options = {
            "Show all players sort by ID": self.sort_by_id,
            "Show all players sort by first name": self.sort_by_first_name,
            "Show all players sort by last name": self.sort_by_last_name,
            "Show all players sort by birth date": self.sort_by_birth_date,
            "Show all players sort by sex": self.sort_by_sex,
            "Show all players sort by rating": self.sort_by_rating,
        }
        self.menu = menu_creator.MenuScreen(self.title, self.options, self.__class__.__name__)

        self.all_players = Db().load_all_players()

    def order(self):

        tools.cls()
        tools.print_logo()
        self.menu.print_menu()
        self.menu.user_action()

    def sort_by_id(self):
        pass

    def sort_by_first_name(self):
        """sort´s all players by first name"""
        self.all_players = sorted(self.all_players, key=lambda x: x.get('first name'))

    def sort_by_last_name(self):
        """sort´s all players by last name"""
        self.all_players = sorted(self.all_players, key=lambda x: x.get('last name'))

    def sort_by_birth_date(self):
        """sort´s all players by birth date"""
        self.all_players = sorted(self.all_players, key=lambda x: x.get('birth date'))

    def sort_by_sex(self):
        """sort´s all players by sex"""
        self.all_players = sorted(self.all_players, key=lambda x: x.get('sex'))

    def sort_by_rating(self):
        """sort´s all players by rating from highest to lowest"""
        self.all_players = sorted(self.all_players, key=lambda x: x.get('rating'), reverse=True)

    def show_all(self, not_show: list):

        tools.cls()
        tools.print_logo()
        self.menu.print_menu(title_only=True)

        if len(self.all_players) == 0:
            print("\n                     No Players in Database!")

        for player in self.all_players:
            if player.doc_id not in not_show:
                print(tools.all_player_details(player))


class LoadTournament:

    def __init__(self):
        pass


class EditTournament:

    def __init__(self):
        pass


class DeleteTournament:

    def __init__(self):
        pass


