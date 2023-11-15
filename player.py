from typing import List

from board import Vertex, Edge


class Player:
    # Number of resources
    
    resources_dict = {'wood': 0, 'brick': 0, 'sheep': 0, 'wheat': 0, 'rock': 0}

    # Number of each Development Card in hand
    dev_dict= {'yearOfPlenty' : 0, 'monopoly' : 0, 'knightsNotPlayed' : 0, 'road_building' : 0}
  
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