from typing import List

from board import Vertex, Edge


class Player:
    # Number of resources
    num_wood: int = 0
    num_brick: int = 0
    num_sheep: int = 0
    num_wheat: int = 0
    num_rock: int = 0

    # Number of each Development Card in hand
    num_year_of_plenty: int = 0
    num_monopoly: int = 0
    num_knight: int = 0  # Num of knights not played
    num_road_building: int = 0

    # Lists of settlements, cities, and roads
    settlements: List[Vertex] = []
    cities: List[Vertex] = []
    roads: List[Edge] = []

    # Counts used to calculate points
    knights_played: int = 0
    longest_road: int = 0

    score: int = 0
    color: str
    player_id: int

    def __init__(self, color: str, player_id):
        self.color = color
        self.player_id = player_id
