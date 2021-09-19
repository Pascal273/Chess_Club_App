
from chess_club_app.models.player import Player
from chess_club_app.models.database import Database


class DatabaseOperator:
    """Database operators"""

    def __init__(self):
        """DatabaseOperator constructor"""

        self.database = Database()

    def save_player(self, first_name, last_name, birth_date, sex, rating):
        """Player gets serialized and saved in database"""

        serialized_player = Player(
            first_name, last_name, birth_date, sex, rating).create()

        self.database.save_player(serialized_player)

