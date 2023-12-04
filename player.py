from typing import List, Dict

from board_elements import Vertex, Edge, TileType


class Player:
    # Number of each Influence Tokens
    influenceTokens: int
    # Lists of settlements, cities, and roads
    settlements: List[Vertex]
    roads: List[Edge]

    # Counts used to calculate points
    mercenaries_played: int

    color: str
    player_id: int
    resources_dict: dict

    def __init__(self, color: str, player_id):
        self.color = color
        self.player_id = player_id
        self.resources_dict = {'lumber': 0, 'brick': 0, 'wool': 0, 'grain': 0, 'rock': 0}
        self.influenceTokens = 5
        self.mercenaries_played = 0
        self.settlements = []
        self.roads = []
        self.score = 0

    def resource_importance(self) -> List[str]:
        resource_scores: Dict[str, int] = {"brick": 0, "lumber": 0, "grain": 0, "wool": 0, "rock": 0, "desert": 0}

        for v in self.settlements:
            for t in v.adj_tiles:
                match t.tile_type:
                    case TileType.BRICK:
                        resource_scores["brick"] += 1
                    case TileType.LUMBER:
                        resource_scores["lumber"] += 1
                    case TileType.GRAIN:
                        resource_scores["grain"] += 1
                    case TileType.WOOL:
                        resource_scores["wool"] += 1
                    case TileType.ROCK:
                        resource_scores["rock"] += 1

        return sorted(resource_scores)
