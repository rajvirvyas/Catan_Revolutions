import math
import random
import sys
from enum import Enum
from typing import Dict, List
from result import Result, Ok, Err
from graphics import Point, Rectangle, Polygon, Text, GraphWin, Circle

MAX_WOOD: int = 4
MAX_BRICK: int = 3
MAX_SHEEP: int = 4
MAX_WHEAT: int = 4
MAX_ROCK: int = 3

TWO_MAX: int = 1
THREE_MAX: int = 2
FOUR_MAX: int = 2
FIVE_MAX: int = 2
SIX_MAX: int = 2
EIGHT_MAX: int = 2
NINE_MAX: int = 2
TEN_MAX: int = 2
ELEVEN_MAX: int = 2
TWELVE_MAX: int = 1

BOARD_SIZE: int = 19


class TileType(Enum):
    WOOD = 0
    BRICK = 1
    SHEEP = 2
    WHEAT = 3
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
    owner: str
    color: str
    rect: Rectangle

    def __init__(self, rect: Rectangle):
        self.owner = ""
        self.color = ""
        self.rect = rect


class Vertex:
    pos: Point  # Vertex point
    adj_tiles: List[Tile]  # list of edge object references

    def __init__(self, pos: Point, adj_tiles: List[Tile]):
        self.pos = pos
        self.adj_tiles = adj_tiles

    def __hash__(self):
        return hash((self.pos.x, self.pos.y))

    def __eq__(self, other):
        return (self.pos.x, self.pos.y) == (other.pos.x, other.pos.y)


class Edge:
    v1: Vertex
    v2: Vertex
    road: Road = None

    def __init__(self, v1: Vertex, v2: Vertex):
        self.v1 = v1
        self.v2 = v2

    def __eq__(self, other):
        return (self.v1, self.v2) == (other.v1, other.v2)

    def add_road(self, road: Road):
        self.road = road


class BoardGraph:
    edges: List[Edge]
    vertices: List[Vertex]
    graph: Dict[Vertex, List[Edge]]

    def __init__(self):
        self.edges = []
        self.vertices = []
        self.graph = {}

    def add_vertex(self, vertex: Vertex) -> Result[str, str]:
        if self.contains_vertex(vertex):
            return Err("Already contains Vertex at this Point.")
        self.vertices.append(vertex)
        self.graph[vertex] = []
        return Ok("vertex")

    def contains_vertex(self, vertex: Vertex) -> bool:
        for v in self.vertices:
            if v.pos.x == vertex.pos.x and v.pos.y == vertex.pos.y:
                return True
        return False

    def contains_edge(self, edge: Edge) -> bool:
        if self.contains_vertex(edge.v1) and self.contains_vertex(edge.v2):
            v1_edges = self.graph[edge.v1]
            if v1_edges is None:
                return True
            for e in v1_edges:
                if edge == e:
                    return True
        return False

    def add_edge(self, edge: Edge) -> Result[str, str]:
        if self.contains_vertex(edge.v1) and self.contains_vertex(edge.v2):
            if self.contains_edge(edge):
                return Err("Already contains Edge")
            self.edges.append(edge)

            if self.graph[edge.v1] is None:
                self.graph[edge.v1] = [edge]
            else:
                self.graph[edge.v1].append(edge)
            if self.graph[edge.v2] is None:
                self.graph[edge.v2] = [edge]
            else:
                self.graph[edge.v2].append(edge)
        else:
            return Err("Edge Vertex not in Graph")

    def nearest_vertex(self, pos: Point) -> Point:
        min_distance: float = sys.float_info.max
        closest_point: Point = pos
        for v in self.vertices:
            distance: float = distance_between_points(v.pos, pos)
            if distance <= min_distance:
                min_distance = distance
                closest_point = v.pos

        return closest_point



class Board:
    bg: BoardGraph
    scale: float
    tiles: List[Tile]
    center: Point
    ocean: Polygon

    def __init__(self, scale: float, center: Point):
        self.scale = scale
        self.center = center
        self.tiles = generate_tiles(self.scale, self.center)
        self.bg = generate_board_graph(scale, center, self.tiles)
        self.ocean = create_background_hexagon(self.center, self.scale * 6)
        self.set_graphics()

    def set_graphics(self):
        self.ocean.setFill("Light Sea Green")
        self.ocean.setWidth(3)

        for h in self.tiles:
            h.shape.setFill(h.color)
            h.shape.setWidth(3)
            h.text.setSize(self.scale if self.scale <= 36 else 36)

    def draw_board(self, win: GraphWin):
        self.ocean.draw(win)

        for h in self.tiles:
            h.shape.draw(win)
            h.text.draw(win)

        # i = 0
        # for v in self.bg.vertices:
        #     c: Circle = Circle(v.pos, int(self.scale / 4))
        #     c.setFill("Red")
        #     c.draw(win)
        #     t: Text = Text(v.pos, str(i))
        #     t.setSize(int(self.scale / 4))
        #     t.draw(win)
        #     i += 1

