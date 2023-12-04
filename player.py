from typing import List

from board import Vertex, Edge


class Player:
    # Number of each Influence Tokens
    influenceTokens=int

    # Lists of settlements, cities, and roads
    settlements: List[Vertex] = []
    cities: List[Vertex] = []
    roads: List[Edge] = []

    score: int = 0
    color: str
    player_id: int
    resources_dict: dict

    def __init__(self, color: str, player_id):
        self.color = color
        self.player_id = player_id
        self.resources_dict = {'lumber': 0, 'brick': 0, 'wool': 0, 'grain': 0, 'rock': 0}
        self.score= 0
        self.influenceTokens=5