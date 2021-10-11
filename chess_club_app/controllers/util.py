import os
import datetime
from chess_club_app.views import main_menu
from chess_club_app.views import player_menus
from chess_club_app.views import tournament_menus
from chess_club_app.controllers.database_operator import DatabaseOperator as Db


def print_logo():
    """Prints the ascii-logo"""
    logo = """
     .::.
     _::_                                            _()_
   _/____\\_                                        _/____\\_
   \\      /                                        \\      /
    \\____/                                          \\____/
    (____)                                          (____)
     |  |                                            |  |
     |__|                                            |__|
    /    \\          ___| |__   ___  ___ ___         /    \\
   (______)        / __| '_ \\ / _ \\/ __/ __|       (______)
  (________)      | (__| | | |  __/\\__ \\__ \\      (________)
  /________\\       \\___|_| |_|\\___||___/___/      /________\\
    """
    print(logo)


def cls():
    """Clears the terminal"""
    os.system("cls" if os.name == "nt" else "clear")


def date_today():
    """Returns current date in format: DD.MM.YYYY"""

    date = datetime.date.today().strftime("%d.%m.%Y")
    return date


def date_range(start_date, end_date):
    """Takes 2 dates and returns a list of all dates,
       from the start date to the end date"""

    s_date_obj = datetime.datetime.strptime(start_date, "%d.%m.%Y")
    e_date_obj = datetime.datetime.strptime(end_date, "%d.%m.%Y")

    delta = e_date_obj - s_date_obj

    days_list = []
    for date in range(delta.days + 1):
        day = s_date_obj + datetime.timedelta(days=date)
        days_list.append(datetime.datetime.strftime(day, "%d.%m.%Y"))
    return days_list


def valid_menu_choice(answer, opt_num):
    """Checks if the users choice is valid
       valid -> returns: True
       invalid -> returns: False"""

    try:
        if answer == "":
            return False
        elif int(answer) > opt_num:
            return False
        else:
            return True
    except ValueError:
        print("     Enter the number of an option!")
        return False


def turn_back_to(current_class_name: str):
    """Turns back to the last Menu by calling the last Class before the current one.
       If current class = MainMenu -> it closes the Program"""

    if current_class_name == "MainMenu":
        cls()
        exit()
    elif current_class_name in ["PlayerMenu", "TournamentMenu"]:
        main_menu.MainMenu()

    elif current_class_name in [
        "AddNewPlayer",
        "ShowAllPlayers",
        "SearchPlayer",
    ]:
        player_menus.PlayerMenu()

    elif current_class_name in [
        "EditPlayer",
        "DeletePlayer",
        "EditOrDelete"
    ]:
        player_menus.SearchPlayer()

    elif current_class_name in [
        "NewTournament",
        "SelectPlayers",
        "ShowPlayers",
        "ShowTournaments",
        "PlayTournament",
        "DeleteTournament"
    ]:
        tournament_menus.TournamentMenu()


def all_player_details(player):
    """Takes a player object and returns all
       (for the app user relevant) Details in a printable table"""

    player_details = (f"""
                     ID:          {player.doc_id}
                     First Name:  {player["first name"]}
                     Last Name :  {player["last name"]}
                     Birth Date:  {player["birth date"]}
                     Sex:         {player["sex"]}
                     Rating:      {player["rating"]}
        """)
    return player_details


def all_tournament_details(tournament):

    ser_players = [Db().player_by_id(id_num) for id_num in tournament["players"]]
    player_name_list = [p["first name"] + " " + p["last name"] for p in ser_players]
    names = "\n"
    for name in player_name_list:
        names += f"                                    {name}\n"

    if len(tournament["date"]) > 1:
        dates = f'{tournament["date"][0]} - {tournament["date"][-1]}'
    else:
        dates = tournament["date"][0]

    if len(tournament["rounds"]) == 0:
        rounds = "No rounds played"
    # TODO - display round results
    else:
        rounds = "Display round results"

    tournament_details = (f"""
                     ID:            {tournament.doc_id}
                     Name:          {tournament["name"]}
                     Location:      {tournament["location"]}
                     Date(s):       {dates}
                     Nr. of Rounds: {tournament["number of rounds"]}
                     Time Control:  {tournament["time control"]}
                     Participants:  {names}
                     Description:   {tournament["description"]}\n
                     Rounds:        {rounds}
        """)

    return tournament_details


def valid_date(date_text):
    """Checks if a date String is in a valid format and returns False or True"""

    try:
        datetime.datetime.strptime(date_text, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def valid_sex(sex_text):
    """Checks if a string is m or f and returns False or True"""

    if sex_text == "F" or sex_text == "M":
        return True
    else:
        return False


def valid_rating(number_string):
    """Checks if number is valid, not negative, int or float
       and returns False or True"""

    try:
        if float(number_string) >= 0:
            return True
        else:
            return False

    except ValueError:
        print("\n                     It has to be a 0 or positive number!")
        return False


def valid_int(number_string):
    """Checks if number is a valid id, int > 1
           and returns False or True"""

    try:
        if int(number_string) > 0:
            return True
        else:
            return False

    except ValueError:
        return False
