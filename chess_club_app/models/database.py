import os

from tinydb import TinyDB, Query

DB_FILE = "database.json"
DIRECTORY = "./database"


class Database:
    """The database Model"""
    def __init__(self):
        """Database constructor"""

        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)

        self.database = TinyDB(f"{DIRECTORY}/{DB_FILE}")
        self.players_table = self.database.table("players")
        self.tournaments = {}

    def save_player(self, serialized_player):
        """insert a serialized player in the Database"""

        self.players_table.insert(serialized_player)
