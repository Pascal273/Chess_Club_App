import chess_club_app.views.tools as tools
from chess_club_app.views.player_menus import PlayerMenu
from chess_club_app.views.tournament_menus import TournamentMenu


class MainMenu:

    def __init__(self):
        """MainMenu Constructor"""

        self.menu_options = """
                    --------Home---------
                    
                    [1] Player Menu
                    [2] Tournament Menu
            
                    [0] Exit Chess App
        """

        self.show_main_menu()
        self.ask_user()

    def show_main_menu(self):
        """Shows the Main Menu"""
        tools.cls()
        tools.print_logo()
        print(self.menu_options)

    def ask_user(self):
        answer = input("                What would you like to do? ")

        if answer == "1":
            PlayerMenu()

        elif answer == "2":
            TournamentMenu()

        elif answer == "0":
            tools.cls()
            exit()

        else:
            MainMenu()
