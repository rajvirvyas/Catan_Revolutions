import math
import tkinter
from enum import Enum
import random
from typing import List

from board import Board, BoardGraph, Edge
from board_elements import Road, TileType
from graphics import *
from tkinter import *
from player import Player
from trade import *
import pygame

player1: Player = Player("Red", 1)  # Does not accurately connect chosen color to player
player2: Player = Player("Blue", 2)  # does not connect chosen color to player
bank: Player = Player("Yellow", 0)

current_player = 1  # Default to player 1's turn
roll_result = tk.IntVar()
scale = 50.0


def distance_between_points(p1: Point, p2: Point) -> float:
    return math.sqrt(math.fabs((p1.x - p2.x) ** 2) + math.fabs((p1.y - p2.y) ** 2))


def play():
    pygame.mixer.init()
    pygame.mixer.music.load("music.wav")
    pygame.mixer.music.play(loops=0)


def stop_sound():
    pygame.mixer.music.stop()


# --------------------------------------------------------------------------------------
def start_menu():
    start_win = Tk()
    start_win.title("Catan Start Menu")
    start_win.geometry("1100x700")
    start_win.config(bg="skyblue")

    # Define start button command
    def start_game():
        stop_sound()
        start_win.destroy()
        # start_turn(p1, p2)
        main()

    text_label = Label(start_win, text="CATAN REVOLUTIONS", font=("Impact", 80), bg="skyblue", fg="firebrick")
    # text_label.setStyle('bold')
    text_label.pack(pady=20)

    sword = Label(start_win, font=("Helvetica", 150), fg="black", bg="skyblue",
                  text='')  # Create a label with empty text
    sword.place(x=500, y=350)
    img = '\u2694'
    sword.config(text=img)

    queen = Label(start_win, font=("Helvetica", 150), fg="firebrick", bg="skyblue",
                  text='')  # Create a label with empty text
    queen.place(x=700, y=350)
    img2 = '\u265B'
    queen.config(text=img2)

    king = Label(start_win, font=("Helvetica", 150), fg="firebrick", bg="skyblue",
                 text='')  # Create a label with empty text
    king.place(x=300, y=350)
    img3 = '\u265A'
    king.config(text=img3)

    text_label = Label(start_win, text="Strategize. Influence. Rebel.", font=("Garamond", 40), bg="skyblue", fg="black")
    text_label.pack(pady=20)

    # Play the sound when the script is executed
    play()
    # Create buttons for start menu
    start_button = Button(start_win, text="START", font=("Impact", 20), bg="skyblue", width=15, height=1,
                          command=start_game)
    quit_button = Button(start_win, text="QUIT", font=("Impact", 20), bg="skyblue", width=15, height=1,
                         command=start_win.quit)

    # Pack buttons into the window
    start_button.pack(pady=20)
    quit_button.pack(pady=20)

    start_win.mainloop()


# --------------------------------------------------------------------------------------

ROAD_WIDTH: int = 10


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


def road_poly(e: Edge) -> Polygon:
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


def switch_turn():
    global current_player
    current_player = 3 - current_player  # Switch between player 1 and player 2 (e.g., 3 - 1 = 2, 3 - 2 = 1)


def update_chat_log(text_widget, message):
    if message is None:
        message = "Welcome to Catan Revolutions!\nPlayer 1 can roll dice to get started.\n"

    # Insert the message into the text widget
    text_widget.config(state='normal')
    text_widget.insert('end', message + '\n')

    text_widget.config(state='disabled')
    # Auto-scroll to the bottom
    text_widget.see('end')


def roll(label, text_widget) -> int:
    dice = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
    result = (f'{random.choice(dice)}{random.choice(dice)}')

    printPips = (
        result.replace('\u2680', '1').replace('\u2681', '2').replace('\u2682', '3').replace('\u2683', '4').replace(
            '\u2684', '5').replace('\u2685', '6'))

    sumPips = int(printPips[0]) + int(printPips[1])

    update_chat_log(text_widget, f"You rolled a {sumPips}\n")

    label.config(text=result)

    return sumPips


