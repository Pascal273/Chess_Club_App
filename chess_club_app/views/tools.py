import os

import chess_club_app.views.main_menu as _main_menu


def cls():
    """Clears the terminal"""
    os.system("cls" if os.name == "nt" else "clear")


def back(current_site):
    """Return to previous page"""
    if current_site in ["PlayerMenu", "TournamentMenu"]:
        _main_menu.MainMenu()
