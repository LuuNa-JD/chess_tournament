import json
import os
from datetime import datetime


class Player:

    def __init__(self, last_name, first_name, birth_date, national_id):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.national_id = national_id
        self.points = 0

    def add_to_dict(self):
        return {
            'last_name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date.isoformat(),
            'national_id': self.national_id,
            'points': self.points
        }

    @classmethod
    def from_dict(cls, data):
        birth_date = datetime.fromisoformat(data['birth_date']).date()
        player = cls(
            data['last_name'],
            data['first_name'],
            birth_date,
            data['national_id']
        )
        player.points = data.get('points', 0)
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
