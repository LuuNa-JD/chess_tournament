import json
import os
from datetime import datetime


class Player:

    def __init__(self, last_name, first_name, birth_date, national_id,
                 ranking, gender):
        self.last_name = last_name
        self.first_name = first_name
        if isinstance(birth_date, str):
            self.birth_date = datetime.strptime(birth_date, '%d/%m/%Y').date()
        else:
            self.birth_date = birth_date
        self.national_id = national_id
        self.ranking = ranking
        self.gender = gender

    def add_to_dict(self):
        return {
            'last_name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date.strftime('%d/%m/%Y'),
            'national_id': self.national_id,
            'ranking': self.ranking,
            'gender': self.gender
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(
            data['last_name'],
            data['first_name'],
            data['birth_date'],
            data['national_id'],
            data['ranking'],
            data['gender']
        )
        return player

    @staticmethod
    def load_players(file_path='data/players.json'):
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as f:
            players_data = json.load(f)
        return [Player.from_dict(player) for player in players_data]

    @staticmethod
    def save_players(players, file_path='data/players.json'):
        with open(file_path, 'w') as f:
            json.dump(
                [player.add_to_dict() for player in players],
                f,
                indent=4
            )
