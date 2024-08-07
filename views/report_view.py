from rich.console import Console
from rich.table import Table
from controllers.report_controller import ReportController

console = Console()


class ReportView:
    """
    Classe de la vue pour gérer les rapports.
    """

    def __init__(self):
        self.report_controller = ReportController()

    def display_tournaments(self):
        """
        Affiche la liste des tournois disponibles.
        """
        tournaments = self.report_controller.tournament_controller.tournaments
        table = Table(title="Liste des tournois disponibles")
        table.add_column("Index", style="cyan", no_wrap=True)
        table.add_column("Nom", style="magenta")
        table.add_column("Lieu", style="magenta")
        table.add_column("Date de début", style="green")
        table.add_column("Date de fin", style="green")

        for index, tournament in enumerate(tournaments):
            table.add_row(
                str(index),
                tournament.name,
                tournament.location,
                tournament.start_date,
                tournament.end_date
            )

        console.print(table)

    def generate_player_report(self):
        """
        Génère et affiche un rapport des joueurs.
        """
        self.report_controller.generate_player_report()
        console.print("[green]Rapport de joueur généré avec succès ![/green]")

    def generate_tournament_list_report(self):
        """
        Génère et affiche un rapport de la liste des tournois.
        """
        self.report_controller.generate_tournament_list_report()
        console.print("[green]Rapport de la liste des tournois généré avec succès ![/green]")

    def generate_tournament_details_report(self, tournament_index):
        """
        Génère et affiche un rapport des détails d'un tournoi donné.
        """
        self.report_controller.generate_tournament_details_report(tournament_index)
        console.print("[green]Rapport du détail pour le tournoi généré avec succès ![/green]")

    def generate_tournament_players_report(self, tournament_index):
        """
        Génère et affiche un rapport des joueurs d'un tournoi par ordre alphabétique.
        """
        self.report_controller.generate_tournament_players_report(tournament_index)
        console.print("[green]Rapport sur les joueurs présents dans le tournoi généré avec succès ![/green]")

    def generate_tournament_rounds_report(self, tournament_index):
        """
        Génère et affiche un rapport des tours et des matchs d'un tournoi.
        """
        self.report_controller.generate_tournament_rounds_report(tournament_index)
        console.print("[green]Rapports sur les tours et les matchs du tournoi généré avec succès ![/green]")
