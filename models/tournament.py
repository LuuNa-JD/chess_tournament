import json
from datetime import datetime
from models.player import Player
from models.round import Round
from models.match import Match
import random


class Tournament:
    def __init__(self, name, location, start_date, end_date, rounds=4, description=""):
        self.name = name
        self.location = location
        self.start_date = start_date.strftime('%d/%m/%Y') if isinstance(start_date, datetime) else start_date
        self.end_date = end_date.strftime('%d/%m/%Y') if isinstance(end_date, datetime) else end_date
        self.rounds = rounds
        self.current_round = 0
        self.players = []
        self.round_list = []
        self.description = description
        self.player_points = {}

    def add_player(self, player):
        self.players.append(player)
        self.player_points[player.national_id] = 0

    def get_player_points(self, player):
        return self.player_points.get(player.national_id, 0)

    def generate_pairs(self, round_instance):
        if self.current_round == 0:
            random.shuffle(self.players)
        else:
            self.players.sort(key=lambda p: self.player_points[p.national_id], reverse=True)

        paired_players = set()
        for i in range(0, len(self.players), 2):
            if i + 1 < len(self.players):
                player1 = self.players[i]
                player2 = self.players[i + 1]
                if (player1, player2) not in paired_players and (player2, player1) not in paired_players:
                    match = Match(player1, player2)
                    round_instance.add_match(match)
                    paired_players.add((player1, player2))

    def start_new_round(self):
        round_name = f"Round {self.current_round + 1}"
        new_round = Round(round_name)
        self.generate_pairs(new_round)
        self.round_list.append(new_round)
        self.current_round += 1

    def end_current_round(self):
        if self.current_round > 0:
            current_round = self.round_list[-1]
            current_round.end_round()

    def update_match_result(self, round_index, match_index, winner, score1, score2):
        match = self.round_list[round_index].matches[match_index]
        match.set_result(winner)
        match.score1 = score1
        match.score2 = score2
        self.player_points[match.player1.national_id] += score1
        self.player_points[match.player2.national_id] += score2

    @staticmethod
    def save_tournaments(tournaments, file_path):
        with open(file_path, 'w') as f:
            json.dump([tournament.add_to_dict() for tournament in tournaments], f, indent=4)

    @staticmethod
    def load_tournaments(file_path):
        with open(file_path, 'r') as f:
            tournaments_data = json.load(f)
            return [Tournament.from_dict(data) for data in tournaments_data]

    def add_to_dict(self):
        return {
            'name': self.name,
            'location': self.location,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'rounds': self.rounds,
            'current_round': self.current_round,
            'players': [player.add_to_dict() for player in self.players],
            'round_list': [round_instance.add_to_dict() for round_instance in self.round_list],
            'description': self.description,
            'player_points': self.player_points
        }

    @classmethod
    def from_dict(cls, data):
        start_date = data['start_date']
        end_date = data['end_date']
        tournament = cls(
            data['name'],
            data['location'],
            start_date,
            end_date,
            data['rounds'],
            data['description']
        )
        tournament.current_round = data['current_round']
        tournament.players = [Player.from_dict(player) for player in data['players']]
        tournament.round_list = [
            Round.from_dict(round_instance, tournament.players)
            for round_instance in data['round_list']
        ]
        tournament.player_points = data.get('player_points', {})
        return tournament
