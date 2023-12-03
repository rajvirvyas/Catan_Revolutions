import math
from enum import Enum
import random
from board import Board, BoardGraph, Edge
from graphics import *
from tkinter import *
from player import Player
from trade import *

player1: Player = Player("Red", 1) # Does not accurately connect chosen color to player
player2: Player = Player("Blue", 2) # does not connect chosen color to player
bank: Player = Player("Yellow", 0)

#--------------------------------------------------------------------------------------
def start_menu():
        start_win = Tk()
        start_win.title("Catan Start Menu")
        start_win.geometry("1100x700")
        
        
        # Define start button command
        def start_game():
            start_win.destroy()
            # start_turn(p1, p2)
            main()

        text_label = Label(start_win, text="Catan Revolutions", font=("Arial", 24), fg="red")
        text_label.pack(pady=20)

        text_label = Label(start_win, text="Strategize. Influence. Rebel.", font=("Arial", 18))
        text_label.pack(pady=20)
        # Player selection
        color_var = StringVar()
        color_var.set("Red")  # Default selection
         # Get player selection
        player_color = color_var.get()
        if player_color == "Red":
                    player1 = Player("Red", 1)
                    player2 = Player("Blue", 2)
        else:
                    player1 = Player(1, "Blue")
                    player2 = Player(2, "Red")
        red_button = Radiobutton(start_win, text="Red", variable=color_var, value="Red")
        blue_button = Radiobutton(start_win, text="Blue", variable=color_var, value="Blue")
        red_button.pack(pady=10)
        blue_button.pack(pady=10)

        # Create buttons for start menu
        start_button = Button(start_win, text="Start Game", command=start_game)
        exit_button = Button(start_win, text="Exit", command=start_win.quit)

        # Pack buttons into the window
        start_button.pack(pady=20)
        exit_button.pack(pady=20)

        start_win.mainloop()
#--------------------------------------------------------------------------------------

ROAD_WIDTH: int = 10

win = GraphWin("Catan Board", 1100, 700)


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

def update_chat_log(text_widget, message):
    
    if message is None:
        message="Welcome to Catan Revolutions!\nPlayer 1 can roll dice to get started.\n"
    
    # Insert the message into the text widget
    text_widget.config(state='normal')
    text_widget.insert('end', message + '\n')
    
    text_widget.config(state='disabled')
    # Auto-scroll to the bottom
    text_widget.see('end')

def roll(label, text_widget):
    dice=['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']
    result= (f'{random.choice(dice)}{random.choice(dice)}')

    printPips = (result.replace('\u2680', '1').replace('\u2681', '2').replace('\u2682', '3').replace('\u2683', '4').replace('\u2684', '5').replace('\u2685', '6'))

    sumPips= int(printPips[0]) + int(printPips[1])
    
    update_chat_log(text_widget, f"You rolled a {sumPips}\n")
                    
    label.config(text=result)


def printTokens(text_widget):
      update_chat_log(text_widget, "You have 5 influence tokens\nYou can...\n1.Force Trade\n2.Play Mercenary\n3.Curse Opponent\n")

def printTrade(text_widget):
      
      update_chat_log(text_widget, "Which resource do you want to trade? Enter as 'give,get'\nBrick\nGrain\nLumber\nWool\nRock\n")

def printResources(text_widget):
    message = ""
    for i in player1.resources_dict:
        message += f"You have {player1.resources_dict.get(i)} {i}\n"
    update_chat_log(text_widget, message)

def printAIAssist(text_widget):
      update_chat_log(text_widget, "Beep boop\n")

def printEnd(text_widget):
      update_chat_log(text_widget, "Turn ended\n")

 

def main():
    scale: float = 50.0
    center: Point = Point(500, 350)
    board: Board = Board(scale, center)
    board.draw_board(win)

    placement_circle: Circle = Circle(Point(0.0, 0.0), 20.0)
    placement_circle.setFill("Red")
    placement_circle_drawn: bool = False
    objects = []

   
    


    #initialize bank
    for key in bank.resources_dict.keys():
        bank.resources_dict[key] +=19
    

    action: Action = Action.BUILD_SETTLEMENT
    
    # Create a text box for chat log
    chat_text = Text(win, height=20, width=40, wrap='word', fg='white')
    chat_text.place(x=800, y=0)

    bank_text = Text(win, height=5, width=40, wrap='word', bg='yellow', fg='black')
    bank_text.place(x=800, y=325)

    victory_text= Text(win, height=5, width=40, wrap='word', bg='black', fg='green',font='Helvetica 12 bold italic')
    victory_text.place(x=800, y=400)
   

    box= Label(win, font=("Helvetica", 55), text='', bg='green')  # Create a label with empty text
    box.place(x=945, y=402)
    
    
    user_entry=Entry(win,width=30, bg="white", fg="black")
    user_entry.place(x=800, y=275)
    
        # Add a scrollbar for the chat log
    scrollbar = Scrollbar(win, command=chat_text.yview)
    scrollbar.place(x=1085, y=0, height=265)
    chat_text.config(yscrollcommand=scrollbar.set)

    update_chat_log(chat_text,message=None)
    update_chat_log(bank_text, message=f'Treasury holds\n {bank.resources_dict}\n')
    update_chat_log(chat_text, f'P1 is {player1.color}\n')
    update_chat_log(chat_text, f'P2 is {player2.color}\n')
    update_chat_log(victory_text, "Points\n")
    update_chat_log(victory_text, message = f"P1: {player1.score}".ljust(30) + f"P2: {player2.score}".rjust(35)
)
    #update_chat_log(chat_text, f'BANK is {bank.color}\n')

