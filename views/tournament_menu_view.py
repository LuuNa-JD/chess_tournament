from rich.console import Console
from rich.table import Table
from views.tournament_view import TournamentView

console = Console()


class TournamentMenuView:
    """
    Classe de la vue pour gérer le menu spécifique des tournois.
    """

    def __init__(self):
        self.tournament_view = TournamentView()
        self.selected_tournament = None

    def run(self):
        """
        Démarre le menu de gestion du tournoi.
        """
        self.select_tournament()
        while self.selected_tournament:
            choice = self.display_tournament_menu()
            self.handle_choice(choice)

    def select_tournament(self):
        """
        Sélectionne un tournoi sur lequel travailler.
        """
        self.tournament_view.view_tournaments()
        tournament_index = self.tournament_view.get_tournament_index()
        self.selected_tournament = self.tournament_view.tournament_controller.tournaments[tournament_index]
        console.print(f"[green]Tournoi selectionné: {self.selected_tournament.name}[/green]")

    @staticmethod
    def display_tournament_menu():
        """
        Affiche le menu spécifique des tournois et retourne le choix de l'utilisateur.
        """
        table = Table(title="Menu du tournoi")
        table.add_column("Option", style="cyan", no_wrap=True)
        table.add_column("Description", style="magenta")

        table.add_row("1", "Ajouter un joueur au tournoi")
        table.add_row("2", "Demarrer un tour du tournoi")
        table.add_row("3", "Mettre a jour un tour du tournoi")
        table.add_row("4", "Terminer un tour du tournoi")
        table.add_row("5", "Voir les tours/matchs du tournoi ")
        table.add_row("6", "Changer de tournoi")
        table.add_row("7", "Retour au menu principal")

        console.print(table)
        return input("Sélectionnez une option: ")

    def handle_choice(self, choice):
        """
        Gère les choix de l'utilisateur dans le menu spécifique des tournois.
        """
        if choice == "1":
            self.tournament_view.add_player_to_tournament(self.selected_tournament)
        elif choice == "2":
            self.tournament_view.start_tournament_round(self.selected_tournament)
        elif choice == "3":
            self.tournament_view.update_match_result(self.selected_tournament)
        elif choice == "4":
            self.tournament_view.end_tournament_round(self.selected_tournament)
        elif choice == "5":
            self.view_tournament_matches()
        elif choice == "6":
            self.select_tournament()
        elif choice == "7":
            self.selected_tournament = None
        else:
            print("Choix invalide, veuillez selectionner un choix valide.")

    def view_tournament_matches(self):
        """
        Affiche les matchs d'un tournoi.
        """
        self.tournament_view.view_rounds(self.selected_tournament)
        for round_instance in self.selected_tournament.round_list:
            self.tournament_view.view_matches(round_instance)
