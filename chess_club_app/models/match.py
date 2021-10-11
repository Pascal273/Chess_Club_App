
class Match:
    """The Match model

        Args:
            player_1: player object
            player_2: player object
            winner: int
    """

    def __init__(self, player_1: object, player_2: object, winner: int):
        """Constructor for the Match model"""

        self.player_1 = player_1
        self.player_2 = player_2

        if winner == 1:
            self.p1_score = 1
            self.p2_score = 0

        elif winner == 2:
            self.p1_score = 0
            self.p2_score = 1

        else:
            self.p1_score = 0.5
            self.p2_score = 0.5

    def create(self):

        result = (
            [self.player_1, self.p1_score],
            [self.player_2, self.p2_score]
        )

        return result
