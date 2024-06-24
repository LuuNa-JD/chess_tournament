import json
from models.player import Player
from models.round import Round
from models.tournament import Tournament
from datetime import datetime


def test_tournament_creation():

    start_date = datetime.fromisoformat("2022-01-01").date()
    end_date = datetime.fromisoformat("2022-01-02").date()
    tournament = Tournament("Tournament", "Paris", start_date, end_date)
    assert tournament.name == "Tournament"
    assert tournament.location == "Paris"
    assert tournament.start_date == start_date
    assert tournament.end_date == end_date
    assert tournament.rounds == 4
    assert tournament.current_round == 0
    assert tournament.players == []
    assert tournament.round_list == []
    assert tournament.description == ""


def test_tournament_add_to_dict():
    start_date = datetime.fromisoformat("2022-01-01").date()
    end_date = datetime.fromisoformat("2022-01-02").date()
    tournament = Tournament("Tournament", "Paris", start_date, end_date)
    tournament.players = [
        Player("Potter", "Harry", datetime.fromisoformat("1995-01-01").date(),
               "AB123456")
        ]
    round_instance = Round("Round 1")
    tournament.round_list = [round_instance]

    result = tournament.add_to_dict()
    expected = {
        'name': 'Tournament',
        'location': 'Paris',
        'start_date': '2022-01-01',
        'end_date': '2022-01-02',
        'rounds': 4,
        'current_round': 0,
        'players': [{
            'last_name': 'Potter',
            'first_name': 'Harry',
            'birth_date': '1995-01-01',
            'national_id': 'AB123456',
            'points': 0
        }],
        'round_list': [{
            'name': 'Round 1',
            'start_time': round_instance.start_time,
            'end_time': None,
            'matches': []
        }],
        'description': ""
    }

    assert result['name'] == expected['name']
    assert result['location'] == expected['location']
    assert result['start_date'] == expected['start_date']
    assert result['end_date'] == expected['end_date']
    assert result['rounds'] == expected['rounds']
    assert result['current_round'] == expected['current_round']
    assert result['players'] == expected['players']
    assert result['description'] == expected['description']

    result_start_time = datetime.fromisoformat(
        result['round_list'][0]['start_time']
        )
    expected_start_time = datetime.fromisoformat(
        expected['round_list'][0]['start_time']
        )

    assert result_start_time == expected_start_time


def test_tournament_from_dict():
    now = datetime.now().isoformat()
    tournament_data = {
        'name': 'Tournament',
        'location': 'Paris',
        'start_date': '2022-01-01',
        'end_date': '2022-01-02',
        'rounds': 4,
        'current_round': 0,
        'players': [{
            'last_name': 'Potter',
            'first_name': 'Harry',
            'birth_date': '1995-01-01',
            'national_id': 'AB123456',
            'points': 0
        }],
        'round_list': [{
            'name': 'Round 1',
            'start_time': now,
            'end_time': None,
            'matches': []
        }],
        'description': ""
    }
    tournament = Tournament.from_dict(tournament_data)
    assert tournament.name == "Tournament"
    assert tournament.location == "Paris"
    assert tournament.start_date == datetime.fromisoformat("2022-01-01").date()
    assert tournament.end_date == datetime.fromisoformat("2022-01-02").date()
    assert tournament.rounds == 4
    assert tournament.current_round == 0
    assert len(tournament.players) == 1
    player = tournament.players[0]
    assert player.last_name == "Potter"
    assert player.first_name == "Harry"
    assert player.birth_date == datetime.fromisoformat("1995-01-01").date()
    assert player.national_id == "AB123456"
    assert player.points == 0
    assert len(tournament.round_list) == 1
    round_instance = tournament.round_list[0]
    assert round_instance.name == "Round 1"
    assert round_instance.start_time == now
    assert round_instance.end_time is None
    assert round_instance.matches == []

    parsed_start_time = datetime.fromisoformat(round_instance.start_time)
    now_parsed = datetime.fromisoformat(now)
    assert parsed_start_time == now_parsed


def test_tournament_add_player():
    start_date = datetime.fromisoformat("2022-01-01").date()
    end_date = datetime.fromisoformat("2022-01-02").date()
    tournament = Tournament("Tournament", "Paris", start_date, end_date)
    player = Player("Potter", "Harry",
                    datetime.fromisoformat("1995-01-01").date(), "AB123456"
                    )
    tournament.add_player(player)
    assert len(tournament.players) == 1
    assert tournament.players[0] == player


