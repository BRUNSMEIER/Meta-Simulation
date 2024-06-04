import random
import numpy as np

# Strategy based on Nicky Case's "The Evolution of Trust"
# DETECTIVE Strategy Description:
# Start with a fixed sequence: Cooperate, Cheat, Cooperate, Cooperate.
# If the opponent cheats in response, switch to Tit for Tat strategy.
# If the opponent never cheats, switch to always defect to exploit the opponent.


def strategy(history, memory):
    testing_schedule = [1, 0, 1, 1]
    game_length = history.shape[1]
    shall_exploit = memory if memory is not None else False
    choice = None

    # Initial phase: follow the testing schedule
    if game_length < 4:
        return testing_schedule[game_length], shall_exploit

    # Decision phase: analyze opponent's actions after the initial phase
    if game_length == 4:
        opponents_actions = history[1, :4]
        shall_exploit = np.all(opponents_actions == 1)  # True if opponent always cooperated

    # Post-decision phase: choose strategy based on analysis
    if shall_exploit:
        choice = 0  # Always defect
    else:
        choice = history[1, -1]  # Tit for Tat

    return choice, shall_exploit