def tile_type_to_str(tp: TileType) -> str:
    match tp:
        case TileType.LUMBER:
            return "lumber"
        case TileType.ROCK:
            return "rock"
        case TileType.BRICK:
            return "brick"
        case TileType.WOOL:
            return "wool"
        case TileType.GRAIN:
            return "grain"
        case _:
            return "desert"


def give_resources(player: Player):
    print(roll_result.get())
    for s in player.settlements:
        for t in s.adj_tiles:
            if t.num == roll_result.get() and t.tile_type != TileType.DESERT and not t.has_bishop:
                tile_type = tile_type_to_str(t.tile_type)
                amount = 0
                if s.settlement.is_city:
                    if bank.resources_dict[tile_type] >= 2:
                        amount = 2
                    elif bank.resources_dict[tile_type] == 1:
                        amount = 1
                else:
                    if bank.resources_dict[tile_type] > 0:
                        amount = 1
                player.resources_dict[tile_type] += amount
                bank.resources_dict[tile_type] -= amount

    if player.player_id == player1.player_id:
        player = player2
    else:
        player = player1

    for s in player.settlements:
        for t in s.adj_tiles:
            if t.num == roll_result.get() and t.tile_type != TileType.DESERT and not t.has_bishop:
                tile_type = tile_type_to_str(t.tile_type)
                amount = 0
                if s.settlement.is_city:
                    if bank.resources_dict[tile_type] >= 2:
                        amount = 2
                    elif bank.resources_dict[tile_type] == 1:
                        amount = 1
                else:
                    if bank.resources_dict[tile_type] > 0:
                        amount = 1
                player.resources_dict[tile_type] += amount
                bank.resources_dict[tile_type] -= amount


def printTokens(text_widget):
    update_chat_log(text_widget,
                    "You have 5 influence tokens\nYou can...\n1.Force Trade\n2.Play Mercenary\n3.Curse Opponent\n")


def printTrade(text_widget):
    update_chat_log(text_widget,
                    "Which resource do you want to trade? Enter as 'give,get'\nBrick\nGrain\nLumber\nWool\nRock\n")


def printResources(text_widget):
    global current_player
    message = ""
    if current_player == 1:
        for i in player1.resources_dict:
            message += f"You have {player1.resources_dict.get(i)} {i}\n"
    else:
        for i in player2.resources_dict:
            message += f"You have {player2.resources_dict.get(i)} {i}\n"
    update_chat_log(text_widget, message)


def printAIAssist(text_widget):
    update_chat_log(text_widget, "Beep boop\n")


def printBuild(text_widget):
    update_chat_log(text_widget, "Building time!\n")


def printEnd(text_widget):
    switch_turn()
    update_chat_log(text_widget, f"End Turn\nIt's now Player {current_player}'s turn.\n")
    # update_chat_log(text_widget, "Turn ended\n")


def build_settlement(player: Player, win: GraphWin, board: Board, objects, initial_settlements: bool, text_widget):
    if not initial_settlements and (player.resources_dict["wood"] < 1 or player.resources_dict["brick"] < 1 or player.resources_dict["wool"] < 1
            or player.resources_dict["grain"] < 1):
        update_chat_log(text_widget, "You do not have enough resources to build a settlement.")
        return
    placement_circle: Circle = Circle(Point(0.0, 0.0), 20.0)
    placement_circle.setFill("Purple")
    placement_circle.draw(win)

    while not win.isClosed():
        x = win.winfo_pointerx()
        y = win.winfo_pointery()
        abs_coord_x = x - win.winfo_rootx()
        abs_coord_y = y - win.winfo_rooty()
        mouse_point = Point(abs_coord_x, abs_coord_y)
        new_point: Point = board.bg.nearest_vertex_point(mouse_point)
        placement_circle.move(new_point.x - placement_circle.getCenter().x,
                              new_point.y - placement_circle.getCenter().y)
        if (win.checkMouse() is not None and board.bg.build_settlement(new_point, player, initial_settlements) and
                distance_between_points(new_point, mouse_point) < scale):
            placement_circle.setFill(player.color)
            objects.append(placement_circle)
            return


