import unittest
from typing import Dict

import Main
from Main import Action
from board import Board, BoardGraph
from board_elements import Road, Vertex
from graphics import GraphWin, Point, Circle, Polygon, Text
from player import Player


class MyTestCase(unittest.TestCase):
    def test_settlement_placement(self):
        win = GraphWin("Catan Board", 1000, 700)
        scale: float = 50.0
        center: Point = Point(500, 350)
        board: Board = Board(scale, center)
        player1: Player = Player("Blue", 0)

        action: Action = Action.BUILD_SETTLEMENT

        Main.build_road(board.bg, board.bg.edges[0].center, scale, player1)
        self.assertTrue(board.bg.build_settlement(board.bg.vertices[0].pos, player1.player_id))
        self.assertFalse(board.bg.build_settlement(board.bg.vertices[0].pos, player1.player_id))
        self.assertFalse(board.bg.build_settlement(board.bg.vertices[1].pos, player1.player_id))
        self.assertFalse(board.bg.build_settlement(board.bg.vertices[10].pos, player1.player_id))

        win.close()

    def test_build_road(self):
        win = GraphWin("Catan Board", 1000, 700)
        scale: float = 50.0
        center: Point = Point(500, 350)
        board: Board = Board(scale, center)
        bg: BoardGraph = board.bg
        board.draw_board(win)
        placement_poly: Polygon = Main.road_poly(bg.nearest_edge(Point(0.0, 0.0)), 30)
        center = bg.nearest_edge(Point(0.0, 0.0)).center
        placement_poly.setFill("Red")
        placement_poly_drawn: bool = False
        objects = []
        player1: Player = Player("Blue", 0)
        action: Action = Action.BUILD_ROAD
        first_poly = Main.road_poly(bg.nearest_edge(Point(0, 0)), scale)
        bg.edges[7].road = Road(first_poly, player1.player_id)
        first_poly.setFill("Blue")
        first_poly.draw(win)

        while True:
            match action:
                case Action.BUILD_ROAD:
                    if not placement_poly_drawn:
                        placement_poly.draw(win)
                        placement_poly_drawn = True
                    x = win.winfo_pointerx()
                    y = win.winfo_pointery()
                    abs_coord_x = x - win.winfo_rootx()
                    abs_coord_y = y - win.winfo_rooty()
                    new_center = bg.nearest_edge(Point(abs_coord_x, abs_coord_y)).center
                    if new_center != center:
                        placement_poly.undraw()
                        placement_poly = Main.road_poly(bg.nearest_edge(Point(abs_coord_x, abs_coord_y)), scale)
                        placement_poly.setFill("Red")
                        placement_poly.draw(win)
                        center = bg.nearest_edge(Point(abs_coord_x, abs_coord_y)).center
                    # print(Point(center.x - new_center.x, center.y - new_center.y))
                    road_poly: Polygon = placement_poly.clone()
                    current_pos = win.checkMouse()
                    if current_pos is not None and bg.build_road(current_pos, road_poly, player1.player_id):
                        road_poly.setFill("Blue")
                        road_poly.draw(win)
                        objects.append(road_poly)
                case _:
                    placement_poly.undraw()
                    placement_poly_drawn = False

        win.close()

    def test_distance_calculator(self):
        win = GraphWin("Catan Board", 1000, 700)
        scale: float = 50.0
        center: Point = Point(500, 350)
        board: Board = Board(scale, center)
        board.draw_board(win)
        bg: BoardGraph = board.bg
        player1: Player = Player("Blue", 0)
        circle1 = Circle(bg.vertices[11].pos, 20.0)
        circle1.setFill(player1.color)
        circle1.draw(win)
        circle2 = Circle(bg.vertices[17].pos, 20.0)
        circle2.setFill(player1.color)
        circle2.draw(win)
        circle3 = Circle(bg.vertices[25].pos, 20.0)
        circle3.setFill(player1.color)
        circle3.draw(win)

        self.assertTrue(bg.build_settlement(bg.vertices[17].pos, player1, True))
        self.assertTrue(bg.build_settlement(bg.vertices[11].pos, player1, True))
        self.assertTrue(bg.build_settlement(bg.vertices[25].pos, player1, True))

        distances: Dict[Vertex, int] = bg.best_settlement_locations(player1)
        print(distances)

        for v in distances.keys():
            t: Text = Text(v.pos, str(distances[v]))
            t.setFill("Red")
            t.setSize(scale if scale <= 36 else 36)
            t.draw(win)

        win.getMouse()
        win.close()


if __name__ == '__main__':
    unittest.main()
