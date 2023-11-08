
from tkinter import *
import random
 
def roll(label):
    dice=['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']
    result= (f'{random.choice(dice)}{random.choice(dice)}')
    label.config(text=result)
    
 
