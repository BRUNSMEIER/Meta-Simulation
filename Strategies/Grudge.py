def strategy(history, memory):
    if history.shape[1] < 5:
        return 1, None  # Initially cooperate for the first five moves

    if history.shape[1] == 5:
        memory = 0  # Initialize memory after the initial phase

    if 0 in history[1]:
        memory = 1  # Defect if opponent ever defected
    if memory == 1:
        return 0,None

    return 1, None  # Otherwise, keep cooperating