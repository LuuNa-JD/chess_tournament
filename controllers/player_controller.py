from models.player import Player
from datetime import datetime
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
        self.players = Player.load_players(self.data_file)  # Charge les joueurs depuis le fichier JSON

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
            )  # Crée une nouvelle instance de Player avec les données fournies.
            self.players.append(player)  # Ajoute le nouveau joueur à la liste des joueurs.
            self.save_players()  # Sauvegarde la liste mise à jour des joueurs dans le fichier JSON.
            console.print("[green]Joueur ajouté avec succès.[/green]")
        except ValueError as e:
            console.print(f"[red]Erreur de saisie : {e}. Merci de vérifier vos entrées.[/red]")
        except Exception as e:
            console.print(f"[red]Erreur : {e}.[/red]")

    def load_players(self):
        """
        Charge la liste des joueurs à partir du fichier JSON.
        """
        self.players = Player.load_players(self.data_file)  # Charge les joueurs depuis le fichier JSON

    def save_players(self):
        """
        Sauvegarde la liste des joueurs dans le fichier JSON.
        """
        Player.save_players(self.players, self.data_file)  # Sauvegarde la liste des joueurs dans le fichier JSON
