from typing import List

from board import Vertex, Edge


class Player:
    # Number of resources
    
    resources_dict = {'lumber': 0, 'ore': 0, 'wool': 0, 'grain': 0, 'rock': 0}

    # Number of each Influence Tokens
    influenceTokens=5
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