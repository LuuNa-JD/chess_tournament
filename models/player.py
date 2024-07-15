import json
import os
from datetime import datetime


class Player:
    """
    Classe représentant un joueur.
    """

    def __init__(self, last_name, first_name, birth_date, national_id,
                 ranking, gender):
        """
        Initialise un nouveau joueur.

        Arguments:
            last_name (str): Le nom de famille du joueur.
            first_name (str): Le prénom du joueur.
            birth_date (str or datetime): La date de naissance du joueur (format 'DD/MM/YYYY' ou datetime).
            national_id (str): L'identifiant national du joueur.
            ranking (int): Le classement du joueur.
            gender (str): Le sexe du joueur.
        """
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
        """
        Convertit les détails du joueur en dictionnaire.
        La méthode retourne un dictionnaire contenant les détails du joueur.
        """
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
        """
        Crée une instance de Player à partir d'un dictionnaire.

        La méthode retourne une instance de Player initialisée avec les données fournies.
        """
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
        """
        Charge les joueurs à partir d'un fichier JSON.

        La méthode retourne une liste d'instances de joueurs.
        """
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as f:
            players_data = json.load(f)
        return [Player.from_dict(player) for player in players_data]

    @staticmethod
    def save_players(players, file_path='data/players.json'):
        """
        Sauvegarde les joueurs dans un fichier JSON.
        """
        with open(file_path, 'w') as f:
            json.dump(
                [player.add_to_dict() for player in players],
                f,
                indent=4
            )
