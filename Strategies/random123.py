import random

def strategy(history, memory):
    # 80% chance to cooperate, 20% to defect
    choice = 1 if random.random() < 0.8 else 0
    return choice, None