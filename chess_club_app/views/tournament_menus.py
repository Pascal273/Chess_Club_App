from time import sleep

from chess_club_app.controllers import menu_creator
from chess_club_app.controllers import util
from chess_club_app.controllers.tournament_operator import TournamentOperator
from chess_club_app.controllers.database_operator import DatabaseOperator as Db

DEFAULT_ROUNDS = 4


class TournamentMenu:
    """Displays the tournament main menu"""

    def __init__(self):
        """TournamentMenu constructor"""

        self.title = "Tournament Menu"
        self.options = {
             "Create New Tournament": NewTournament,
             "Show Tournaments": ShowTournaments,
             "Play Tournament": PlayTournamentMenu,
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
            self.name = input(f"{self.spacer}What´s the name of the Tournament?: ").title()

        # ------------------------------------------Enter Location------------------------------------------------------

        while len(self.location) < 5:
            self.location = input(f"\n{self.spacer}What´s the location of the Tournament?: ").title()

        # ------------------------------------------Enter Date----------------------------------------------------------

        while not util.valid_date(self.date):
            date = input(
                f"\n{self.spacer}What´s the start date of the Tournament? (DD.MM.YYYY)\n"
                f"{self.spacer}(If it´s today you can type 'today'): ")
            if date == "today":
                self.date = util.date_today()
            else:
                self.date = date

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
            self.description = input(f"\n{self.spacer}Enter a Description: ").capitalize()

        # ------------------------------------------Enter Select Players------------------------------------------------

        self.players = SelectPlayers(self.number_of_rounds).selection()

    def confirm(self):
        """
                1. Displays the all tournament details
                2. Asks user if it's all correct
                3. If user answers 'yes' the tournament gets saved.
                   If if user answers 'no' the player doesn't get saved.
                """

        ser_players = [Db().player_by_id(id_num) for id_num in self.players]
        player_name_list = [p["first name"] + " " + p["last name"] for p in ser_players]
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
                     Nr. of Rounds:      {self.number_of_rounds}\n
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

        # participants = [Db().player_by_id(player_id) for player_id in self.player_ids]
        return self.player_ids


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


class ShowTournaments:

    def __init__(self):
        self.spacer = "\n                     "
        self.title = "Show Tournaments"
        self.options = {
            "Show all Finished Tournaments": self.show_all_finished,
            "Show all Unfinished Tournaments": self.show_all_unfinished,
            "Search for a Tournament": self.search_for
        }

        self.menu = menu_creator.MenuScreen(
            title=self.title,
            options=self.options,
            current_site=self.__class__.__name__
        )

        self.all_tournaments_serialized = Db().load_all_tournaments()

        util.cls()
        util.print_logo()
        self.menu.print_menu()
        self.menu.user_action()

    def show_all_unfinished(self):

        unfinished_tournaments = [
            t for t in self.all_tournaments_serialized if len(t["rounds"]) < t["number of rounds"]]

        menu = menu_creator.MenuScreen(
            title="Unfinished Tournaments",
            options={
                "Play a Tournament": PlayTournamentMenu,
                "Delete a Tournament": DeleteTournament
            },
            current_site=self.__class__.__name__
        )

        util.cls()
        util.print_logo()
        menu.print_menu(title_only=True)

        if len(unfinished_tournaments) == 0:
            print(f"{self.spacer}No Unfinished Tournaments in Database!")
            sleep(3)
            ShowTournaments()

        else:
            for tournament in unfinished_tournaments:
                print(util.all_tournament_details(tournament))

            menu.print_menu(options_only=True)
            menu.user_action()

    def show_all_finished(self):

        finished_tournaments = [
            t for t in self.all_tournaments_serialized if len(t["rounds"]) == t["number of rounds"]]

        menu = menu_creator.MenuScreen(
            title="Finished Tournaments",
            options={
                "Edit a Tournament": EditTournament,
                "Delete a Tournament": DeleteTournament
            },
            current_site=self.__class__.__name__
        )

        util.cls()
        util.print_logo()
        menu.print_menu(title_only=True)

        if len(finished_tournaments) == 0:
            print(f"{self.spacer}No Finished Tournaments in Database!")
            sleep(3)
            ShowTournaments()

        else:
            for tournament in finished_tournaments:
                print(util.all_tournament_details(tournament))

        menu.print_menu(options_only=True)
        menu.user_action()

    def search_for(self):
        pass


class PlayTournamentMenu:

    def __init__(self):
        self.spacer = "\n                     "
        self.title = "Play Tournament"
        self.options = {
            "show Tournaments sort by ID": self.sort_by_id,
            "Show Tournaments sort by date (latest -> oldest)": self.sort_by_date
        }

        self.tournaments_serialized = Db().database.tournaments_table
        self.unfinished_tournaments = [
            t for t in self.tournaments_serialized if len(t["rounds"]) < t["number of rounds"]]

        self.menu = menu_creator.MenuScreen(
            title=self.title,
            options=self.options,
            current_site=self.__class__.__name__
        )

        util.cls()
        util.print_logo()
        self.menu.print_menu()
        self.menu.user_action()

        util.cls()
        util.print_logo()
        self.menu.print_menu(title_only=True)
        self.show_all()
        self.user_choice()

    def sort_by_id(self):
        pass

    def sort_by_date(self):
        """sort´s all unfinished tournaments by date"""
        self.unfinished_tournaments = sorted(
            self.unfinished_tournaments, key=lambda x: x.get('date'[0]), reverse=True)

    def show_all(self):
        """Displays all unfinished tournaments in the chosen order"""

        if len(self.unfinished_tournaments) == 0:
            print("\n                     No new or unfinished in Database!")

        else:
            for tournament in self.unfinished_tournaments:
                print(util.all_tournament_details(tournament))

    def user_choice(self):
        """User has to pick a tournament by ID"""
        available_ids = [str(t.doc_id) for t in self.unfinished_tournaments]

        tournament_id = ""
        while not util.valid_int(tournament_id) or tournament_id not in available_ids:
            tournament_id = input(f"{self.spacer}Which tournament do you want to start? (Enter ID): ")

        RunTournament(int(tournament_id))


class RunTournament:

    def __init__(self, tournament_id: int):
        self.tournament = TournamentOperator(tournament_id)

        self.spacer = "\n                     "
        self.play_rounds()
        self.show_leaderboard()

    def play_rounds(self):
        while self.tournament.get_completed_rounds_nr() < self.tournament.rounds_to_play:
            title = f"Playing Round {self.tournament.get_current_round_number()}"
            menu = menu_creator.MenuScreen(title)
            util.cls()
            util.print_logo()
            menu.print_menu()

            self.current_round()
            self.tournament.update_scores()
            self.tournament.save_finished_round()

    def current_round(self):

        if self.tournament.get_current_round_number() == 1:
            pairs = self.tournament.first_pairing()
        else:
            pairs = self.tournament.next_pairing()

        for pair in pairs:
            p1 = pair[0][0]
            p2 = pair[1][0]

            print(f"{self.spacer}---Match {self.tournament.get_current_match_number()}---")
            print(f"{self.spacer}{p1['first name']} {p1['last name']} vs {p2['first name']} {p2['last name']}")

            result = ""
            while result not in ["0", "1", "2"]:
                result = input(f"{self.spacer}Winner? (P1 = 1, P2 = 2, Tie = 0): ")

            self.tournament.save_match(
                player_1=p1,
                player_2=p2,
                winner=int(result)
            )

    def show_leaderboard(self):
        """Displays the leaderboard"""

        spacer = "                     "
        title = "Results"
        options = {
            "Return to Tournament Menu": TournamentMenu,
            "Show Tournaments": ShowTournaments
        }
        menu = menu_creator.MenuScreen(
            title=title,
            options=options,
            current_site="MainMenu"
        )

        leaderboard = self.tournament.get_leaderboard()

        util.cls()
        util.print_logo()
        menu.print_menu(title_only=True)
        for ps in leaderboard:
            lb_row = f"{spacer}{ps[0]['first name']} {ps[0]['last name']} : {ps[1]}"
            print(lb_row)



class EditTournament:

    def __init__(self):
        pass


class DeleteTournament:
    """Tournament gets displayed and the User has to confirm
    that he wants to delete the player from the database."""

    def __init__(self, tournament_object):
        self.spacer = "\n                     "
        self.title = "Delete Tournament"
        self.options = {
            f"Please confirm: Delete the tournament {tournament_object['name']} "
            f"{tournament_object['date']} from the database!": self.delete
        }
        self.menu = menu_creator.MenuScreen(self.title, self.options, self.__class__.__name__)
        self.tournament_object = tournament_object

        util.cls()
        util.print_logo()
        self.menu.print_menu(title_only=True)
        print(util.all_tournament_details(self.tournament_object))
        self.menu.print_menu(options_only=True)
        self.menu.user_action()

    def delete(self):
        """Deletes the Player, prints confirmation and
           turns back to the search player menu."""
        Db().delete_tournament(self.tournament_object.doc_id)
        print(f"{self.spacer}The player: {self.tournament_object['name']} successfully deleted!")
        sleep(2)
        TournamentMenu()
