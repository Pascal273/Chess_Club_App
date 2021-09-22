from tinydb import Query

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

    def load_all_players(self):
        """Loads all players and returns them in a list """

        all_players_serialized = self.database.players_table.all()
        all_players_list = [player for player in all_players_serialized]

        return all_players_list

    def search_for(self, filter_by, key_word):
        """Loads all players, filters them by a given key
           and returns a dict of all matches"""

        user = Query()
        results = self.database.players_table.search(user[filter_by] == key_word)
        return results

