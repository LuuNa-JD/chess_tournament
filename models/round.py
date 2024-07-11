from datetime import datetime
from models.match import Match


class Round:
    def __init__(self, name, start_time=None, end_time=None):
        self.name = name
        self.start_time = start_time if isinstance(start_time, datetime) else datetime.now()
        self.end_time = end_time if isinstance(end_time, datetime) else None
        self.matches = []

    def add_match(self, match):
        self.matches.append(match)

    def end_round(self):
        self.end_time = datetime.now()

    def update_match_result(self, match_index, winner):
        self.matches[match_index].set_result(winner)

    def add_to_dict(self):
        return {
            'name': self.name,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'matches': [match.add_to_dict() for match in self.matches]
        }

    @classmethod
    def from_dict(cls, data, players):
        round_instance = cls(
            data['name'],
            datetime.fromisoformat(data['start_time']) if data['start_time'] else None,
            datetime.fromisoformat(data['end_time']) if data['end_time'] else None
        )
        round_instance.matches = [Match.from_dict(match, players) for match in data['matches']]
        return round_instance

    def formatted_start_time(self):
        return self.start_time.strftime("%d/%m/%Y %H:%M") if self.start_time else None

    def formatted_end_time(self):
        return self.end_time.strftime("%d/%m/%Y %H:%M") if self.end_time else None
