from board import Board
from graphics import *


def main():
    win = GraphWin("My Circle", 1000, 700)
    scale: float = 50.0
    center: Point = Point(500, 350)
    board: Board = Board(scale, center)
    board.draw_board(win)
    circle: Circle = Circle(Point(0.0, 0.0), 20.0)
    circle.setFill("Red")
    circle.draw(win)


    while win.checkMouse() is None:
        x = win.winfo_pointerx()
        y = win.winfo_pointery()
        abs_coord_x = x - win.winfo_rootx()
        abs_coord_y = y - win.winfo_rooty()
        print(f"x: {circle.getCenter().x - abs_coord_x}, y: {circle.getCenter().y - abs_coord_y}")
        new_point: Point = board.bg.nearest_vertex(Point(abs_coord_x, abs_coord_y))

        circle.move(new_point.x - circle.getCenter().x,new_point.y - circle.getCenter().y)
    win.close()


if __name__ == "__main__":
    main()
