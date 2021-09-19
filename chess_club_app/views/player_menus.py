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
            PlayerMenu()


class AddNewPlayer:
    """New player creator"""

    def __init__(self):
        """New player constructor"""

        self.title = """
                    --Create new Player--
        """
        self.first_name = ""
        self.last_name = ""
        self.birth_date = ""
        self.sex = ""
        self.rating = ""

        self.enter_player_details()
        self.check_details()

    def enter_player_details(self):
        """ask user for the details of the new player"""

        tools.cls()
        tools.print_logo()
        print(self.title)

        while len(self.first_name) < 2:
            self.first_name = input("whats the players first name?:    ")

        while len(self.last_name) < 2:
            self.last_name = input("Whats the players last name?:    ")

        while not tools.valid_date(self.birth_date):
            self.birth_date = input("Whats the players birth date? (DD.MM.YYYY)?:    ")

        while not tools.valid_sex(self.sex):
            self.sex = input("Whats the players sex? (M/F):    ").lower()

        while not self.rating.isnumeric():
            self.rating = input("Whats the players current rating?:    ")

    def check_details(self):
        """1. Displays the all the players details
        2. Asks user if it's all correct
        3. If user answers 'yes' the player gets saved.
           If if user answers 'no' the player doesn't get saved.
        """

        tools.cls()
        tools.print_logo()
        print(self.title)

        print(f"""
        Name:             {self.first_name} {self.last_name}
        Date of Birth:    {self.birth_date}
        Sex:              {self.sex}
        Rating:           {self.rating}
        """)

        if input("Are details about the new player correct? (Y/N)    ").lower() == "y":
            self.save_player()
        else:
            PlayerMenu()

    def save_player(self):
        """Saves new Player in the database"""

        print(f"Player {self.first_name} {self.last_name} saved in Database")


class EditPlayer:

    def __init__(self):
        pass


class ShowAllPlayers:

    def __init__(self):
        pass


class DeletePlayer:

    def __init__(self):
        pass

