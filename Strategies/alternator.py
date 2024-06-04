def strategy(history, memory):
    if history.shape[1] == 0:  # We're on the first turn!
        return 1, None  # Cooperate on the first move.
    else:
        last_choice = history[0, -1]
        return 1 - last_choice, None  # Alternate the choice.
