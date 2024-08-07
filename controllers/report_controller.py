from jinja2 import Environment, FileSystemLoader
import os
import webbrowser
from rich.console import Console
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController

console = Console()


class ReportController:
    """
    Contrôleur pour générer des rapports basés sur les données des joueurs et des tournois.
    """

    def __init__(self):
        """
        Initialise le contrôleur de rapport.
        """
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        # Configuration de l'environnement Jinja2 pour le chargement des templates.
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.reports_dir = 'reports'

        # Crée le répertoire des rapports s'il n'existe pas
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

    def generate_player_report(self):
        """
        Génère un rapport des joueurs triés par nom et prénom.
        """
        players = sorted(self.player_controller.players, key=lambda x: (x.last_name, x.first_name))  # Tri des joueurs
        template = self.env.get_template('player_report_template.html')  # Chargement du template pour le rapport
        report_content = template.render(players=players)
        report_path = os.path.join(self.reports_dir, 'player_report.html')
        with open(report_path, 'w') as report_file:
            report_file.write(report_content)
        webbrowser.open_new_tab(report_path)  # Ouverture du rapport généré dans un nouvel onglet du navigateur.

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
            webbrowser.open_new_tab(report_path)
        else:
            console.print("[red]Index du tournoi invalide[/red]")

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
            webbrowser.open_new_tab(report_path)
        else:
            console.print("[red]Index du tournoi invalide[/red]")

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
            webbrowser.open_new_tab(report_path)
        else:
            console.print("[red]Index du tournoi invalide[/red]")
