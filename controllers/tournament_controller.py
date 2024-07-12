import random
from models.tournament import Tournament
from models.match import Match
import os


class TournamentController:
    def __init__(self):
        self.data_file = 'data/tournaments.json'
        self.tournaments = self.load_tournaments()

    def create_tournament(self, name, location, start_date, end_date, rounds=4, description=""):
        tournament = Tournament(name, location, start_date, end_date, rounds, description)
        self.tournaments.append(tournament)
        self.save_tournaments()

    def add_player_to_tournament(self, tournament, player):
        if any(p.national_id == player.national_id for p in tournament.players):
            print("Le joueur " + player.first_name + " " + player.last_name + " est déjà dans le tournoi.")
        else:
            tournament.add_player(player)
            self.save_tournaments()

    def start_round(self, tournament):
        tournament.start_new_round()
        self.save_tournaments()

    def end_round(self, tournament, round_index):
        round_instance = tournament.round_list[round_index]
        round_instance.end_round()
        self.save_tournaments()

    def update_match_result(
        self, tournament, round_index, match_index, winner, score1, score2
    ):
        tournament.update_match_result(
            round_index, match_index, winner, score1, score2
        )
        self.save_tournaments()

    def save_tournaments(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        Tournament.save_tournaments(self.tournaments, self.data_file)

    def load_tournaments(self):
        try:
            return Tournament.load_tournaments(self.data_file)
        except FileNotFoundError:
            return []

    def get_all_tournaments(self):
        return self.tournaments

    def get_tournament_by_name(self, name):
        for tournament in self.tournaments:
            if tournament.name == name:
                return tournament
        return None
