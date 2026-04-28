TEAMS = [
    "Náutico",
    "Sport Recife",
    "Santa Cruz",
    "Palmeiras",
    "Flamengo",
    "São Paulo",
    "Corinthians",
    "Vasco da Gama",
]

ANIMES = [
    "Death Note",
    "Blue Lock",
    "Dragon Ball Z",
    "Naruto",
    "One Piece",
    "Attack on Titan",
    "Jujutsu Kaisen",
    "Demon Slayer",
]

ANIMALS = [
    "Gato",
    "Cachorro",
    "Lagarto",
    "Zebra",
    "Capivara",
    "Pinguim",
    "Elefante",
    "Macaco",
]


class User:
    def __init__(self, username):
        self.username = username
        self.liked_teams = []
        self.liked_animes = []
        self.liked_animals = []

    def add_seed(self, category, item):
        if category == "team":
            self.liked_teams.append(item)
        elif category == "anime":
            self.liked_animes.append(item)
        elif category == "animal":
            self.liked_animals.append(item)
