def strategy(history, memory):
    # 如果是第一轮，选择合作，并初始化记忆存储对手的行为
    if history.shape[1] == 0:
        return 1, {"opponent_moves": []}

    # 更新记忆中的对手行为历史
    memory["opponent_moves"].append(history[1, -1])

    # 分析对手的行为模式
    if len(memory["opponent_moves"]) > 3 and memory["opponent_moves"][-1] == memory["opponent_moves"][-2] == memory["opponent_moves"][-3]:
        # 如果对手连续三次采取相同行为，则预测对手将继续这种行为
        predicted_next_move = memory["opponent_moves"][-1]
    else:
        predicted_next_move = 1  # 缺乏明确模式时，默认预测对手将合作

    # 基于预测的对手下一步行为作出决定
    choice = 0 if predicted_next_move == 0 else 1
    return choice, memory