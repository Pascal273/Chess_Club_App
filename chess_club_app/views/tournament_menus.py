from time import sleep

from chess_club_app.controllers import menu_creator
from chess_club_app.controllers import util
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
        util.cls()
        util.print_logo()
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
            title=self.title,
            current_site=self.__class__.__name__
        )
        self.start_date = ""
        self.end_date = ""

        self.name = ""
        self.location = ""
        self.date = []
        self.number_of_rounds = ""
        self.rounds = []
        self.players = []
        self.time_control = ""
        self.description = ""

        self.saved_players = len(Db().load_all_players())

        if self.saved_players >= 8:
            self.enter_data()
            self.confirm()
        else:
            print(f"\n{self.spacer}Not enough player in Database! Please add more!\n"
                  f"{self.spacer}(Min. 8 are required for a tournament)")
            sleep(3)
            TournamentMenu()

    def enter_data(self):
        """lets the user enter all tournament data"""

        util.cls()
        util.print_logo()
        self.menu.print_menu()

        # ------------------------------------------Enter Name----------------------------------------------------------

        while len(self.name) < 3:
            self.name = input(f"{self.spacer}What´s the name of the Tournament?: ")

        # ------------------------------------------Enter Location------------------------------------------------------

        while len(self.location) < 5:
            self.location = input(f"\n{self.spacer}What´s the location of the Tournament?: ").title()

        # ------------------------------------------Enter Dates---------------------------------------------------------

        while not util.valid_date(self.start_date):
            date = input(
                f"\n{self.spacer}What´s the start date of the Tournament? (DD.MM.YYYY)\n"
                f"{self.spacer}(If it´s today you can type 'today'): ")
            if date == "today":
                self.start_date = util.date_today()
            else:
                self.start_date = date
# TODO second date question should come at the end of the tournament!
        while not util.valid_date(self.end_date):
            date = input(
                f"\n{self.spacer}What´s the end date of the Tournament? (DD.MM.YYYY)\n"
                f"{self.spacer}(If´s today you can type 'today'): ")
            if date == "today":
                self.end_date = util.date_today()
            else:
                self.end_date = date

        if self.start_date == self.end_date:
            self.date.append(self.start_date)
        else:
            self.date = util.date_range(self.start_date, self.end_date)

        # ------------------------------------------Enter Number of Rounds----------------------------------------------

        while not util.valid_int(self.number_of_rounds):
            self.number_of_rounds = input(
                f"\n{self.spacer}Number of rounds to play (default is {DEFAULT_ROUNDS}): ") or DEFAULT_ROUNDS
        self.number_of_rounds = int(self.number_of_rounds)

        # ------------------------------------------Enter Time Control--------------------------------------------------

        while self.time_control not in ["bullet", "blitz", "rapid"]:
            self.time_control = input(
                f"\n{self.spacer}Time control? (bullet / blitz / rapid): ").lower()

        # ------------------------------------------Enter Description---------------------------------------------------

        while len(self.description) < 1:
            self.description = input(f"\n{self.spacer}Enter a Description: ")

        # ------------------------------------------Enter Select Players------------------------------------------------

        self.players = SelectPlayers(self.number_of_rounds).selection()

    def confirm(self):
        """
                1. Displays the all tournament details
                2. Asks user if it's all correct
                3. If user answers 'yes' the tournament gets saved.
                   If if user answers 'no' the player doesn't get saved.
                """

        player_name_list = [p["first name"] + " " + p["last name"] for p in self.players]
        names = "\n"
        for name in player_name_list:
            names += f"                                         {name}\n\n"

        util.cls()
        util.print_logo()
        menu = menu_creator.MenuScreen("Confirm")
        menu.print_menu()

        print(f"""
                     Tournament Name:    {self.name}\n
                     Location:           {self.location}\n
                     Date(s):            {self.date}\n
                     Nr. of  Rounds:     {self.number_of_rounds}\n
                     Time Control:       {self.time_control}\n
                     Participants:       {names}\n
                     Description:        {self.description}\n
                """)

        if input(f"{self.spacer}Are details about the new tournament correct? (Y/N) "
                 ).lower() == "y":
            self.save_tournament()
            print(f"{self.spacer}{self.name} - Tournament added to the Database")
            sleep(3)
            TournamentMenu()
        else:
            TournamentMenu()

    def save_tournament(self):
        """Saves new Player in the database"""

        Db().save_tournament(
            name=self.name,
            location=self.location,
            date=self.date,
            number_of_rounds=self.number_of_rounds,
            rounds=self.rounds,
            players=self.players,
            time_control=self.time_control,
            description=self.description
        )


class SelectPlayers:
    """lets the user select a number of players, matching the number of rounds
       and returns them in a list"""

    def __init__(self, number_of_rounds: int):
        """Select Players Constructor"""
        self.spacer = "\n                     "

        self.player_ids = []
        self.number_of_participants = number_of_rounds * 2

        self.show_players = ShowPlayers()
        self.show_players.order()   # user pick´s the order the players will be displayed

    def selection(self):
        """Displays all available PLayers from Database and lets the user pick
        one after the other to add to the list of participants."""

        available_ids = [p.doc_id for p in Db().load_all_players()]

        while len(self.player_ids) < self.number_of_participants:

            picked = "0"
            while not util.valid_int(picked) or picked in self.player_ids:
                self.show_players.show_all(not_show=self.player_ids)
                print(f"{self.spacer}Players in Tournament {len(self.player_ids)} / {self.number_of_participants}")
                picked = input(f"{self.spacer}Add to tournament (Enter ID): ")
            picked = int(picked)

            if picked not in self.player_ids and picked in available_ids:
                self.player_ids.append(picked)

        participants = [Db().player_by_id(player_id) for player_id in self.player_ids]
        return participants


class ShowPlayers:
    """Displays all players incl. table of their information,
       sorted by a detail of the users choice.
       Players that are already added to the tournament will not be displayed."""

    def __init__(self):
        self.title = "Pick Participants"
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

        util.cls()
        util.print_logo()
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

        util.cls()
        util.print_logo()
        self.menu.print_menu(title_only=True)

        if len(self.all_players) == 0:
            print("\n                     No Players in Database!")
            sleep(2)
            TournamentMenu()

        for player in self.all_players:
            if player.doc_id not in not_show:
                print(util.all_player_details(player))


class LoadTournament:

    def __init__(self):
        pass


class EditTournament:

    def __init__(self):
        pass


class DeleteTournament:

    def __init__(self):
        pass
