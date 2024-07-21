import json
from datetime import datetime
from models.player import Player
from models.round import Round
from models.match import Match
import random


class Tournament:
    """
    Classe représentant un tournoi d'échecs.
    """

    def __init__(self, name, location, start_date, end_date, rounds=4, description=""):
        """
        Initialise un nouveau tournoi.

        Arguments:
            name (str): Le nom du tournoi.
            location (str): Le lieu du tournoi.
            start_date (str or datetime): La date de début du tournoi (format 'DD/MM/YYYY' ou datetime).
            end_date (str or datetime): La date de fin du tournoi (format 'DD/MM/YYYY' ou datetime).
            rounds (int, optional): Le nombre de tours du tournoi. Par défaut à 4.
            description (str): La description du tournoi.
        """
        self.name = name
        self.location = location
        self.start_date = start_date.strftime('%d/%m/%Y') if isinstance(start_date, datetime) else start_date
        self.end_date = end_date.strftime('%d/%m/%Y') if isinstance(end_date, datetime) else end_date
        self.rounds = rounds
        self.current_round = 0
        self.players = []  # Initialise une liste vide pour les joueurs
        self.round_list = []  # Initialise une liste vide pour les tours
        self.description = description
        self.player_points = {}  # Initialise un dictionnaire vide pour les points des joueurs

    def add_player(self, player):
        """
        Ajoute un joueur au tournoi.
        """
        self.players.append(player)  # Ajoute le joueur à la liste des joueurs
        self.player_points[player.national_id] = 0

    def get_player_points(self, player):
        """
        Retourne les points d'un joueur dans le tournoi.
        """
        return self.player_points.get(player.national_id, 0)

    def generate_pairs(self, round_instance):
        """
        Génère des paires de joueurs pour un tour donné.
        """
        # Pour le premier tour, les joueurs sont mélangés aléatoirement
        if self.current_round == 0:
            random.shuffle(self.players)
        else:
            # Pour les tours suivants, les joueurs sont triés par leurs points (du plus élevé au plus bas)
            self.players.sort(key=lambda p: self.player_points[p.national_id], reverse=True)

        # Ensemble pour suivre les paires de joueurs déjà créées
        paired_players = set()

        # Itérer sur la liste des joueurs deux par deux pour créer des paires
        for i in range(0, len(self.players), 2):
            if i + 1 < len(self.players):
                player1 = self.players[i]
                player2 = self.players[i + 1]
                # S'assurer que la paire de joueurs n'a pas déjà été créée
                if (player1, player2) not in paired_players and (player2, player1) not in paired_players:
                    # Créer un match avec les deux joueurs
                    match = Match(player1, player2)
                    # Ajouter le match au tour actuel
                    round_instance.add_match(match)
                    # Ajouter la paire de joueurs à l'ensemble des paires
                    paired_players.add((player1, player2))

    def start_new_round(self):
        """
        Démarre un nouveau tour et génère les paires de joueurs pour ce tour.
        """
        round_name = f"Round {self.current_round + 1}"
        new_round = Round(round_name)
        self.generate_pairs(new_round)
        self.round_list.append(new_round)  # Ajoute le nouveau tour à la liste des tours
        self.current_round += 1

    def end_current_round(self):
        """
        Termine le tour en cours en enregistrant l'heure actuelle comme heure de fin.
        """
        if self.current_round > 0:
            current_round = self.round_list[-1]  # Récupère le tour actuel
            current_round.end_round()  # Termine le tour en cours

    def update_match_result(self, round_index, match_index, winner, score1, score2):
        """
        Met à jour le résultat d'un match dans un tour donné.
        """
        match = self.round_list[round_index].matches[match_index]  # Récupère le match spécifique dans le tour.
        match.set_result(winner)  # Définit le résultat du match.
        match.score1 = score1  # Met à jour le score du premier joueur.
        match.score2 = score2
        self.player_points[match.player1.national_id] += score1   # Met à jour les points du premier joueur.
        self.player_points[match.player2.national_id] += score2

    @staticmethod
    def save_tournaments(tournaments, file_path):
        """
        Sauvegarde la liste des tournois dans un fichier JSON.
        """
        with open(file_path, 'w') as f:
            json.dump([tournament.add_to_dict() for tournament in tournaments], f, indent=4)

    @staticmethod
    def load_tournaments(file_path):
        """
        Charge la liste des tournois depuis un fichier JSON.
        La méthode retourne une liste d'instances de tournois.
        """
        with open(file_path, 'r') as f:
            tournaments_data = json.load(f)  # Charge les données du fichier JSON.
            return [Tournament.from_dict(data) for data in tournaments_data]

    def add_to_dict(self):
        """
        Convertit les détails du tournoi en dictionnaire.
        La méthode retourne un dictionnaire contenant les détails du tournoi.
        """
        return {
            'name': self.name,  # Ajoute le nom du tournoi au dictionnaire.
            'location': self.location,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'rounds': self.rounds,
            'current_round': self.current_round,
            'players': [player.add_to_dict() for player in self.players],
            'round_list': [round_instance.add_to_dict() for round_instance in self.round_list],
            'description': self.description,
            'player_points': self.player_points
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crée une instance de Tournament à partir d'un dictionnaire.
        La méthode retourne une instance de Tournament initialisée avec les données fournies.
        """
        start_date = data['start_date']
        end_date = data['end_date']
        tournament = cls(
            data['name'],   # Extrait le nom du tournoi du dictionnaire.
            data['location'],
            start_date,  # Passée en tant que chaîne de caractères
            end_date,
            data['rounds'],
            data['description']
        )
        tournament.current_round = data['current_round']
        tournament.players = [Player.from_dict(player) for player in data['players']]
        tournament.round_list = [
            Round.from_dict(round_instance, tournament.players)
            for round_instance in data['round_list']
        ]  # Crée une liste de tours à partir des données du dictionnaire.
        tournament.player_points = data.get('player_points', {})  # Définit les points des joueurs à partir du dict
        return tournament
