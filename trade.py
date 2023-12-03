from player import Player
import random

def trade(p1,p2,bank, take, give):
    p1.resources_dict[take] -=4
    bank.resources_dict[take] +=4
    bank.resources_dict[give] -=1
    p1.resources_dict[give] +=1 
    return (f'Tresury holds\n {bank.resources_dict}\n')

def forced_trade(fromPlayer, toPlayer, g1, g2):
        printMessage=""
        print("this is pre trade",fromPlayer.resources_dict.items())
        #------ update your and others inventory
        #----Check resources
        if not fromPlayer.resources_dict:
            printMessage= f"{fromPlayer} does not have any resources"
            return printMessage
        else:

            toPlayer.resources_dict[g1] -=1
            toPlayer.resources_dict[g2] -=1
            fromPlayer.resources_dict[g1] +=1
            fromPlayer.resources_dict[g2] +=1

        
        
        trade_key1, t1= random.choice(list(fromPlayer.resources_dict.items()))
        trade_key2, t2= random.choice(list(fromPlayer.resources_dict.items()))

        if t1 and t2 != "0":
            # Assign the value to the same key in player1
            if trade_key1 in toPlayer.resources_dict.keys():
                toPlayer.resources_dict[trade_key1] += 1
                fromPlayer.resources_dict[trade_key1] -=1
                printMessage= printMessage+ f"{1} {trade_key1}"

            if trade_key2 in toPlayer.resources_dict.keys():
                toPlayer.resources_dict[trade_key2] += 1
                fromPlayer.resources_dict[trade_key2] -=1
                printMessage= printMessage+ f" {1} {trade_key2}\n"
        else:
               print("Wrong!")

        print("this is post trade",fromPlayer.resources_dict.items())
        return printMessage

def steal(fromPlayer, toPlayer):
    trade_key, tval= random.choice(list(fromPlayer.resources_dict.items()))
    if tval > 0:
        # Assign the value to the same key in player1
        if trade_key in toPlayer.resources_dict:
            toPlayer.resources_dict[trade_key] += 1
            fromPlayer.resources_dict[trade_key] -= 1
            printMessage = f"Player {toPlayer.player_id} stole 1 {trade_key} from Player {fromPlayer.player_id}"
            
        else:
            printMessage = f"Player {fromPlayer.player_id} does not have the resource {trade_key}"
    else:
        printMessage = f"Player {fromPlayer.player_id} does not have any non-zero resources to steal"
        
    return printMessage