def distance_between_points(p1: Point, p2: Point) -> float:
    return math.sqrt(math.fabs((p1.x - p2.x) ** 2) + math.fabs((p1.y - p2.y) ** 2))

def get_hexagon_center(hexagon: Polygon) -> Point:
    sum_x: int = 0
    sum_y: int = 0
    for p in hexagon.getPoints():
        sum_x += p.x
        sum_y += p.y

    return Point(sum_x / 6, sum_y / 6)


# Relates a TileType with a corresponding color, and returns the string for that color.
def tile_color(tile_type: TileType) -> str:
    match tile_type:
        case TileType.WOOD:
            return "Dark Olive Green"
        case TileType.BRICK:
            return "Brown"
        case TileType.SHEEP:
            return "Green Yellow"
        case TileType.WHEAT:
            return "Gold"
        case TileType.ROCK:
            return "Dim Gray"
        case _:
            return "Khaki"


# Relates an int with a corresponding TileType, and returns the TileType
def assign_tile_type(tile_type: int) -> TileType:
    match tile_type:
        case TileType.WOOD.value:
            return TileType.WOOD
        case TileType.BRICK.value:
            return TileType.BRICK
        case TileType.SHEEP.value:
            return TileType.SHEEP
        case TileType.WHEAT.value:
            return TileType.WHEAT
        case TileType.ROCK.value:
            return TileType.ROCK
        case _:
            return TileType.DESERT


def generate_tile_types(board_size: int) -> list[TileType]:
    wood_count: int = 0
    brick_count: int = 0
    sheep_count: int = 0
    wheat_count: int = 0
    rock_count: int = 0

    type_list: list[TileType] = []

    for i in range(board_size):
        if i == 9:
            type_list.append(TileType.DESERT)
            continue

        valid_type: bool = False
        while not valid_type:
            match random.randint(0, 4):
                case TileType.WOOD.value:
                    if wood_count < MAX_WOOD:
                        type_list.append(TileType.WOOD)
                        wood_count += 1
                        valid_type = True
                case TileType.BRICK.value:
                    if brick_count < MAX_BRICK:
                        type_list.append(TileType.BRICK)
                        brick_count += 1
                        valid_type = True
                case TileType.SHEEP.value:
                    if sheep_count < MAX_SHEEP:
                        type_list.append(TileType.SHEEP)
                        sheep_count += 1
                        valid_type = True
                case TileType.WHEAT.value:
                    if wheat_count < MAX_WHEAT:
                        type_list.append(TileType.WHEAT)
                        wheat_count += 1
                        valid_type = True
                case TileType.ROCK.value:
                    if rock_count < MAX_ROCK:
                        type_list.append(TileType.ROCK)
                        rock_count += 1
                        valid_type = True

    return type_list


def generate_tile_nums(board_size: int) -> list[int]:
    two_count: int = 0
    three_count: int = 0
    four_count: int = 0
    five_count: int = 0
    six_count: int = 0
    eight_count: int = 0
    nine_count: int = 0
    ten_count: int = 0
    eleven_count: int = 0
    twelve_count: int = 0

    num_list: list[int] = []

    for i in range(board_size):
        if i == 9:
            num_list.append(7)
            continue

        valid_num: bool = False
        while not valid_num:
            match random.randint(2, 12):
                case 2:
                    if two_count < TWO_MAX:
                        num_list.append(2)
                        two_count += 1
                        valid_num = True
                case 3:
                    if three_count < THREE_MAX:
                        num_list.append(3)
                        three_count += 1
                        valid_num = True
                case 4:
                    if four_count < FOUR_MAX:
                        num_list.append(4)
                        four_count += 1
                        valid_num = True
                case 5:
                    if five_count < FIVE_MAX:
                        num_list.append(5)
                        five_count += 1
                        valid_num = True
                case 6:
                    if six_count < SIX_MAX:
                        num_list.append(6)
                        six_count += 1
                        valid_num = True
                case 8:
                    if eight_count < EIGHT_MAX:
                        num_list.append(8)
                        eight_count += 1
                        valid_num = True
                case 9:
                    if nine_count < NINE_MAX:
                        num_list.append(9)
                        nine_count += 1
                        valid_num = True
                case 10:
                    if ten_count < TEN_MAX:
                        num_list.append(10)
                        ten_count += 1
                        valid_num = True
                case 11:
                    if eleven_count < ELEVEN_MAX:
                        num_list.append(11)
                        eleven_count += 1
                        valid_num = True
                case 12:
                    if twelve_count < TWELVE_MAX:
                        num_list.append(12)
                        twelve_count += 1
                        valid_num = True

    return num_list


