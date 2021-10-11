
class Round:
    """The round model"""

    def __init__(self, round_nr: int):
        """Constructor for Round

        Args:
            round_nr: int - the number of the current round in the Tournament
        """

        self.nr = round_nr
        self.matches = []

    def create(self):

        ser_round = {f"Round {self.nr}": self.matches}

        return ser_round