def build_road(player: Player, win: GraphWin, board: Board, objects):
    placement_poly: Polygon = road_poly(board.bg.edges[0])
    placement_poly.setFill("Purple")
    new_point = Point(win.winfo_pointerx() - win.winfo_rootx(), win.winfo_pointery() - win.winfo_rooty())

    while not win.isClosed():
        x = win.winfo_pointerx()
        y = win.winfo_pointery()
        abs_coord_x = x - win.winfo_rootx()
        abs_coord_y = y - win.winfo_rooty()
        mouse_point = Point(abs_coord_x, abs_coord_y)
        e = board.bg.nearest_edge(mouse_point)
        if distance_between_points(mouse_point, new_point) < scale:
            old_point = new_point
            new_point: Point = e.center
            if old_point != new_point:
                placement_poly.undraw()
                placement_poly = road_poly(e)
                placement_poly.setFill("Purple")
                placement_poly.draw(win)

        if (win.checkMouse() is not None and board.bg.build_road(new_point, placement_poly, player.player_id)
                and distance_between_points(mouse_point, new_point) < scale):
            placement_poly.setFill(player.color)
            objects.append(placement_poly)
            return


def game_setup(win: GraphWin, chat_text: Text, board: Board, objects, b1: Button):
    message = "Welcome to Catan Revolutions!\nPlayer 1 can roll the dice to get started.\n"
    update_chat_log(chat_text, message)
    b1.wait_variable(roll_result)
    message = "Player 2 can roll the dice.\n"
    update_chat_log(chat_text, message)
    b1.wait_variable(roll_result)

    for i in range(2):
        update_chat_log(chat_text, "Player 1, place a starting settlement and road.")
        build_settlement(player1, win, board, objects, True, chat_text)
        build_road(player1, win, board, objects)
        update_chat_log(chat_text, "Player 2, place a starting settlement and road.")
        build_settlement(player2, win, board, objects, True, chat_text)
        build_road(player2, win, board, objects)

    message = "We will now roll for starting resources.\nPlayer 1 please roll the dice.\n"
    update_chat_log(chat_text, message)
    b1.wait_variable(roll_result)
    while roll_result.get() == 7:
        message = "Please roll again."
        update_chat_log(chat_text, message)
        b1.wait_variable(roll_result)
    give_resources(player1)
    first_roll = roll_result.get()
    message = "Player 2 please roll the dice.\n"
    update_chat_log(chat_text, message)
    b1.wait_variable(roll_result)
    while roll_result.get() == 7 and roll_result.get() != first_roll:
        message = "Please roll again."
        update_chat_log(chat_text, message)
        b1.wait_variable(roll_result)
    give_resources(player2)


