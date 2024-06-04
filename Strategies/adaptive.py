def strategy(history, memory):
    if history.shape[1] == 0:
        return 1, None  # Initially cooperate

    defections = sum(history[1] == 0)
    total_moves = history.shape[1]

    # Calculate the percentage of the opponent's defections
    defection_rate = defections / total_moves

    # Set a threshold for defection rate that triggers a more aggressive response
    defection_threshold = 0.3  # 30% defections trigger retaliation

    if defection_rate > defection_threshold:
        # If the opponent's defection rate is higher than the threshold, defect more aggressively
        # Defect for a number of rounds based on how much the rate exceeds the threshold
        rounds_to_defect = int((defection_rate - defection_threshold) * 10)  # Scale up the response

        if memory is None:
            memory = rounds_to_defect
        else:
            memory = max(memory - 1, rounds_to_defect)

        if memory > 0:
            return 0, memory  # Continue defecting for 'memory' number of rounds

    return 1, None  # Otherwise, keep cooperating
