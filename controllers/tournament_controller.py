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
            print("Player " + player.first_name + " " + player.last_name + " is already in the tournament.")
        else:
            tournament.add_player(player)
            self.save_tournaments()

    def start_round(self, tournament):
        tournament.start_new_round()
        self.save_tournaments()

    def generate_pairs(self, tournament, round_instance):
        if tournament.current_round == 0:
            random.shuffle(tournament.players)
        else:
            tournament.players.sort(key=lambda p: p.points, reverse=True)

        paired_players = set()
        for i in range(0, len(tournament.players), 2):
            if i + 1 < len(tournament.players):
                player1 = tournament.players[i]
                player2 = tournament.players[i + 1]
                if (player1, player2) not in paired_players and (player2, player1) not in paired_players:
                    match = Match(player1, player2)
                    round_instance.add_match(match)
                    paired_players.add((player1, player2))

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
