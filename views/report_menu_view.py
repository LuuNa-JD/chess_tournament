from rich.console import Console
from rich.table import Table
from views.report_view import ReportView

console = Console()


class ReportMenuView:
    """
    Classe de la vue pour gérer le menu des rapports.
    """

    def __init__(self):
        self.report_view = ReportView()

    def run(self):
        while True:
            self.display_menu()
            choice = input("Selectionnez une option: ")
            if choice == "1":
                self.report_view.generate_player_report()
                console.print("[green]Rapport des joueurs généré avec succès ![/green]")
            elif choice == "2":
                self.report_view.generate_tournament_list_report()
                console.print("[green]Rapport sur la liste des tournois généré avec succès ![/green]")
            elif choice == "3":
                self.report_view.display_tournaments()
                tournament_index = int(input("Entrez l'index du tournoi: "))
                self.report_view.generate_tournament_details_report(tournament_index)
                console.print("[green]Rapport sur les details du tournoi généré avec succès ![/green]")
            elif choice == "4":
                self.report_view.display_tournaments()
                tournament_index = int(input("Entrez l'index du tournoi: "))
                self.report_view.generate_tournament_players_report(tournament_index)
                console.print("[green]Rapport sur les joueurs du tournoi généré avec succès !.[/green]")
            elif choice == "5":
                self.report_view.display_tournaments()
                tournament_index = int(input("Entrez l'index du tournoi: "))
                self.report_view.generate_tournament_rounds_report(tournament_index)
                console.print("[green]Rapport sur les tours du tournoi généré avec succès ![/green]")
            elif choice == "6":
                break
            else:
                console.print("[red]Choix invalide, veuillez selectionner un choix valide[/red]")

    def display_menu(self):
        table = Table(title="Menu des rapports")
        table.add_column("Option", style="cyan", no_wrap=True)
        table.add_column("Rapports", style="magenta")

        table.add_row("1", "Génération d'un rapport des joueurs")
        table.add_row("2", "Génération d'un rapport sur la liste des tournois")
        table.add_row("3", "Génération d'un rapport sur les détails d'un tournoi")
        table.add_row("4", "Génération d'un rapport sur les joueurs d'un tournoi")
        table.add_row("5", "Génération d'un rapport sur les tours d'un tournoi")
        table.add_row("6", "Back to Main Menu")

        console.print(table)