def create_tile_hexagon(center: Point, scale: float) -> Polygon:
    x: float = center.x
    y: float = center.y
    d: float = math.sqrt(3) / 2
    return Polygon(Point(x, y + scale), Point(x + d * scale, y + scale / 2), Point(x + d * scale, y - scale / 2),
                   Point(x, y - scale), Point(x - d * scale, y - scale / 2), Point(x - d * scale, y + scale / 2))


def create_background_hexagon(center: Point, scale: float) -> Polygon:
    x: float = center.x
    y: float = center.y
    d: float = math.sqrt(3) / 2
    return Polygon(Point(x + scale, y), Point(x + scale / 2, y - d * scale), Point(x - scale / 2, y - d * scale),
                   Point(x - scale, y), Point(x - scale / 2, y + d * scale), Point(x + scale / 2, y + d * scale))


def generate_tiles(scale: float, board_center: Point) -> List[Tile]:
    d: float = math.sqrt(3) / 2
    tile_positions: List[Polygon] = [
        create_tile_hexagon(Point(board_center.x - d * 2 * scale, board_center.y + 3 * scale), scale),  # Tile 0
        create_tile_hexagon(Point(board_center.x, board_center.y + 3 * scale), scale),  # Tile 1
        create_tile_hexagon(Point(board_center.x + d * 2 * scale, board_center.y + 3 * scale), scale),  # Tile 2
        create_tile_hexagon(Point(board_center.x - d * 3 * scale, board_center.y + 1.5 * scale), scale),  # Tile 3
        create_tile_hexagon(Point(board_center.x - d * scale, board_center.y + 1.5 * scale), scale),  # Tile 4
        create_tile_hexagon(Point(board_center.x + d * scale, board_center.y + 1.5 * scale), scale),  # Tile 5
        create_tile_hexagon(Point(board_center.x + d * 3 * scale, board_center.y + 1.5 * scale), scale),  # Tile 6
        create_tile_hexagon(Point(board_center.x - d * 2 * scale, board_center.y), scale),  # Tile 7
        create_tile_hexagon(Point(board_center.x - d * 4 * scale, board_center.y), scale),  # Tile 8
        create_tile_hexagon(board_center, scale),  # Tile 9 (Desert)
        create_tile_hexagon(Point(board_center.x + d * 2 * scale, board_center.y), scale),  # Tile 10
        create_tile_hexagon(Point(board_center.x + d * 4 * scale, board_center.y), scale),  # Tile 11
        create_tile_hexagon(Point(board_center.x - d * 3 * scale, board_center.y - 1.5 * scale), scale),  # Tile 12
        create_tile_hexagon(Point(board_center.x - d * scale, board_center.y - 1.5 * scale), scale),  # Tile 13
        create_tile_hexagon(Point(board_center.x + d * scale, board_center.y - 1.5 * scale), scale),  # Tile 14
        create_tile_hexagon(Point(board_center.x + d * 3 * scale, board_center.y - 1.5 * scale), scale),  # Tile 15
        create_tile_hexagon(Point(board_center.x - d * 2 * scale, board_center.y - 3 * scale), scale),  # Tile 16
        create_tile_hexagon(Point(board_center.x, board_center.y - 3 * scale), scale),  # Tile 17
        create_tile_hexagon(Point(board_center.x + d * 2 * scale, board_center.y - 3 * scale), scale)  # Tile 18
    ]
    tiles: List[Tile] = []
    type_list: List[TileType] = generate_tile_types(len(tile_positions))
    num_list: List[int] = generate_tile_nums(len(tile_positions))

    for i in range(len(tile_positions)):
        tiles.append(Tile(type_list[i], tile_positions[i], num_list[i]))

    return tiles


