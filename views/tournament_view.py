from datetime import datetime
from rich.console import Console
from rich.table import Table
from controllers.tournament_controller import TournamentController
from views.player_view import PlayerView

console = Console()


class TournamentView:
    """
    Classe de la vue pour gérer les interactions liées aux tournois.
    """

    def __init__(self):
        self.tournament_controller = TournamentController()

    def create_tournament(self):
        """
        Crée un tournoi.
        """
        while True:
            tournament_info = self.get_tournament_info()
            if tournament_info:
                try:
                    start_date = datetime.strptime(tournament_info["start_date"], "%d/%m/%Y")
                    end_date = datetime.strptime(tournament_info["end_date"], "%d/%m/%Y")
                    self.tournament_controller.create_tournament(
                        tournament_info["name"],
                        tournament_info["location"],
                        start_date,
                        end_date,
                        tournament_info["rounds"],
                        tournament_info["description"]
                    )
                    console.print("[green]Tournoi créé avec succès.[/green]")
                    break
                except ValueError as e:
                    console.print(f"[red]Erreur de saisie : {e}. Merci de vérifier vos entrées.[/red]")
            else:
                console.print("[red]Erreur dans la saisie des informations du tournoi. Veuillez réessayer.[/red]")

    def add_player_to_tournament(self, tournament=None):
        """
        Ajoute un joueur à un tournoi.
        """
        if tournament is None:
            self.view_tournaments()
            tournament_index = self.get_tournament_index()
            tournament = self.tournament_controller.tournaments[tournament_index]

        while True:
            player_view = PlayerView()
            all_players = player_view.player_controller.players
            sorted_players = sorted(all_players, key=lambda x: (x.last_name, x.first_name))
            player_index = player_view.get_player_index(sorted_players)
            player = sorted_players[player_index]

            if tournament:
                self.tournament_controller.add_player_to_tournament(tournament, player)
                console.print("[green]Joueur ajouté au tournoi avec succès.[/green]")
            else:
                console.print("[red]Tournoi introuvable.[/red]")

            add_another = input("Ajouter un autre joueur ? (o/n): ")
            if add_another.lower() != 'o':
                break

    def start_tournament_round(self, tournament=None):
        """
        Démarre un tour de tournoi.
        """
        if tournament is None:
            self.view_tournaments()
            tournament_index = self.get_tournament_index()
            tournament = self.tournament_controller.tournaments[tournament_index]

        if tournament:
            self.tournament_controller.start_round(tournament)
            console.print("[green]Tour démarré avec succès.[/green]")
            self.view_matches(tournament.round_list[-1])
        else:
            console.print("[red]Tournoi introuvable.[/red]")

    def end_tournament_round(self, tournament=None):
        """
        Termine un tour de tournoi.
        """
        if tournament is None:
            self.view_tournaments()
            tournament_index = self.get_tournament_index()
            tournament = self.tournament_controller.tournaments[tournament_index]

        if tournament:
            self.view_rounds(tournament)
            round_index = self.get_round_index()
            if 0 <= round_index < len(tournament.round_list):
                round_instance = tournament.round_list[round_index]
                if round_instance.end_time is None:
                    self.tournament_controller.end_round(tournament, round_index)
                    console.print(f"[green]{round_instance.name} s'est terminé avec succès.[/green]")
                else:
                    console.print("[yellow]Ce tour est déjà terminé.[/yellow]")
            else:
                console.print("[red]Index de tour invalide.[/red]")
        else:
            console.print("[red]Tournoi introuvable.[/red]")

    def update_match_result(self, tournament=None):
        """
        Met à jour le résultat d'un match dans un tournoi.
        """
        if tournament is None:
            self.view_tournaments()
            tournament_index = self.get_tournament_index()
            tournament = self.tournament_controller.tournaments[tournament_index]

        if tournament:
            self.view_rounds(tournament)
            round_index = self.get_round_index()
            self.view_matches(tournament.round_list[round_index])
            match_index = self.get_match_index()

            match = tournament.round_list[round_index].matches[match_index]
            console.print(f"1. {match.player1.first_name} {match.player1.last_name}")
            console.print(f"2. {match.player2.first_name} {match.player2.last_name}")
            console.print("3. Egalité")
            result_choice = int(input("Selectionnez le vainqueur (1, 2) ou 3 pour une égalité: "))

            if result_choice == 1:
                winner = match.player1
                score1, score2 = 1.0, 0.0
            elif result_choice == 2:
                winner = match.player2
                score1, score2 = 0.0, 1.0
            else:
                winner = None
                score1, score2 = 0.5, 0.5

            self.tournament_controller.update_match_result(tournament, round_index,
                                                           match_index, winner, score1, score2)
            console.print("[green]Le resultat du match est mis à jour avec succès.[/green]")
        else:
            console.print("[red]Tournoi introuvable.[/red]")

    def view_tournaments(self):
        """
        Affiche les tournois.
        """
        self.tournament_controller.load_tournaments()
        self.display_tournaments(self.tournament_controller.tournaments)

    @staticmethod
    def get_tournament_info():
        """
        Demande les informations du tournoi et les retourne sous forme de dictionnaire.
        """
        while True:
            try:
                name = input("Entrez le nom du tournoi: ")
                location = input("Entrez le lieu du tournoi: ")
                start_date = input("Entrez la date de début (DD/MM/YYYY): ")
                end_date = input("Entrez la date de fin (DD/MM/YYYY): ")
                rounds = int(input("Entrez le nombre de tours souhaités (par défaut: 4): "))
                description = input("Entrez la description: ")
                return {
                    "name": name,
                    "location": location,
                    "start_date": start_date,
                    "end_date": end_date,
                    "rounds": rounds,
                    "description": description
                }
            except ValueError as e:
                console.print(f"[red]Erreur de saisie : {e}. Merci de vérifier vos entrées.[/red]")
            except Exception as e:
                console.print(f"[red]Erreur : {e}.[/red]")

    @staticmethod
    def get_tournament_index():
        """
        Demande l'index du tournoi à l'utilisateur.
        """
        return int(input("Entrez l'index du tournoi: "))

    @staticmethod
    def get_round_index():
        """
        Demande l'index du round à l'utilisateur.
        """
        return int(input("Entrez l'index du tour: "))

    @staticmethod
    def get_match_index():
        """
        Demande l'index du match à l'utilisateur.
        """
        return int(input("Entrez l'index du match: "))

    @staticmethod
    def display_tournaments(tournaments):
        """
        Affiche les tournois.
        """
        table = Table(title="Liste des tournois")
        table.add_column("Index", style="cyan", no_wrap=True)
        table.add_column("Nom", style="magenta")
        table.add_column("Emplacement", style="magenta")
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

    @staticmethod
    def view_rounds(tournament):
        """
        Affiche les rounds d'un tournoi.
        """
        table = Table(title=f"Rounds dans le tournoi {tournament.name}")
        table.add_column("Index", style="cyan", no_wrap=True)
        table.add_column("Nom", style="magenta")
        table.add_column("Date de début", style="green")
        table.add_column("Date de fin", style="green")

        for index, round_instance in enumerate(tournament.round_list):
            table.add_row(
                str(index),
                round_instance.name,
                round_instance.start_time.strftime('%d/%m/%Y %H:%M'),
                round_instance.end_time.strftime('%d/%m/%Y %H:%M') if round_instance.end_time else "None"
            )

        console.print(table)

    @staticmethod
    def view_matches(round_instance):
        """
        Affiche les matchs d'un round.
        """
        table = Table(title=f"Matchs du {round_instance.name}")
        table.add_column("Index", style="cyan", no_wrap=True)
        table.add_column("Joueur 1", style="magenta")
        table.add_column("Joueur 2", style="magenta")
        table.add_column("Score", style="green")
        table.add_column("Couleur de jeu", style="yellow")

        for index, match in enumerate(round_instance.matches):
            table.add_row(
                str(index),
                f"{match.player1.first_name} {match.player1.last_name}",
                f"{match.player2.first_name} {match.player2.last_name}",
                f"{match.score1} - {match.score2}",
                f"{match.player1_color} - {match.player2_color}"
            )

        console.print(table)
