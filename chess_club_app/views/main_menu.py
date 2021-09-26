import chess_club_app.controllers.menu_creator
import chess_club_app.controllers.tools as tools

from chess_club_app.views.player_menus import PlayerMenu
from chess_club_app.views.tournament_menus import TournamentMenu


class MainMenu:

    def __init__(self):
        """MainMenu Constructor"""

        self.title = "Home"
        self.options = {
            "Player Menu": PlayerMenu,
            "Tournament Menu": TournamentMenu
        }
        self.show_main_menu()

    def show_main_menu(self):
        """Shows the Main Menu"""

        tools.cls()
        tools.print_logo()
        menu = chess_club_app.controllers.menu_creator.MenuScreen(
            title=self.title,
            options=self.options,
            current_site=self.__class__.__name__)
        menu.print_menu()
        menu.user_action()
