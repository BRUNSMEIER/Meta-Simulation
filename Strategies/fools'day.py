
def strategy(history, memory):
    choice = None
    if history.shape[1] == 0: #on the first turn!
        choice = 1
    else:
        choice = history[0,-1] # keep doing the same thing as last move!
        if history[1,-1] == 0: # If my opponent defected last turn, do the opposite thing as my last move:
            choice = 1-choice
            
    return choice, None