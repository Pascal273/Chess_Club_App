from tinydb import Query

from chess_club_app.models.player import Player
from chess_club_app.models.tournament import Tournament
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
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            sex=sex,
            rating=rating
        ).create()

        self.database.players_table.insert(serialized_player)

    def load_all_players(self):
        """Loads all players and returns them in a list"""

        all_players_serialized = self.database.players_table.all()

        return all_players_serialized

    def search_player(self, filter_by, key_word):
        """Loads all players matching a given key
           and returns a dict of all matches"""

        results = self.database.players_table.search(self.player[filter_by] == key_word)
        return results

    def player_by_id(self, player_id: int):
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

    # ------------------------------------------Tournament Operations---------------------------------------------------

    def save_tournament(self,
                        name,
                        location,
                        date,
                        number_of_rounds,
                        rounds,
                        players,
                        time_control,
                        description
                        ):
        """Tournament gets serialized and saved in database"""

        serialized_tournament = Tournament(
            name=name,
            location=location,
            date=date,
            number_of_rounds=number_of_rounds,
            rounds=rounds,
            players=players,
            time_control=time_control,
            description=description
        ).create()

        self.database.tournaments_table.insert(serialized_tournament)

    def load_all_tournaments(self):
        """Loads all players and returns them in a list"""

        all_tournaments_serialized = self.database.tournaments_table.all()

        return all_tournaments_serialized

    def search_tournament(self, filter_by: str, key_word):
        """Loads all tournaments matching a given key
           and returns a dict of all matches"""

        results = self.database.tournaments_table.search(self.player[filter_by] == key_word)
        return results
