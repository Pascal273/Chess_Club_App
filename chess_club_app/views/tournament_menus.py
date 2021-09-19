import chess_club_app.views.views_tools as tools


class TournamentMenu:

    def __init__(self):
        self.options = """
                     ---Tournament Menu---

                     [1] New Tournament
                     [2] Load Tournament
                     [3] Edit Tournament
                     [4] Delete Tournament
            
                     [0] Return to Home
        """
        self.tournament_menu()
        self.ask_user()

    def tournament_menu(self):
        tools.cls()
        tools.print_logo()
        print(self.options)

    def ask_user(self):
        answer = input("                What would you like to do? ")

        if answer == "1":
            pass

        elif answer == "2":
            pass

        elif answer == "3":
            pass

        elif answer == "4":
            pass

        elif answer == "0":
            tools.back(self.__class__.__name__)

        else:
            TournamentMenu()


class NewTournament:

    def __init__(self):
        pass


class LoadTournament:

    def __init__(self):
        pass


class DeleteTournament:

    def __init__(self):
        pass
