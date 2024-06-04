def strategy(history, memory):
    # 试图在前几轮建立信任
    if history.shape[1] < 5:
        return 1, None  # 前5轮一直合作

    # 分析对手的行为，寻找合适的背叛时机
    if history[1, -1] == 1 and history[1, -2] == 1:  # 如果对手连续两轮合作
        # 选择一个时机背叛，以获得额外利益
        return 0, None
    else:
        # 在其他时间尽可能合作，以维护信任
        return 1, None
