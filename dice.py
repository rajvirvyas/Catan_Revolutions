
from tkinter import *
import random
 
def roll(label):
    dice=['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']
    result= (f'{random.choice(dice)}{random.choice(dice)}')

    printPips = (result.replace('\u2680', '1').replace('\u2681', '2').replace('\u2682', '3').replace('\u2683', '4').replace('\u2684', '5').replace('\u2685', '6'))

    
    print("You Rolled a", int(printPips[0]) + int(printPips[1]))
    label.config(text=result)
    
 
