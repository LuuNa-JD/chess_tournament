from models.tournament import Tournament
import os


class TournamentController:
    """
    Contrôleur pour gérer les opérations liées aux tournois.
    """

    def __init__(self):
        """
        Initialise le contrôleur de tournoi.
        """
        self.data_file = 'data/tournaments.json'
        self.tournaments = self.load_tournaments()

    def create_tournament(self, name, location, start_date, end_date, rounds=4, description=""):
        """
        Crée un nouveau tournoi et l'ajoute à la liste des tournois.
        """
        tournament = Tournament(name, location, start_date, end_date, rounds, description)
        self.tournaments.append(tournament)  # Ajout du tournoi à la liste des tournois.
        self.save_tournaments()  # Sauvegarde des tournois dans le fichier JSON.

    def add_player_to_tournament(self, tournament, player):
        """
        Ajoute un joueur à un tournoi, si le joueur n'est pas déjà inscrit.
        """
        if any(p.national_id == player.national_id for p in tournament.players):
            print("Le joueur " + player.first_name + " " + player.last_name + " est déjà dans le tournoi.")
        else:
            tournament.add_player(player)  # Ajoute le joueur au tournoi.
            self.save_tournaments()  # Sauvegarde des tournois dans le fichier JSON.

    def start_round(self, tournament):
        """
        Démarre un nouveau tour pour le tournoi donné.
        """
        tournament.start_new_round()  # Démarre un nouveau tour pour le tournoi.
        self.save_tournaments()

    def end_round(self, tournament, round_index):
        """
        Termine le tour spécifié d'un tournoi.
        """
        round_instance = tournament.round_list[round_index]   # Récupère le tour spécifié par son index.
        round_instance.end_round()  # Termine le tour.
        self.save_tournaments()

    def update_match_result(
        self, tournament, round_index, match_index, winner, score1, score2
    ):
        """
        Met à jour le résultat d'un match dans un tournoi.

        Arguments:
            tournament (Tournament): Le tournoi contenant le match.
            round_index (int): L'index du tour contenant le match.
            match_index (int): L'index du match à mettre à jour.
            winner (Player): Le joueur gagnant du match.
            score1 (float): Le score du joueur 1.
            score2 (float): Le score du joueur 2.
        """
        tournament.update_match_result(
            round_index, match_index, winner, score1, score2
        )  # Met à jour le résultat du match.
        self.save_tournaments()

    def save_tournaments(self):
        """
        Sauvegarde la liste des tournois dans un fichier JSON.
        """
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        # Utilise la méthode de classe de Tournament pour sauvegarder les tournois.
        Tournament.save_tournaments(self.tournaments, self.data_file)

    def load_tournaments(self):
        """
        Charge la liste des tournois à partir d'un fichier JSON.
        """
        try:
            # Utilise la méthode de classe de Tournament pour charger les tournois.
            return Tournament.load_tournaments(self.data_file)
        except FileNotFoundError:
            return []  # Retourne une liste vide si le fichier n'existe pas.
