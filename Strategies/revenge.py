def strategy(history, memory):
    if history.shape[1] == 0:
        return 1, None  # Initially cooperate

    if memory is None:
        memory1 = {
            'cooperation_streak': 0,
            'defection_streak': 0
        }

    last_move = history[1, -1]

    if last_move == 1:
        memory1['cooperation_streak'] += 1
        memory1['defection_streak'] = 0

        if memory1['cooperation_streak'] % 3 == 0:
            return 1, memory  # Cooperate every three consecutive cooperations by the opponent
        else:
            return 1, memory
    else:
        if memory1['defection_streak'] < 5:
            memory1['defection_streak'] += 1
            return 0, memory  # Defect for five turns after an opponent defection
        else:
            return 1, memory  # Then go back to checking for cooperation streaks

