
#once betrayed betray forever
def strategy(history, memory):
    betrayed = False
    if memory is not None and memory: # Has memory that it was already fooled.
        betrayed = True
    else: # Has not been defected yet, historically.
        if history.shape[1] >= 1 and history[1,-1] == 0: # fool me once recorded
            betrayed = True
    
    if betrayed:
        return 0, True
    else:
        return 1, False
    