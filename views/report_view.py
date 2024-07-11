from rich.console import Console
from rich.table import Table
import os
import webbrowser
from jinja2 import Environment, FileSystemLoader
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController

console = Console()


class ReportView:
    """
    Classe de la vue pour gérer les rapports.
    """

    def __init__(self):
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.reports_dir = 'reports'

        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

    def display_tournaments(self):
        """
        Affiche les tournois disponibles.
        """
        tournaments = self.tournament_controller.tournaments
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
        Génère un rapport des joueurs.
        """
        players = sorted(self.player_controller.players, key=lambda x: (x.last_name, x.first_name))
        template = self.env.get_template('player_report_template.html')
        report_content = template.render(players=players)

        report_path = os.path.join(self.reports_dir, 'player_report.html')
        with open(report_path, 'w') as report_file:
            report_file.write(report_content)

        print("Rapport de joueur généré avec succès !")
        webbrowser.open_new_tab(report_path)

    def generate_tournament_list_report(self):
        """
        Génère un rapport de la liste des tournois.
        """
        tournaments = self.tournament_controller.tournaments
        template = self.env.get_template('tournament_list_template.html')
        report_content = template.render(tournaments=tournaments)

        report_path = os.path.join(self.reports_dir, 'tournament_list.html')
        with open(report_path, 'w') as report_file:
            report_file.write(report_content)

        print("Rapport de la liste des tournois généré avec succès !")
        webbrowser.open_new_tab(report_path)

    def generate_tournament_details_report(self, tournament_index):
        """
        Génère un rapport des détails d'un tournoi donné.
        """
        tournaments = self.tournament_controller.tournaments
        if 0 <= tournament_index < len(tournaments):
            tournament = tournaments[tournament_index]
            template = self.env.get_template('tournament_details_template.html')
            report_content = template.render(tournament=tournament)

            report_path = os.path.join(self.reports_dir, f'tournament_details_{tournament_index}.html')
            with open(report_path, 'w') as report_file:
                report_file.write(report_content)

            print(f"Rapport du détail pour le tournoi {tournament.name} généré avec succès !")
            webbrowser.open_new_tab(report_path)
        else:
            print("Index du tournoi invalide")

    def generate_tournament_players_report(self, tournament_index):
        """
        Génère un rapport des joueurs d'un tournoi par ordre alphabétique.
        """
        tournaments = self.tournament_controller.tournaments
        if 0 <= tournament_index < len(tournaments):
            tournament = tournaments[tournament_index]
            players = sorted(tournament.players, key=lambda x: (x.last_name, x.first_name))
            template = self.env.get_template('tournament_players_template.html')
            report_content = template.render(tournament=tournament, players=players)

            report_path = os.path.join(self.reports_dir, f'tournament_players_{tournament_index}.html')
            with open(report_path, 'w') as report_file:
                report_file.write(report_content)

            print(f"Rapport sur les joueurs présents dans le tournoi {tournament.name} généré avec succès !")
            webbrowser.open_new_tab(report_path)
        else:
            print("Index du tournoi invalide")

    def generate_tournament_rounds_report(self, tournament_index):
        """
        Génère un rapport des tours et des matchs d'un tournoi.
        """
        tournaments = self.tournament_controller.tournaments
        if 0 <= tournament_index < len(tournaments):
            tournament = tournaments[tournament_index]
            rounds = tournament.round_list
            template = self.env.get_template('tournament_rounds_template.html')
            report_content = template.render(tournament=tournament, rounds=rounds)

            report_path = os.path.join(self.reports_dir, f'tournament_rounds_{tournament_index}.html')
            with open(report_path, 'w') as report_file:
                report_file.write(report_content)

            print(f"Rapports sur les tours et les matchs du tournoi {tournament.name} généré avec succès !")
            webbrowser.open_new_tab(report_path)
        else:
            print("Index du tournoi invalide")