def generate_vertices(scale: float, center: Point, tiles: list[Tile]) -> List[Vertex]:
    vertices: List[Vertex] = []
    d: float = math.sqrt(3) / 2

    # Row 0
    vertices.append(Vertex(Point(center.x - d * 3 * scale, center.y - 3.5 * scale), [tiles[0]]))
    vertices.append(Vertex(Point(center.x - d * 2 * scale, center.y - 4.0 * scale), [tiles[0]]))
    vertices.append(Vertex(Point(center.x - d * 1 * scale, center.y - 3.5 * scale), [tiles[0], tiles[1]]))
    vertices.append(Vertex(Point(center.x - d * 0 * scale, center.y - 4.0 * scale), [tiles[1]]))
    vertices.append(Vertex(Point(center.x + d * 1 * scale, center.y - 3.5 * scale), [tiles[1], tiles[2]]))
    vertices.append(Vertex(Point(center.x + d * 2 * scale, center.y - 4.0 * scale), [tiles[2]]))
    vertices.append(Vertex(Point(center.x + d * 3 * scale, center.y - 3.5 * scale), [tiles[2]]))
    # Row 1
    vertices.append(Vertex(Point(center.x - d * 4 * scale, center.y - 2.0 * scale), [tiles[3]]))
    vertices.append(Vertex(Point(center.x - d * 3 * scale, center.y - 2.5 * scale), [tiles[0], tiles[3]]))
    vertices.append(Vertex(Point(center.x - d * 2 * scale, center.y - 2.0 * scale), [tiles[0], tiles[3], tiles[4]]))
    vertices.append(Vertex(Point(center.x - d * 1 * scale, center.y - 2.5 * scale), [tiles[0], tiles[1], tiles[4]]))
    vertices.append(Vertex(Point(center.x - d * 0 * scale, center.y - 2.0 * scale), [tiles[1], tiles[4], tiles[5]]))
    vertices.append(Vertex(Point(center.x + d * 1 * scale, center.y - 2.5 * scale), [tiles[1], tiles[2], tiles[5]]))
    vertices.append(Vertex(Point(center.x + d * 2 * scale, center.y - 2.0 * scale), [tiles[2], tiles[5], tiles[6]]))
    vertices.append(Vertex(Point(center.x + d * 3 * scale, center.y - 2.5 * scale), [tiles[2], tiles[6]]))
    vertices.append(Vertex(Point(center.x + d * 4 * scale, center.y - 2.0 * scale), [tiles[6]]))
    # Row 2
    vertices.append(Vertex(Point(center.x - d * 5 * scale, center.y - 0.5 * scale), [tiles[7]]))
    vertices.append(Vertex(Point(center.x - d * 4 * scale, center.y - 1.0 * scale), [tiles[3], tiles[7]]))
    vertices.append(Vertex(Point(center.x - d * 3 * scale, center.y - 0.5 * scale), [tiles[3], tiles[7], tiles[8]]))
    vertices.append(Vertex(Point(center.x - d * 2 * scale, center.y - 1.0 * scale), [tiles[3], tiles[4], tiles[8]]))
    vertices.append(Vertex(Point(center.x - d * 1 * scale, center.y - 0.5 * scale), [tiles[4], tiles[8], tiles[9]]))
    vertices.append(Vertex(Point(center.x - d * 0 * scale, center.y - 1.0 * scale), [tiles[4], tiles[5], tiles[9]]))
    vertices.append(Vertex(Point(center.x + d * 1 * scale, center.y - 0.5 * scale), [tiles[5], tiles[9], tiles[10]]))
    vertices.append(Vertex(Point(center.x + d * 2 * scale, center.y - 1.0 * scale), [tiles[5], tiles[6], tiles[10]]))
    vertices.append(Vertex(Point(center.x + d * 3 * scale, center.y - 0.5 * scale), [tiles[6], tiles[10], tiles[11]]))
    vertices.append(Vertex(Point(center.x + d * 4 * scale, center.y - 1.0 * scale), [tiles[6], tiles[11]]))
    vertices.append(Vertex(Point(center.x + d * 5 * scale, center.y - 0.5 * scale), [tiles[11]]))
    # Row 3
    vertices.append(Vertex(Point(center.x - d * 5 * scale, center.y + 0.5 * scale), [tiles[7]]))
    vertices.append(Vertex(Point(center.x - d * 4 * scale, center.y + 1.0 * scale), [tiles[7], tiles[12]]))
    vertices.append(Vertex(Point(center.x - d * 3 * scale, center.y + 0.5 * scale), [tiles[7], tiles[8], tiles[12]]))
    vertices.append(Vertex(Point(center.x - d * 2 * scale, center.y + 1.0 * scale), [tiles[8], tiles[12], tiles[13]]))
    vertices.append(Vertex(Point(center.x - d * 1 * scale, center.y + 0.5 * scale), [tiles[8], tiles[9], tiles[13]]))
    vertices.append(Vertex(Point(center.x - d * 0 * scale, center.y + 1.0 * scale), [tiles[9], tiles[13], tiles[14]]))
    vertices.append(Vertex(Point(center.x + d * 1 * scale, center.y + 0.5 * scale), [tiles[9], tiles[10], tiles[14]]))
    vertices.append(Vertex(Point(center.x + d * 2 * scale, center.y + 1.0 * scale), [tiles[10], tiles[14], tiles[15]]))
    vertices.append(Vertex(Point(center.x + d * 3 * scale, center.y + 0.5 * scale), [tiles[10], tiles[11], tiles[15]]))
    vertices.append(Vertex(Point(center.x + d * 4 * scale, center.y + 1.0 * scale), [tiles[11], tiles[15]]))
    vertices.append(Vertex(Point(center.x + d * 5 * scale, center.y + 0.5 * scale), [tiles[11]]))
    # Row 4
    vertices.append(Vertex(Point(center.x - d * 4 * scale, center.y + 2.0 * scale), [tiles[12]]))
    vertices.append(Vertex(Point(center.x - d * 3 * scale, center.y + 2.5 * scale), [tiles[12], tiles[16]]))
    vertices.append(Vertex(Point(center.x - d * 2 * scale, center.y + 2.0 * scale), [tiles[12], tiles[13], tiles[16]]))
    vertices.append(Vertex(Point(center.x - d * 1 * scale, center.y + 2.5 * scale), [tiles[13], tiles[16], tiles[17]]))
    vertices.append(Vertex(Point(center.x - d * 0 * scale, center.y + 2.0 * scale), [tiles[13], tiles[14], tiles[17]]))
    vertices.append(Vertex(Point(center.x + d * 1 * scale, center.y + 2.5 * scale), [tiles[14], tiles[17], tiles[18]]))
    vertices.append(Vertex(Point(center.x + d * 2 * scale, center.y + 2.0 * scale), [tiles[14], tiles[15], tiles[18]]))
    vertices.append(Vertex(Point(center.x + d * 3 * scale, center.y + 2.5 * scale), [tiles[15], tiles[18]]))
    vertices.append(Vertex(Point(center.x + d * 4 * scale, center.y + 2.0 * scale), [tiles[15]]))
    # Row 5
    vertices.append(Vertex(Point(center.x - d * 3 * scale, center.y + 3.5 * scale), [tiles[16]]))
    vertices.append(Vertex(Point(center.x - d * 2 * scale, center.y + 4.0 * scale), [tiles[16]]))
    vertices.append(Vertex(Point(center.x - d * 1 * scale, center.y + 3.5 * scale), [tiles[16], tiles[17]]))
    vertices.append(Vertex(Point(center.x - d * 0 * scale, center.y + 4.0 * scale), [tiles[17]]))
    vertices.append(Vertex(Point(center.x + d * 1 * scale, center.y + 3.5 * scale), [tiles[17], tiles[18]]))
    vertices.append(Vertex(Point(center.x + d * 2 * scale, center.y + 4.0 * scale), [tiles[18]]))
    vertices.append(Vertex(Point(center.x + d * 3 * scale, center.y + 3.5 * scale), [tiles[18]]))

    return vertices


