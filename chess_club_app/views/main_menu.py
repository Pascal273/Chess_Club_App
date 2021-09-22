import chess_club_app.views.views_tools as tools
from chess_club_app.views.player_menus import PlayerMenu
from chess_club_app.views.tournament_menus import TournamentMenu


class MainMenu:

    def __init__(self):
        """MainMenu Constructor"""

        self.options = {
            "Player Menu": PlayerMenu,
            "Tournament Menu": TournamentMenu
        }
        self.show_main_menu()

    def show_main_menu(self):
        """Shows the Main Menu"""

        tools.cls()
        tools.print_logo()
        tools.print_menu(title="Home", options=self.options)
