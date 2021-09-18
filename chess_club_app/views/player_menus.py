import chess_club_app.views.tools as tools


class PlayerMenu:
    """Displays options for player operations"""

    def __init__(self):
        """ PlayerMenu Constructor"""

        self.options = """
        
        -----Player Menu-----
        
        [1] Add a new player
        [2] Edit player
        [3] Show all players
        [4] Delete player

        [0] Return to Home
        """
        self.player_main_menu()
        self.ask_user()

    def player_main_menu(self):
        """Shows the player main menu"""

        tools.cls()
        print(self.options)

    def ask_user(self):
        answer = input("    What would you like to do? ")

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
            PlayerMenu()


class AddNewPlayer:

    def __init__(self):
        pass


class EditPlayer:

    def __init__(self):
        pass


class ShowAllPlayers:

    def __init__(self):
        pass


class DeletePlayer:

    def __init__(self):
        pass