def main():
    win = GraphWin("Catan Board", 1100, 700)
    win.config(bg="skyblue")
    center: Point = Point(500, 350)
    board: Board = Board(scale, center)
    board.draw_board(win)

    placement_circle: Circle = Circle(Point(0.0, 0.0), 20.0)
    placement_circle.setFill("Red")
    placement_circle_drawn: bool = False
    objects = []

    # initialize bank
    for key in bank.resources_dict.keys():
        bank.resources_dict[key] += 19

    action: Action = Action.BUILD_SETTLEMENT

    # Create a text box for chat log
    chat_text = Text(win, height=20, width=40, wrap='word', bg='white', fg='black')
    chat_text.place(x=800, y=0)

    bank_text = Text(win, height=5, width=40, wrap='word', bg='gold', fg='black')
    bank_text.place(x=800, y=325)

    victory_text = Text(win, height=4, width=40, wrap='word', bg='springgreen2', fg='black', font=('Impact',))
    victory_text.place(x=800, y=400)

    box = Label(win, font=("Helvetica", 55), text='', bg='black')  # Create a label with empty text
    box.place(x=945, y=402)

    user_entry = Entry(win, width=30, bg="white", fg="black")
    user_entry.place(x=800, y=275)

    # Add a scrollbar for the chat log
    scrollbar = Scrollbar(win, command=chat_text.yview)
    scrollbar.place(x=1085, y=0, height=265)
    chat_text.config(yscrollcommand=scrollbar.set)

    update_chat_log(chat_text, message=None)
    update_chat_log(bank_text, message=f'Treasury holds\n {bank.resources_dict}\n')
    update_chat_log(chat_text, f'P1 is {player1.color}\n')
    update_chat_log(chat_text, f'P2 is {player2.color}\n')
    update_chat_log(victory_text, "Points\n")
    update_chat_log(victory_text, message=f"P1: {player1.score}".ljust(30) + f"P2: {player2.score}".rjust(50)
                    )
    # update_chat_log(chat_text, f'BANK is {bank.color}\n')

    # Trading------------------------------------------------------------------------------
    # Initialize Players with values
    # for key in player2.resources_dict.keys():
    #     player2.resources_dict[key] += 10
    # for key in player1.resources_dict.keys():
    #     player1.resources_dict[key] += 8

    # --------------------------------------------------------------------------------------

    # For Dice-----------------------------------------------------------------------------

    l1 = Label(win, font=("Helvetica", 150), fg="firebrick", bg="skyblue", text='')  # Create a label with empty text
    l1.place(x=20, y=0)
    b1 = Button(win, text="Roll the Dice!", foreground='blue', background="skyblue",
                command=lambda: roll_result.set(roll(l1, chat_text)))
    b1.place(x=20, y=0)
    # ---------------------------------------------------------------------------------------
    # left buttons-----
    l2 = Label(win, font=("Helvetica", 150), bg="skyblue", text='')  # Create a label with empty text
    l2.place(x=20, y=500)
    b2 = Button(win, text="Infleunce Tokens", foreground='blue', bg="skyblue", command=lambda: printTokens(chat_text))
    b2.place(x=20, y=500)

    l3 = Label(win, font=("Helvetica", 150), bg="skyblue", text='')  # Create a label with empty text
    l3.place(x=20, y=550)
    b3 = Button(win, text="Resource Cards", foreground='blue', bg="skyblue", command=lambda: printResources(chat_text))
    b3.place(x=20, y=550)

    l4 = Label(win, font=("Helvetica", 150), bg="skyblue", text='')  # Create a label with empty text
    l4.place(x=20, y=600)
    l4 = Button(win, text="Trade", foreground='blue', bg="skyblue", command=lambda: printTrade(chat_text))
    l4.place(x=20, y=600)

    l7 = Label(win, font=("Helvetica", 150), bg="skyblue", text='')  # Create a label with empty text
    l7.place(x=20, y=650)
    l7 = Button(win, text="Build", foreground='blue', bg="skyblue", command=lambda: printBuild(chat_text))
    l7.place(x=20, y=650)

    # right buttons----

    l5 = Label(win, font=("Helvetica", 150), bg="skyblue", text='')  # Create a label with empty text
    l5.place(x=1010, y=500)
    l5 = Button(win, text="End Turn", foreground='blue', bg="skyblue", command=lambda: printEnd(chat_text))
    l5.place(x=1010, y=500)

    l6 = Label(win, font=("Helvetica", 150), bg="skyblue", text='')  # Create a label with empty text
    l6.place(x=1010, y=550)
    l6 = Button(win, text="AI Assist", foreground='blue', bg="skyblue", command=lambda: printAIAssist(chat_text))
    l6.place(x=1010, y=550)

    def send_message():
        user_input = user_entry.get()
        if user_input == '1':
            update_chat_log(chat_text,
                            "Gunship Diplomacy\nWhich two cards would you like to trade (enter with commas)\nA)Brick\nB)Grain\nC)Lumber\nD)Wool\nE)Rock\n")
        elif user_input == '2':
            # stolen=steal(player2,player1)
            stolen = steal(player2, player1) if current_player == 1 else steal(player1, player2)
            update_chat_log(chat_text, f"Hired Muscle\nRobber Ran\n{stolen}\n")
        elif user_input == '3':
            update_chat_log(chat_text, "Poor Harvest\nPlayer 2 will get half resources next roll\n")

        # Forced Trades------------------------------------------------------------------------------------
        elif user_input.lower() == "a,a":
            given1 = "brick"
            given2 = "brick"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 2 {given1}\nReceived {gotten}\n")
        elif user_input.lower() == 'a,b' or user_input.lower() == 'b,a':
            given1 = "brick"
            given2 = "grain"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower() == 'a,c' or user_input.lower() == 'c,a':
            given1 = "brick"
            given2 = "lumber"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower() == 'a,d' or user_input.lower() == 'd,a':
            given1 = "brick"
            given2 = "wool"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower() == 'a,e' or user_input.lower() == 'e,a':
            given1 = "brick"
            given2 = "rock"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower() == 'b,b':
            given1 = "grain"
            given2 = "grain"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 2 {given1}\nReceived {gotten}\n")
        elif user_input.lower() == 'b,c' or user_input.lower() == 'c,b':
            given1 = "grain"
            given2 = "lumber"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower() == 'b,d' or user_input.lower() == 'd,b':
            given1 = "grain"
            given2 = "wool"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower() == 'b,e' or user_input.lower() == 'e,b':
            given1 = "grain"
            given2 = "rock"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower() == 'c,c':
            given1 = "lumber"
            given2 = "lumber"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 2 {given1}\nReceived {gotten}\n")
        elif user_input.lower() == 'c,d' or user_input.lower() == 'd,c':
            given1 = "lumber"
            given2 = "wool"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower() == 'c,e' or user_input.lower() == 'e,c':
            given1 = "lumber"
            given2 = "rock"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower() == 'd,d':
            given1 = "wool"
            given2 = "wool"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 2 {given1}\nReceived {gotten}\n")
        elif user_input.lower() == 'd,e' or user_input.lower() == 'e,d':
            given1 = "wool"
            given2 = "rock"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower() == 'e,e':
            given1 = "rock"
            given2 = "rock"
            gotten = forced_trade(player2, player1, given1, given2) if current_player == 1 else forced_trade(player1,
                                                                                                             player2,
                                                                                                             given1,
                                                                                                             given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        # ------------------------------------------------------------------------------------

        # ---Bank trading----------------------------------------------------------------------
        elif user_input.lower() == "brick,grain":
            gotten = trade(player1, bank, "brick", "grain") if current_player == 1 else trade(player2, bank, "brick",
                                                                                              "grain")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 brick\nReceived 1 grain\n")
        elif user_input.lower() == "brick,lumber":
            gotten = trade(player1, bank, "brick", "lumber") if current_player == 1 else trade(player2, bank, "brick",
                                                                                               "lumber")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 brick\nReceived 1 lumber\n")
        elif user_input.lower() == "brick,wool":
            gotten = trade(player1, bank, "brick", "wool") if current_player == 1 else trade(player2, bank, "brick",
                                                                                             "wool")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 brick\nReceived 1 wool\n")
        elif user_input.lower() == "brick,rock":
            gotten = trade(player1, bank, "brick", "rock") if current_player == 1 else trade(player2, bank, "brick",
                                                                                             "rock")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 brick\nReceived 1 rock\n")
        elif user_input.lower() == "grain,brick":
            gotten = trade(player1, bank, "grain", "brick") if current_player == 1 else trade(player2, bank, "grain",
                                                                                              "brick")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 grain\nReceived 1 brick\n")
        elif user_input.lower() == "grain,lumber":
            gotten = trade(player1, bank, "grain", "lumber") if current_player == 1 else trade(player2, bank, "grain",
                                                                                               "lumber")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 grain\nReceived 1 lumber\n")
        elif user_input.lower() == "grain,wool":
            gotten = trade(player1, bank, "grain", "wool") if current_player == 1 else trade(player2, bank, "grain",
                                                                                             "wool")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 grain\nReceived 1 wool\n")
        elif user_input.lower() == "grain,rock":
            gotten = trade(player1, bank, "grain", "rock") if current_player == 1 else trade(player2, bank, "grain",
                                                                                             "rock")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 grain\nReceived 1 rock\n")
        elif user_input.lower() == "lumber,brick":
            gotten = trade(player1, bank, "lumber", "brick") if current_player == 1 else trade(player2, bank, "lumber",
                                                                                               "brick")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 lumber\nReceived 1 brick\n")
        elif user_input.lower() == "lumber,grain":
            gotten = trade(player1, bank, "lumber", "grain") if current_player == 1 else trade(player2, bank, "lumber",
                                                                                               "grain")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 lumber\nReceived 1 grain\n")
        elif user_input.lower() == "lumber,wool":
            gotten = trade(player1, bank, "lumber", "wool") if current_player == 1 else trade(player2, bank, "lumber",
                                                                                              "wool")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 lumber\nReceived 1 wool\n")
        elif user_input.lower() == "lumber,rock":
            gotten = trade(player1, bank, "lumber", "rock") if current_player == 1 else trade(player2, bank, "lumber",
                                                                                              "rock")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 lumber\nReceived 1 rock\n")
        elif user_input.lower() == "wool,brick":
            gotten = trade(player1, bank, "wool", "brick") if current_player == 1 else trade(player2, bank, "wool",
                                                                                             "brick")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 wool\nReceived 1 brick\n")
        elif user_input.lower() == "wool,grain":
            gotten = trade(player1, bank, "wool", "grain") if current_player == 1 else trade(player2, bank, "wool",
                                                                                             "grain")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 wool\nReceived 1 grain\n")
        elif user_input.lower() == "wool,lumber":
            gotten = trade(player1, bank, "wool", "lumber") if current_player == 1 else trade(player2, bank, "wool",
                                                                                              "lumber")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 wool\nReceived 1 lumber\n")
        elif user_input.lower() == "wool,rock":
            gotten = trade(player1, bank, "wool", "rock") if current_player == 1 else trade(player2, bank, "wool",
                                                                                            "rock")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 wool\nReceived 1 rock\n")
        elif user_input.lower() == "rock,brick":
            gotten = trade(player1, bank, "rock", "brick") if current_player == 1 else trade(player2, bank, "rock",
                                                                                             "brick")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 rock\nReceived 1 brick\n")
        elif user_input.lower() == "rock,grain":
            gotten = trade(player1, bank, "rock", "grain") if current_player == 1 else trade(player2, bank, "rock",
                                                                                             "grain")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 rock\nReceived 1 grain\n")
        elif user_input.lower() == "rock,lumber":
            gotten = trade(player1, bank, "rock", "lumber") if current_player == 1 else trade(player2, bank, "rock",
                                                                                              "lumber")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 rock\nReceived 1 lumber\n")
        elif user_input.lower() == "rock,wool":
            gotten = trade(player1, bank, "rock", "wool") if current_player == 1 else trade(player2, bank, "rock",
                                                                                            "wool")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 rock\nReceived 1 wool\n")
        # ---------------------------------------------------------------------------------------

        else:
            update_chat_log(chat_text, user_input)
        user_entry.delete(0, 'end')  # Clear the user entry field

    send_button = Button(win, text="Enter", bg="skyblue", command=send_message)
    send_button.place(x=1030, y=275)

    player: Player = player1
    game_setup(win, chat_text, board, objects, b1)
    start_menu()
    while not win.isClosed():
        match current_player:
            case player1.player_id:
                player = player1
            case _:
                player = player2

        match action:
            case Action.NOTHING:
                pass
            case Action.BUILD_SETTLEMENT:
                if not placement_circle_drawn:
                    placement_circle.draw(win)
                    placement_circle_drawn = True
                build_settlement(player, win, board, objects, chat_text)
                action = Action.NOTHING

            case _:
                placement_circle.undraw()
                placement_circle_drawn = False

    win.mainloop()


if __name__ == "__main__":
    start_menu()
    # main()
