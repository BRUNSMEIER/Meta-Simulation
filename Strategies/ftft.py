
# Choose to defect if and only if the opponent just defected twice consequently in a row.
def strategy(history, memory):
    choice = 1
    if history.shape[1] >= 2 and history[1,-1] == 0 and history[1,-2] == 0:
        choice = 0
    return choice, None