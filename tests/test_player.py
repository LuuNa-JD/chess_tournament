import json
from models.player import Player
from datetime import datetime


def test_player_creation():

    birth_date = datetime.fromisoformat("1995-01-01").date()
    player = Player("Potter", "Harry", birth_date, "AB123456")
    assert player.last_name == "Potter"
    assert player.first_name == "Harry"
    assert player.birth_date == birth_date
    assert player.national_id == "AB123456"
    assert player.points == 0


def test_player_add_to_dict():

    birth_date = datetime.fromisoformat("1995-01-01").date()
    player = Player("Potter", "Harry", birth_date, "AB123456")
    player.points = 10
    assert player.add_to_dict() == {
        'last_name': 'Potter',
        'first_name': 'Harry',
        'birth_date': '1995-01-01',
        'national_id': 'AB123456',
        'points': 10
    }


def test_player_from_dict():
    player_data = {
        'last_name': 'Potter',
        'first_name': 'Harry',
        'birth_date': '1995-01-01',
        'national_id': 'AB123456',
        'points': 10
    }
    player = Player.from_dict(player_data)
    assert player.last_name == "Potter"
    assert player.first_name == "Harry"
    assert player.birth_date == datetime.fromisoformat("1995-01-01").date()
    assert player.national_id == "AB123456"
    assert player.points == 10


def test_player_load_players(tmp_path):
    file_path = tmp_path / "players.json"
    with open(file_path, 'w') as f:
        f.write('[{"last_name": "Potter", "first_name": "Harry", '
                '"birth_date": "1995-01-01", "national_id": "AB123456", '
                '"points": 10}]')
    players = Player.load_players(file_path)
    assert len(players) == 1
    player = players[0]
    assert player.last_name == "Potter"
    assert player.first_name == "Harry"
    assert player.birth_date == datetime.fromisoformat("1995-01-01").date()
    assert player.national_id == "AB123456"
    assert player.points == 10


def test_player_save_players(tmp_path):
    file_path = tmp_path / "players.json"
    player = Player("Potter", "Harry", datetime.fromisoformat(
        "1995-01-01").date(), "AB123456"
        )
    player.points = 10
    Player.save_players([player], file_path)

    with open(file_path, 'r') as f:
        players_data = json.load(f)

    expected_data = [{
        "last_name": "Potter",
        "first_name": "Harry",
        "birth_date": "1995-01-01",
        "national_id": "AB123456",
        "points": 10
    }]

    assert players_data == expected_data
