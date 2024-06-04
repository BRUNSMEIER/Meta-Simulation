def strategy(history, memory):
    if history.shape[1] == 0:
        return 1, None  # Initially cooperate

    defections = sum(history[1] == 0)
    total_moves = history.shape[1]

    if defections > total_moves / 2:
        # If opponent defected more than half the time, start defecting
        return 0, None

    return 1, None  # Otherwise, keep cooperating
