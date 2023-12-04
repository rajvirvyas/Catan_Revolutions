from enum import Enum
from typing import List

from graphics import Polygon, Text, Point


class TileType(Enum):
    LUMBER = 0
    BRICK = 1
    WOOL = 2
    GRAIN = 3
    ROCK = 4
    DESERT = 5


class Tile:
    tile_type: TileType
    shape: Polygon
    text: Text
    color: str
    num: int
    center: Point
    has_bishop: bool

    def __init__(self, tile_type: TileType, hexagon: Polygon, num: int, has_bishop=False):
        self.tile_type = tile_type
        self.shape = hexagon
        self.color = tile_color(tile_type)
        self.num = num
        self.center = get_hexagon_center(hexagon)
        self.has_bishop = has_bishop
        self.text = Text(get_hexagon_center(hexagon), str(num))


class Road:
    rect: Polygon
    player_id: int

    def __init__(self, rect: Polygon, player_id):
        self.rect = rect
        self.player_id = player_id


class Settlement:
    player_id: int
    is_city: bool

    def __init__(self, player_id: int):
        self.player_id = player_id
        self.is_city = False

    def make_city(self):
        self.is_city = True


class Vertex:
    pos: Point  # Vertex point
    adj_tiles: List[Tile]  # list of edge object references
    settlement: Settlement

    def __init__(self, pos: Point, adj_tiles: List[Tile]):
        self.pos = pos
        self.adj_tiles = adj_tiles
        self.settlement = None

    def __hash__(self):
        return hash((self.pos.x, self.pos.y))

    def __eq__(self, other):
        return (self.pos.x, self.pos.y) == (other.pos.x, other.pos.y)

    def add_settlement(self, player_id: int):
        self.settlement = Settlement(player_id)

    def make_city(self):
        self.settlement.make_city()


class Edge:
    v1: Vertex
    v2: Vertex
    road: Road
    center: Point

    def __init__(self, v1: Vertex, v2: Vertex):
        self.v1 = v1
        self.v2 = v2
        self.center = Point((v1.pos.x + v2.pos.x) / 2, (v1.pos.y + v2.pos.y) / 2)
        self.road = None

    def __eq__(self, other):
        return (self.v1, self.v2) == (other.v1, other.v2)

    def has_road(self) -> bool:
        if self.road is not None:
            return True
        else:
            return False

    def add_road(self, player_id: int, poly: Polygon) -> bool:
        if self.road is not None:
            return False

        self.road = Road(poly, player_id)
        return True

    # Relates a TileType with a corresponding color, and returns the string for that color.


def tile_color(tile_type: TileType) -> str:
    match tile_type:
        case TileType.LUMBER:
            return "Dark Olive Green"
        case TileType.BRICK:
            return "Brown"
        case TileType.WOOL:
            return "Green Yellow"
        case TileType.GRAIN:
            return "Gold"
        case TileType.ROCK:
            return "Dim Gray"
        case _:
            return "Khaki"


def get_hexagon_center(hexagon: Polygon) -> Point:
    sum_x: int = 0
    sum_y: int = 0
    for p in hexagon.getPoints():
        sum_x += p.x
        sum_y += p.y

    return Point(sum_x / 6, sum_y / 6)
