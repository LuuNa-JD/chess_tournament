import random


class Match:
    def __init__(self, player1, player2, score1=0.0, score2=0.0):
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2
        self.player1_color, self.player2_color = self.assign_colors()

    def set_result(self, winner=None):
        if winner is None:
            self.score1 = 0.5
            self.score2 = 0.5
        elif winner == self.player1:
            self.score1 = 1.0
            self.score2 = 0.0
        elif winner == self.player2:
            self.score1 = 0.0
            self.score2 = 1.0

    def add_to_dict(self):
        return {
            'player1': self.player1.add_to_dict(),
            'score1': self.score1,
            'player2': self.player2.add_to_dict(),
            'score2': self.score2,
            'player1_color': self.player1_color,
            'player2_color': self.player2_color
        }

    def assign_colors(self):
        """
        Assigne aléatoirement les couleurs aux joueurs.
        """
        colors = ["Blanc", "Noir"]
        random.shuffle(colors)
        return colors[0], colors[1]

    @classmethod
    def from_dict(cls, data, players):
        player1 = next(
            (player for player in players if
             player.national_id == data['player1']['national_id'])
        )
        player2 = next(player for player in players if
                       player.national_id == data['player2']['national_id'])
        score1 = data['score1']
        score2 = data['score2']
        match = cls(player1, player2, score1, score2)
        match.player1_color = data['player1_color']
        match.player2_color = data['player2_color']
        return match
