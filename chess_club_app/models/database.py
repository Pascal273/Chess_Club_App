import os

from tinydb import TinyDB

DB_FILE = "database.json"
DIRECTORY = "../database"


class Database:
    """The database Model"""
    def __init__(self):
        """Database constructor"""

        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)
        self.players = {}
        self.tournaments = {}
        self.database = TinyDB(f"{DIRECTORY}/{DB_FILE}")

    def save_player(self, serialized_player):
        """insert a serialized player in the Database"""

        self.database.insert(serialized_player)