def test_tournament_add_round():
    start_date = datetime.fromisoformat("2022-01-01").date()
    end_date = datetime.fromisoformat("2022-01-02").date()
    tournament = Tournament("Tournament", "Paris", start_date, end_date)
    round = Round("Round 1")
    tournament.add_round(round)
    assert len(tournament.round_list) == 1
    assert tournament.round_list[0] == round


def test_tournament_load_tournaments(tmp_path):
    file_path = tmp_path / "tournaments.json"
    with open(file_path, 'w') as f:
        f.write(
            '[{"name": "Tournament", '
            '"location": "Paris", '
            '"start_date": "2022-01-01", '
            '"end_date": "2022-01-02", '
            '"rounds": 4, '
            '"current_round": 0, '
            '"players": [{"last_name": "Potter", '
            '"first_name": "Harry", '
            '"birth_date": "1995-01-01", '
            '"national_id": "AB123456", '
            '"points": 0}], '
            '"round_list": [{"name": "Round 1", "start_time": '
            '"2022-01-01T00:00:00", "end_time": null, '
            '"matches": []}], '
            '"description": ""}]'
        )
    tournaments = Tournament.load_tournaments(file_path)
    assert len(tournaments) == 1
    tournament = tournaments[0]
    assert tournament.name == "Tournament"
    assert tournament.location == "Paris"
    assert tournament.start_date == datetime.fromisoformat("2022-01-01").date()
    assert tournament.end_date == datetime.fromisoformat("2022-01-02").date()
    assert tournament.rounds == 4
    assert tournament.current_round == 0
    assert len(tournament.players) == 1
    player = tournament.players[0]
    assert player.last_name == "Potter"
    assert player.first_name == "Harry"
    assert player.birth_date == datetime.fromisoformat("1995-01-01").date()
    assert player.national_id == "AB123456"
    assert player.points == 0
    assert len(tournament.round_list) == 1
    round = tournament.round_list[0]
    assert round.name == "Round 1"
    assert round.start_time == "2022-01-01T00:00:00"
    assert round.end_time is None
    assert round.matches == []


def test_tournament_save_tournaments(tmp_path):
    file_path = tmp_path / "tournaments.json"
    start_date = datetime.fromisoformat("2022-01-01").date()
    end_date = datetime.fromisoformat("2022-01-02").date()
    tournament = Tournament("Tournament", "Paris", start_date, end_date)
    player = Player("Potter", "Harry",
                    datetime.fromisoformat("1995-01-01").date(),
                    "AB123456")
    tournament.players = [player]
    round_instance = Round("Round 1")
    tournament.round_list = [round_instance]
    Tournament.save_tournaments([tournament], file_path)

    with open(file_path, 'r') as f:
        tournaments_data = json.load(f)

    expected_data = [{
        'name': 'Tournament',
        'location': 'Paris',
        'start_date': '2022-01-01',
        'end_date': '2022-01-02',
        'rounds': 4,
        'current_round': 0,
        'players': [{
            'last_name': 'Potter',
            'first_name': 'Harry',
            'birth_date': '1995-01-01',
            'national_id': 'AB123456',
            'points': 0
        }],
        'round_list': [{
            'name': 'Round 1',
            'start_time': round_instance.start_time,
            'end_time': None,
            'matches': []
        }],
        'description': ""
    }]

    assert tournaments_data[0]['name'] == expected_data[0]['name']
    assert tournaments_data[0]['location'] == expected_data[0]['location']
    assert tournaments_data[0]['start_date'] == expected_data[0]['start_date']
    assert tournaments_data[0]['end_date'] == expected_data[0]['end_date']
    assert tournaments_data[0]['rounds'] == expected_data[0]['rounds']
    assert tournaments_data[0]['current_round'] == expected_data[0][
        'current_round']
    assert tournaments_data[0]['players'] == expected_data[0]['players']
    assert tournaments_data[0]['description'] == expected_data[0][
        'description']

    result_start_time = datetime.fromisoformat(
        tournaments_data[0]['round_list'][0]['start_time']
        )
    expected_start_time = datetime.fromisoformat(
        expected_data[0]['round_list'][0]['start_time']
        )
    assert result_start_time == expected_start_time
