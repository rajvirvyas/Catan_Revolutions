from enum import Enum

from board import Board
from graphics import *


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


def main():
    win = GraphWin("My Circle", 1000, 700)
    scale: float = 50.0
    center: Point = Point(500, 350)
    board: Board = Board(scale, center)
    board.draw_board(win)
    circle: Circle = Circle(Point(0.0, 0.0), 20.0)
    circle.setFill("Red")
    circle.draw(win)
    objects = []

    action: Action = Action.BUILD_SETTLEMENT

    while True:
        match action:
            case Action.BUILD_SETTLEMENT:
                x = win.winfo_pointerx()
                y = win.winfo_pointery()
                abs_coord_x = x - win.winfo_rootx()
                abs_coord_y = y - win.winfo_rooty()
                new_point: Point = board.bg.nearest_vertex(Point(abs_coord_x, abs_coord_y))
                if win.checkMouse() is not None:
                    settlement: circle = Circle(new_point, 20.0)
                    settlement.setFill("Red")
                    settlement.draw(win)
                    objects.append(settlement)

        circle.move(new_point.x - circle.getCenter().x, new_point.y - circle.getCenter().y)
    win.close()


if __name__ == "__main__":
    main()
