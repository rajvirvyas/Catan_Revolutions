import math
from enum import Enum

from board import Board, BoardGraph, Edge
from graphics import *
from dice import *
from tkinter import *
from player import Player
from dice import *
from tkinter import *

ROAD_WIDTH: int = 10

win = GraphWin("Catan Board", 1000, 700)


class Action(Enum):
    NOTHING: int = 0
    ROLL_DICE: int = 1
    BUILD_SETTLEMENT: int = 2
    BUILD_CITY: int = 3
    BUILD_ROAD: int = 4
    BUILD_DEV_CARD: int = 5
    TRADE_BANK: int = 6
    TRADE_PLAYER: int = 7
    PLAY_DEV_CARD: int = 8


def road_poly(e: Edge, scale: float) -> Polygon:
    v1x: int = e.v1.pos.x
    v1y: int = e.v1.pos.y
    v2x: int = e.v2.pos.x
    v2y: int = e.v2.pos.y

    if v1x < v2x and v1y < v2y:
        return Polygon(Point(v1x + scale / 2 / ROAD_WIDTH, v1y - scale / 2 / ROAD_WIDTH * math.sqrt(3)),
                       Point(v1x - scale / 2 / ROAD_WIDTH, v1y + scale / 2 / ROAD_WIDTH * math.sqrt(3)),
                       Point(v2x - scale / 2 / ROAD_WIDTH, v2y + scale / 2 / ROAD_WIDTH * math.sqrt(3)),
                       Point(v2x + scale / 2 / ROAD_WIDTH, v2y - scale / 2 / ROAD_WIDTH * math.sqrt(3)))
    elif v1x < v2x and v1y > v2y:
        return Polygon(Point(v1x - scale / 2 / ROAD_WIDTH, v1y - scale / 2 / ROAD_WIDTH * math.sqrt(3)),
                       Point(v1x + scale / 2 / ROAD_WIDTH, v1y + scale / 2 / ROAD_WIDTH * math.sqrt(3)),
                       Point(v2x + scale / 2 / ROAD_WIDTH, v2y + scale / 2 / ROAD_WIDTH * math.sqrt(3)),
                       Point(v2x - scale / 2 / ROAD_WIDTH, v2y - scale / 2 / ROAD_WIDTH * math.sqrt(3)))
    else:
        return Polygon(Point(v1x + scale / 10, v1y), Point(v1x - scale / 10, v1y),
                       Point(v2x - scale / 10, v2y), Point(v2x + scale / 10, v2y))


def build_road(bg: BoardGraph, pos: Point, scale: float, player: Player) -> bool:
    e: Edge = bg.nearest_edge(pos)

    if not bg.can_build_road(pos, player.player_id):
        return False

    poly: Polygon = road_poly(e, scale)

    poly.setFill(player.color)
    result = e.add_road(player.player_id, poly)
    if result:
        poly.draw(win)
        return True
    return False






def main():
    scale: float = 50.0
    center: Point = Point(500, 350)
    board: Board = Board(scale, center)
    board.draw_board(win)

    placement_circle: Circle = Circle(Point(0.0, 0.0), 20.0)
    placement_circle.setFill("Red")
    placement_circle_drawn: bool = False
    objects = []

    player1: Player = Player("Blue", 0)

    action: Action = Action.BUILD_SETTLEMENT

    while True:
        match action:
            case Action.BUILD_SETTLEMENT:
                if not placement_circle_drawn:
                    placement_circle.draw(win)
                    placement_circle_drawn = True
                x = win.winfo_pointerx()
                y = win.winfo_pointery()
                abs_coord_x = x - win.winfo_rootx()
                abs_coord_y = y - win.winfo_rooty()
                new_point: Point = board.bg.nearest_vertex_point(Point(abs_coord_x, abs_coord_y))
                placement_circle.move(new_point.x - placement_circle.getCenter().x,
                                      new_point.y - placement_circle.getCenter().y)
                if win.checkMouse() is not None and board.bg.can_build_settlement(new_point, player1.player_id):
                    settlement: placement_circle = Circle(new_point, 20.0)
                    settlement.setFill("Blue")
                    settlement.draw(win)
                    objects.append(settlement)
            case _:
                placement_circle.undraw()
                placement_circle_drawn = False


    circle: Circle = Circle(Point(0.0, 0.0), 20.0)
    circle.setFill("Red")
    circle.draw(win)

# For Dice-----------------------------------------------------------------------------

    # For Dice-----------------------------------------------------------------------------

    l1 = Label(win, font=("Helvetica", 150), text='')  # Create a label with empty text
    l1.place(x=800, y=0)
    b1 = Button(win, text="Roll the Dice!", foreground='blue', command=lambda: roll(l1))
    b1.place(x=800, y=0)
#--------------------------------------------------------------------------------------

   
    
   
    
    while True:


    while win.checkMouse() is None:

        x = win.winfo_pointerx()
        y = win.winfo_pointery()
        abs_coord_x = x - win.winfo_rootx()
        abs_coord_y = y - win.winfo_rooty()

        #print(f"x: {circle.getCenter().x - abs_coord_x}, y: {circle.getCenter().y - abs_coord_y}")
        new_point: Point = board.bg.nearest_vertex(Point(abs_coord_x, abs_coord_y))

        circle.move(new_point.x - circle.getCenter().x,new_point.y - circle.getCenter().y) 
   

        
        new_point: Point = board.bg.nearest_vertex(Point(abs_coord_x, abs_coord_y))

        circle.move(new_point.x - circle.getCenter().x, new_point.y - circle.getCenter().y)

    win.close()



if __name__ == "__main__":
    main()