def generate_edges(vertices: List[Vertex]) -> List[Edge]:
    edges: List[Edge] = []

    # Rows include vertical edge above vertex
    # Row 0
    edges.append(Edge(vertices[0], vertices[1]))
    edges.append(Edge(vertices[1], vertices[2]))
    edges.append(Edge(vertices[2], vertices[3]))
    edges.append(Edge(vertices[3], vertices[4]))
    edges.append(Edge(vertices[4], vertices[5]))
    edges.append(Edge(vertices[5], vertices[6]))
    # Row 1
    edges.append(Edge(vertices[7], vertices[8]))
    edges.append(Edge(vertices[0], vertices[8]))
    edges.append(Edge(vertices[8], vertices[9]))
    edges.append(Edge(vertices[9], vertices[10]))
    edges.append(Edge(vertices[2], vertices[10]))
    edges.append(Edge(vertices[10], vertices[11]))
    edges.append(Edge(vertices[11], vertices[12]))
    edges.append(Edge(vertices[4], vertices[12]))
    edges.append(Edge(vertices[12], vertices[13]))
    edges.append(Edge(vertices[13], vertices[14]))
    edges.append(Edge(vertices[6], vertices[14]))
    edges.append(Edge(vertices[14], vertices[15]))
    # Row 2
    edges.append(Edge(vertices[16], vertices[17]))
    edges.append(Edge(vertices[7], vertices[17]))
    edges.append(Edge(vertices[17], vertices[18]))
    edges.append(Edge(vertices[18], vertices[19]))
    edges.append(Edge(vertices[9], vertices[19]))
    edges.append(Edge(vertices[19], vertices[20]))
    edges.append(Edge(vertices[20], vertices[21]))
    edges.append(Edge(vertices[11], vertices[21]))
    edges.append(Edge(vertices[21], vertices[22]))
    edges.append(Edge(vertices[22], vertices[23]))
    edges.append(Edge(vertices[13], vertices[23]))
    edges.append(Edge(vertices[23], vertices[24]))
    edges.append(Edge(vertices[24], vertices[25]))
    edges.append(Edge(vertices[15], vertices[25]))
    edges.append(Edge(vertices[25], vertices[26]))
    # Row 3
    edges.append(Edge(vertices[16], vertices[27]))
    edges.append(Edge(vertices[27], vertices[28]))
    edges.append(Edge(vertices[28], vertices[29]))
    edges.append(Edge(vertices[18], vertices[29]))
    edges.append(Edge(vertices[29], vertices[30]))
    edges.append(Edge(vertices[30], vertices[30]))
    edges.append(Edge(vertices[20], vertices[31]))
    edges.append(Edge(vertices[31], vertices[32]))
    edges.append(Edge(vertices[32], vertices[33]))
    edges.append(Edge(vertices[22], vertices[33]))
    edges.append(Edge(vertices[33], vertices[34]))
    edges.append(Edge(vertices[34], vertices[35]))
    edges.append(Edge(vertices[24], vertices[35]))
    edges.append(Edge(vertices[35], vertices[36]))
    edges.append(Edge(vertices[36], vertices[37]))
    edges.append(Edge(vertices[26], vertices[37]))
    # Row 4
    edges.append(Edge(vertices[28], vertices[38]))
    edges.append(Edge(vertices[38], vertices[39]))
    edges.append(Edge(vertices[39], vertices[40]))
    edges.append(Edge(vertices[30], vertices[40]))
    edges.append(Edge(vertices[40], vertices[41]))
    edges.append(Edge(vertices[41], vertices[42]))
    edges.append(Edge(vertices[32], vertices[42]))
    edges.append(Edge(vertices[42], vertices[43]))
    edges.append(Edge(vertices[43], vertices[44]))
    edges.append(Edge(vertices[34], vertices[44]))
    edges.append(Edge(vertices[44], vertices[45]))
    edges.append(Edge(vertices[45], vertices[46]))
    edges.append(Edge(vertices[36], vertices[46]))
    # Row 5
    edges.append(Edge(vertices[39], vertices[47]))
    edges.append(Edge(vertices[47], vertices[48]))
    edges.append(Edge(vertices[48], vertices[49]))
    edges.append(Edge(vertices[41], vertices[49]))
    edges.append(Edge(vertices[49], vertices[50]))
    edges.append(Edge(vertices[50], vertices[51]))
    edges.append(Edge(vertices[43], vertices[51]))
    edges.append(Edge(vertices[51], vertices[52]))
    edges.append(Edge(vertices[52], vertices[53]))
    edges.append(Edge(vertices[45], vertices[53]))

    return edges


def generate_board_graph(scale: float, center: Point, tiles: List[Tile]) -> BoardGraph:
    board_graph: BoardGraph = BoardGraph()

    vertices: List[Vertex] = generate_vertices(scale, center, tiles)
    edges: List[Edge] = generate_edges(vertices)

    for v in vertices:
        board_graph.add_vertex(v)

    for e in edges:
        board_graph.add_edge(e)

    return board_graph
