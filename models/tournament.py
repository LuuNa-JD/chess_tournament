import json
import os
from models.round import Round
from models.player import Player
from datetime import datetime


class Tournament:

    def __init__(self, name, location, start_date, end_date, rounds=4,
                 description=""):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.rounds = rounds
        self.current_round = 0
        self.players = []
        self.round_list = []
        self.description = description

    def add_to_dict(self):
        return {
            'name': self.name,
            'location': self.location,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'rounds': self.rounds,
            'current_round': self.current_round,
            'players': [player.add_to_dict() for player in self.players],
            'round_list': [
                round.add_to_dict() for round in self.round_list
            ],
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data):
        tournament = cls(
            data['name'],
            data['location'],
            datetime.fromisoformat(data['start_date']).date(),
            datetime.fromisoformat(data['end_date']).date(),
            data['rounds'],
            data.get('description', "")
        )
        tournament.current_round = data['current_round']
        tournament.players = [
            Player.from_dict(player) for player in data['players']
            ]
        tournament.round_list = [
            Round.from_dict(round) for round in data['round_list']
            ]
        return tournament

    def add_player(self, player):
        self.players.append(player)

    def add_round(self, round_instance):
        self.round_list.append(round_instance)

    @staticmethod
    def load_tournaments(file_path='data/tournaments.json'):
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as f:
            tournaments_data = json.load(f)
        return [
            Tournament.from_dict(tournament) for tournament in tournaments_data
            ]

    @staticmethod
    def save_tournaments(tournaments, file_path='data/tournaments.json'):
        with open(file_path, 'w') as f:
            json.dump(
                [tournament.add_to_dict() for tournament in tournaments],
                f,
                indent=4
            )
