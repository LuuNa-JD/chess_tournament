from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


class MainView:
    """
    Classe de la vue principale pour gérer le menu principal.
    """

    def run(self):
        """
        Démarre le menu principal.
        """
        while True:
            self.display_title()
            choice = self.display_main_menu()
            self.handle_choice(choice)

    @staticmethod
    def display_title():
        """
        Affiche le titre du logiciel.
        """
        title_text = Text("Chess Tournament Manager", style="bold blue")
        console.print(Panel(title_text, expand=False, border_style="bold green"))

    @staticmethod
    def display_main_menu():
        """
        Affiche le menu principal et retourne le choix de l'utilisateur.
        """
        console.print("\n[bold cyan]Menu Principal[/bold cyan]")
        console.print("1. Ajouter des joueurs")
        console.print("2. Créer un tournoi")
        console.print("3. Gérer un tournoi")
        console.print("4. Voir les joueurs")
        console.print("5. Rapports")
        console.print("6. Quitter\n")
        return input("Selectionner une option: ")

    def handle_choice(self, choice):
        """
        Gère les choix de l'utilisateur dans le menu principal.
        """
        if choice == "1":
            from views.player_view import PlayerView
            PlayerView().add_new_player()
        elif choice == "2":
            from views.tournament_view import TournamentView
            TournamentView().create_tournament()
        elif choice == "3":
            from views.tournament_menu_view import TournamentMenuView
            TournamentMenuView().run()
        elif choice == "4":
            from views.player_view import PlayerView
            PlayerView().view_players()
        elif choice == "5":
            from views.report_menu_view import ReportMenuView
            ReportMenuView().run()
        elif choice == "6":
            console.print("[bold green]A bientot ![/bold green]")
            exit()
        else:
            console.print("[bold red]Choix invalide, essayez un autre.[/bold red]")
