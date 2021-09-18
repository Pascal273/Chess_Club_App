
class Player:
    """The player model."""

    def __init__(self, first_name, last_name, age, birth_date, sex, rating):
        """Player Constructor"""
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.birth_date = birth_date
        self.sex = sex
        self.rating = rating

    def create(self):
        player = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "birth_date": self.birth_date,
            "sex": self.sex,
            "rating": self.rating
        }
        return player
