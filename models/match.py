from models.player import Player


class Match:

    def __init__(self, player1, player2, score1=0.5, score2=0.5):
        self.match = ([player1, score1], [player2, score2])

    def set_result(self, score1, score2):
        self.match[0][1] = score1
        self.match[1][1] = score2

    def add_to_dict(self):
        return {
            'player1': self.match[0][0].to_dict(),
            'score1': self.match[0][1],
            'player2': self.match[1][0].to_dict(),
            'score2': self.match[1][1]
        }

    @classmethod
    def from_dict(cls, data):
        player1 = Player.from_dict(data['player1'])
        player2 = Player.from_dict(data['player2'])
        match = cls(player1, player2, data['score1'], data['score2'])
        return match
