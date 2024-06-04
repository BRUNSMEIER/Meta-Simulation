def strategy(history, memory):
    if history.shape[1] == 0:
        return 1, None  # Initially cooperate

    # Check the last two moves of the opponent
    if history.shape[1] >= 2 and history[1, -1] == 0 and history[1, -2] == 0:
        # If opponent defected in the last two consecutive moves, then defect
        return 0, None

    return 1, None  # Otherwise, keep cooperating
