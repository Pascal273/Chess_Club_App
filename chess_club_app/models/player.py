
class Player:
    """The player model."""

    def __init__(self, first_name: str, last_name: str, birth_date: str, sex: str, rating: int):
        """Player Constructor"""
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.rating = rating
        self.deleted = False

    def create(self):
        """Creates and returns a new player"""
        player = {
            "first name": self.first_name,
            "last name": self.last_name,
            "birth date": self.birth_date,
            "sex": self.sex,
            "rating": self.rating,
            "deleted": self.deleted
        }
        return player