# Trading------------------------------------------------------------------------------
   #Initialize Players with values
    for key in player2.resources_dict.keys():
         player2.resources_dict[key] += 10
    for key in player1.resources_dict.keys():
         player1.resources_dict[key] += 8       

#--------------------------------------------------------------------------------------

# For Dice-----------------------------------------------------------------------------

    l1 = Label(win, font=("Helvetica", 150), text='')  # Create a label with empty text
    l1.place(x=20, y=0)
    b1 = Button(win, text="Roll the Dice!", foreground='blue', command=lambda: [roll(l1, chat_text)])
    b1.place(x=20, y=0)
#--------------------------------------------------------------------------------------
    l2 = Label(win, font=("Helvetica", 150), text='')  # Create a label with empty text
    l2.place(x=20, y=500)
    b2 = Button(win, text="Infleunce Tokens", foreground='blue', command= lambda: printTokens(chat_text))
    b2.place(x=20, y=500)

    l3 = Label(win, font=("Helvetica", 150), text='')  # Create a label with empty text
    l3.place(x=20, y=550)
    b3 = Button(win, text="Resource Cards", foreground='blue', command= lambda: printResources(chat_text))
    b3.place(x=20, y=550)

    l4 = Label(win, font=("Helvetica", 150), text='')  # Create a label with empty text
    l4.place(x=20, y=600)
    l4 = Button(win, text="Trade", foreground='blue', command= lambda: printTrade(chat_text))
    l4.place(x=20, y=600)

    l5 = Label(win, font=("Helvetica", 150), text='')  # Create a label with empty text
    l5.place(x=1010, y=500)
    l5 = Button(win, text="End Turn", foreground='blue', command= lambda: printEnd(chat_text))
    l5.place(x=1010, y=500)

    l6 = Label(win, font=("Helvetica", 150), text='')  # Create a label with empty text
    l6.place(x=1010, y=550)
    l6 = Button(win, text="AI Assist", foreground='blue', command= lambda: printAIAssist(chat_text))
    l6.place(x=1010, y=550)




    

    def send_message():
        user_input = user_entry.get()
        if  user_input=='1':
            update_chat_log(chat_text,"Gunship Diplomacy\nWhich two cards would you like to trade (enter with commas)\nA)Brick\nB)Grain\nC)Lumber\nD)Wool\nE)Rock\n")
        elif user_input=='2':
            stolen=steal(player2,player1)
            update_chat_log(chat_text,f"Hired Muscle\nRobber Ran\n{stolen}\n")
        elif user_input=='3':
            update_chat_log(chat_text,"Poor Harvest\nPlayer 2 will get half resources next roll\n")
       
       # Forced Trades------------------------------------------------------------------------------------
        elif user_input.lower()=="a,a":
            given1="brick"
            given2="brick"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 2 {given1}\nReceived {gotten}\n")
        elif user_input.lower()=='a,b' or user_input.lower()=='b,a':
            given1="brick"
            given2="grain"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower()=='a,c' or user_input.lower()=='c,a':
            given1="brick"
            given2="lumber"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower()=='a,d' or user_input.lower()=='d,a':
            given1="brick"
            given2="wool"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower()=='a,e' or user_input.lower()=='e,a':
            given1="brick"
            given2="rock"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower()=='b,b':
            given1="grain"
            given2="grain"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 2 {given1}\nReceived {gotten}\n")
        elif user_input.lower()=='b,c' or user_input.lower()=='c,b':
            given1="grain"
            given2="lumber"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower()=='b,d' or user_input.lower()=='d,b':
            given1="grain"
            given2="wool"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower()=='b,e' or user_input.lower()=='e,b':
            given1="grain"
            given2="rock"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower()=='c,c':
            given1="lumber"
            given2="lumber"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 2 {given1}\nReceived {gotten}\n")
        elif user_input.lower()=='c,d' or user_input.lower()=='d,c':
            given1="lumber"
            given2="wool"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower()=='c,e' or user_input.lower()=='e,c':
            given1="lumber"
            given2="rock"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower()=='d,d':
            given1="wool"
            given2="wool"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 2 {given1}\nReceived {gotten}\n")
        elif user_input.lower()=='d,e' or user_input.lower()=='e,d':
            given1="wool"
            given2="rock"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        elif user_input.lower()=='e,e':
            given1="rock"
            given2="rock"
            gotten=forced_trade(player2,player1,given1,given2)
            update_chat_log(chat_text, f"\nGave 1 {given1} and {given2}\nReceived {gotten}\n")
        # ------------------------------------------------------------------------------------

        #---Bank trading----------------------------------------------------------------------
        elif user_input.lower()=="brick,grain":
            gotten=trade(player1,player2,bank,"brick", "grain")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 brick\nReceived 1 grain\n")
        elif user_input.lower()=="brick,lumber":
            gotten=trade(player1,player2,bank,"brick", "lumber")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 brick\nReceived 1 lumber\n")
        elif user_input.lower()=="brick,wool":
            gotten=trade(player1,player2,bank,"brick", "wool")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 brick\nReceived 1 wool\n")
        elif user_input.lower()=="brick,rock":
            gotten=trade(player1,player2,bank,"brick", "rock")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 brick\nReceived 1 rock\n")
        elif user_input.lower()=="grain,brick":
            gotten=trade(player1,player2,bank,"grain", "brick")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 grain\nReceived 1 brick\n")
        elif user_input.lower()=="grain,lumber":
            gotten=trade(player1,player2,bank,"grain", "lumber")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 grain\nReceived 1 lumber\n")
        elif user_input.lower()=="grain,wool":
            gotten=trade(player1,player2,bank,"grain", "wool")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 grain\nReceived 1 wool\n")
        elif user_input.lower()=="grain,rock":
            gotten=trade(player1,player2,bank,"grain", "rock")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 grain\nReceived 1 rock\n")
        elif user_input.lower()=="lumber,brick":
            gotten=trade(player1,player2,bank,"lumber", "brick")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 lumber\nReceived 1 brick\n")
        elif user_input.lower()=="lumber,grain":
            gotten=trade(player1,player2,bank,"lumber", "grain")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 lumber\nReceived 1 grain\n")
        elif user_input.lower()=="lumber,wool":
            gotten=trade(player1,player2,bank,"lumber", "wool")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 lumber\nReceived 1 wool\n")
        elif user_input.lower()=="lumber,rock":
            gotten=trade(player1,player2,bank,"lumber", "rock")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 lumber\nReceived 1 rock\n")
        elif user_input.lower()=="wool,brick":
            gotten=trade(player1,player2,bank,"wool", "brick")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 wool\nReceived 1 brick\n")
        elif user_input.lower()=="wool,grain":
            gotten=trade(player1,player2,bank,"wool", "grain")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 wool\nReceived 1 grain\n")
        elif user_input.lower()=="wool,lumber":
            gotten=trade(player1,player2,bank,"wool", "lumber")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 wool\nReceived 1 lumber\n")
        elif user_input.lower()=="wool,rock":
            gotten=trade(player1,player2,bank,"wool", "rock")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 wool\nReceived 1 rock\n")
        elif user_input.lower()=="rock,brick":
            gotten=trade(player1,player2,bank,"rock", "brick")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 rock\nReceived 1 brick\n")
        elif user_input.lower()=="rock,grain":
            gotten=trade(player1,player2,bank,"rock", "grain")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 rock\nReceived 1 grain\n") 
        elif user_input.lower()=="rock,lumber":
            gotten=trade(player1,player2,bank,"rock", "lumber")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 rock\nReceived 1 lumber\n")
        elif user_input.lower()=="rock,wool":
            gotten=trade(player1,player2,bank,"rock", "wool")
            update_chat_log(bank_text, gotten)
            update_chat_log(chat_text, f"\nGave 4 rock\nReceived 1 wool\n")
        #---------------------------------------------------------------------------------------
        
        else:
            update_chat_log(chat_text,user_input)
        user_entry.delete(0, 'end')  # Clear the user entry field

    send_button = Button(win, text="Enter", command=send_message)
    send_button.place(x=1030, y=275)

    while True:
        match action:
            case Action.NOTHING:
                start_menu()
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

if __name__ == "__main__":
    start_menu()
    #main()

    