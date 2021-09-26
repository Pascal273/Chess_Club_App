import chess_club_app.controllers.menu_creator
import chess_club_app.controllers.tools as tools


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
        menu = chess_club_app.controllers.menu_creator.MenuScreen(self.title, self.options, self.__class__.__name__)
        menu.print_menu()
        menu.user_action()


class NewTournament:
    """Creates and saves a new tournament"""

    def __init__(self):
        self.title = "New Tournament"
        self.options = {
            "Create New Tournament": NewTournament,
            "Load Tournament": LoadTournament,
            "Edit Tournament": EditTournament,
            "Delete Tournament": DeleteTournament
        }
        tools.cls()
        tools.print_logo()
        menu = chess_club_app.controllers.menu_creator.MenuScreen(self.title, self.options, self.__class__.__name__)
        menu.print_menu()
        menu.user_action()


class LoadTournament:

    def __init__(self):
        pass


class EditTournament:

    def __init__(self):
        pass


class DeleteTournament:

    def __init__(self):
        pass
