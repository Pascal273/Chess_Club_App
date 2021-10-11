from chess_club_app.controllers.database_operator import DatabaseOperator as Db
from chess_club_app.models.round import Round
from chess_club_app.models.match import Match


class TournamentOperator:
    """The Tournament Operator"""

    def __init__(self):
        self.tdb = Db().database.tournaments_table
