import json
from models.player import Player
from datetime import datetime
import os


class PlayerController:

    def __init__(self, data_file='data/players.json'):
        self.data_file = data_file
        self.players = self.load_players()

    def add_player(self, last_name, first_name, birth_date, national_id,
                   ranking, gender):
        if not self.validate_date(birth_date):
            print("Format de date invalide. Merci de l'ecrire sous la forme "
                  "DD/MM/YYYY.")
            return
        birth_date = datetime.strptime(birth_date, '%d/%m/%Y').date()
        player = Player(
            last_name,
            first_name,
            birth_date,
            national_id,
            ranking,
            gender
        )
        self.players.append(player)
        self.save_players()

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    def get_all_players(self):
        return sorted(self.players, key=lambda p: (p.last_name, p.first_name))

    def update_player_points(self, player):
        for p in self.players:
            if p.national_id == player.national_id:
                p.points = player.points
        self.save_players()

    def load_players(self):
        if not os.path.exists(self.data_file):
            return []
        if os.path.getsize(self.data_file) == 0:
            return []
        with open(self.data_file, 'r') as f:
            players_data = json.load(f)
        return [Player.from_dict(player) for player in players_data]

    def save_players(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(
                [player.add_to_dict() for player in self.players],
                f,
                indent=4)
