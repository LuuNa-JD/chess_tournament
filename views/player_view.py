from rich.console import Console
from rich.table import Table
from controllers.player_controller import PlayerController

console = Console()


class PlayerView:
    """
    Classe de la vue pour gérer les interactions liées aux joueurs.
    """

    def __init__(self):
        self.player_controller = PlayerController()

    def add_player(self):
        """
        Ajoute un joueur.
        """
        player_info = self.get_player_info()
        self.player_controller.add_player(
            player_info["last_name"],
            player_info["first_name"],
            player_info["birth_date"],
            player_info["national_id"],
            player_info["ranking"],
            player_info["gender"]
        )
        console.print("[green]Le joueur a été ajouté avec succes ![/green]")

    def view_players(self):
        """
        Affiche les joueurs par ordre alphabétique.
        """
        self.player_controller.load_players()
        players_sorted = sorted(self.player_controller.players, key=lambda x: x.last_name)
        self.display_players(players_sorted)

    @staticmethod
    def get_player_info():
        """
        Demande les informations du joueur et les retourne sous forme de dictionnaire.
        """
        last_name = input("Entrez le nom de famille: ")
        first_name = input("Entrez le prénom: ")
        birth_date = input("Entrez la date de naissance (DD/MM/YYYY): ")
        national_id = input("Entrez l'identifiant national: ")
        ranking = int(input("Entrez le classement: "))
        gender = input("Entrez le genre (M/F): ")
        return {
            "last_name": last_name,
            "first_name": first_name,
            "birth_date": birth_date,
            "national_id": national_id,
            "ranking": ranking,
            "gender": gender

        }

    def get_player_index(self, players):
        """
        Demande l'index du joueur à l'utilisateur.
        """
        self.display_players(players)
        return int(input("Entrer l'index du joueur: "))

    def display_players(self, players):
        """
        Affiche les joueurs dans un tableau formaté avec Rich.
        """
        table = Table(title="Liste des joueurs")
        table.add_column("Index", justify="right", style="cyan", no_wrap=True)
        table.add_column("Nom", style="magenta")
        table.add_column("Prénom", style="magenta")
        table.add_column("Date de naissance", style="green")
        table.add_column("Identifiant National", style="green")
        table.add_column("Classement", style="yellow")
        table.add_column("Sexe", style="blue")

        for index, player in enumerate(players):
            table.add_row(
                str(index),
                player.last_name,
                player.first_name,
                player.birth_date.strftime('%d/%m/%Y'),
                player.national_id,
                str(player.ranking),
                player.gender,
            )

        console.print(table)
