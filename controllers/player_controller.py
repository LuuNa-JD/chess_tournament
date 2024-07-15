import json
from models.player import Player
from datetime import datetime
import os
from rich.console import Console

console = Console()


class PlayerController:
    """
    Contrôleur pour gérer les opérations liées aux joueurs.
    """

    def __init__(self, data_file='data/players.json'):
        """
        Initialise le contrôleur des joueurs.
        """
        self.data_file = data_file
        self.players = self.load_players()

    def add_player(self, last_name, first_name, birth_date, national_id,
                   ranking, gender):
        """
        Ajoute un nouveau joueur à la liste des joueurs et le sauvegarde.
        """
        try:
            birth_date = datetime.strptime(birth_date, '%d/%m/%Y').date()
            ranking = int(ranking)
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
            console.print("[green]Joueur ajouté avec succès.[/green]")
        except ValueError as e:
            console.print(f"[red]Erreur de saisie : {e}. Merci de vérifier vos entrées.[/red]")
        except Exception as e:
            console.print(f"[red]Erreur : {e}.[/red]")

    def get_all_players(self):
        """
        Retourne la liste de tous les joueurs triés par nom de famille et prénom.
        """
        return sorted(self.players, key=lambda p: (p.last_name, p.first_name))

    def load_players(self):
        """
        Charge les joueurs depuis le fichier JSON.
        """
        if not os.path.exists(self.data_file):
            return []
        if os.path.getsize(self.data_file) == 0:
            return []
        with open(self.data_file, 'r') as f:
            players_data = json.load(f)
        return [Player.from_dict(player) for player in players_data]

    def save_players(self):
        """
        Sauvegarde la liste des joueurs dans le fichier JSON.
        """
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(
                [player.add_to_dict() for player in self.players],
                f,
                indent=4)
