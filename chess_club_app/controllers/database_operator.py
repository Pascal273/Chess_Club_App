from tinydb import Query

from chess_club_app.models.player import Player
from chess_club_app.models.database import Database


class DatabaseOperator:
    """Database operators"""

    def __init__(self):
        """DatabaseOperator constructor"""

        self.database = Database()
        self.player = Query()

    def save_player(self, first_name, last_name, birth_date, sex, rating):
        """Player gets serialized and saved in database"""

        serialized_player = Player(
            first_name, last_name, birth_date, sex, rating).create()

        self.database.players_table.insert(serialized_player)

    def load_all_players(self):
        """Loads all players and returns them in a list """

        all_players_serialized = self.database.players_table.all()
        all_players_list = [player for player in all_players_serialized]

        return all_players_list

    def search_for(self, filter_by, key_word):
        """Loads all players, filters them by a given key
           and returns a dict of all matches"""

        results = self.database.players_table.search(self.player[filter_by] == key_word)
        return results

    def player_by_id(self, player_id):
        """Takes a player ID and returns
           the matching Player as a player object"""

        player = self.database.players_table.get(doc_id=player_id)
        return player

    def update_player(self, player_id, key: str, new_value):
        """Update the value of a given key in the database """

        self.database.players_table.update_player(
            {key: new_value},
            doc_ids=[player_id]
        )

    def update_all_matching_players(self, key: str, old_value: str, new_value: str):
        """Updates all matching entries in the player table"""

        self.database.players_table.update_player(
            {key: new_value},
            self.player[key] == old_value
        )

    def delete_player(self, player_id):
        self.database.players_table.remove(doc_ids=[player_id])
