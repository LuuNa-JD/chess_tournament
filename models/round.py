from datetime import datetime
from models.match import Match


class Round:
    """
    Classe représentant un tour dans un tournoi.
    """

    def __init__(self, name, start_time=None, end_time=None):
        """
        Initialise un nouveau tour.

        Arguments:
            name (str): Le nom du tour.
            start_time (datetime, optional): Le temps de début du tour. Si non fourni, prend l'heure actuelle.
            end_time (datetime, optional): Le temps de fin du tour. Si non fourni, initialise à None.
        """
        self.name = name
        self.start_time = start_time if isinstance(start_time, datetime) else datetime.now()
        self.end_time = end_time if isinstance(end_time, datetime) else None
        self.matches = []  # Initialise une liste vide pour les matchs du tour

    def add_match(self, match):
        """
        Ajoute un match au tour.
        """
        self.matches.append(match)  # Ajoute le match à la liste des matchs

    def end_round(self):
        """
        Termine le tour en enregistrant l'heure actuelle comme heure de fin.
        """
        self.end_time = datetime.now()   # Enregistre l'heure actuelle comme temps de fin du tour

    def update_match_result(self, match_index, winner):
        """
        Met à jour le résultat d'un match.
        """
        self.matches[match_index].set_result(winner)  # Met à jour le résultat du match spécifié par son index

    def add_to_dict(self):
        """
        Convertit les détails du tour en dictionnaire.

        La méthode retourne un dictionnaire contenant les informations du tour.
        """
        return {
            'name': self.name,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'matches': [match.add_to_dict() for match in self.matches]  # Ajoute la liste des matchs convertis en dict
        }

    @classmethod
    def from_dict(cls, data, players):
        """
        Crée une instance de Round à partir d'un dictionnaire.

        La méthode retourne une instance de Round initialisée avec les données fournies.
        """
        round_instance = cls(
            data['name'],
            datetime.fromisoformat(data['start_time']) if data['start_time'] else None,
            datetime.fromisoformat(data['end_time']) if data['end_time'] else None
        )
        round_instance.matches = [Match.from_dict(match, players) for match in data['matches']]
        return round_instance  # Retourne l'instance de Round créée

    def formatted_start_time(self):
        """
        Retourne le temps de début formaté.
        """
        return self.start_time.strftime("%d/%m/%Y %H:%M") if self.start_time else None

    def formatted_end_time(self):
        """
        Retourne le temps de fin formaté.
        """
        return self.end_time.strftime("%d/%m/%Y %H:%M") if self.end_time else None
