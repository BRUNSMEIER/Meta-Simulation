import os
import itertools
import importlib
import numpy as np
import random

# Constants
STRATEGY_FOLDER = "Strategies"
RESULTS_FILE = "results.txt"
POINTS_ARRAY = np.array([[1, 5], [0, 3]])
MOVE_LABELS = ["D", "C"]

def get_game_length():
    return int(200 - 40 * np.log(1 - random.random()))

def get_visible_history(history, player, turn):
    return history[:, :turn] if player == 0 else history[::-1, :turn]

def strategy_move(move):
    if type(move) is str:
        defects = ["defect", "tell truth"]
        return 0 if (move in defects) else 1
    else:
        # Coerce all moves to be 0 or 1 so strategies can safely assume 0/1's only
        return int(bool(move))

def simulate_round(moduleA, moduleB, length_of_game):
    history = np.zeros((2, length_of_game), dtype=int)
    memoryA, memoryB = None, None
    for turn in range(length_of_game):
        moveA, memoryA = moduleA.strategy(get_visible_history(history, 0, turn), memoryA)
        moveB, memoryB = moduleB.strategy(get_visible_history(history, 1, turn), memoryB)
        history[0, turn] = strategy_move(moveA)
        history[1, turn] = strategy_move(moveB)
    return history

def tallyRoundScores(history):
    scoreA = 0
    scoreB = 0
    ROUND_LENGTH = history.shape[1]
    for turn in range(ROUND_LENGTH):
        playerAmove = history[0, turn]
        playerBmove = history[1, turn]
        scoreA += POINTS_ARRAY[playerAmove][playerBmove]
        scoreB += POINTS_ARRAY[playerBmove][playerAmove]
    return scoreA / ROUND_LENGTH, scoreB / ROUND_LENGTH

def output_results(file, pair, history, scores):
    file.write(f"{pair[0]} (P1) VS. {pair[1]} (P2)\n")
    for player_history in history:
        file.write(" ".join(MOVE_LABELS[move] for move in player_history) + "\n")
    file.write(f"Final score for {pair[0]}: {scores[0]}\n")
    file.write(f"Final score for {pair[1]}: {scores[1]}\n\n")

def run_tournament():
    print("Starting tournament")
    strategy_files = [f[:-3] for f in os.listdir(STRATEGY_FOLDER) if f.endswith(".py")]
    score_keeper = dict.fromkeys(strategy_files, 0)

    with open(RESULTS_FILE, "w+") as result_file:
        for pair in itertools.combinations(strategy_files, 2):
            moduleA = importlib.import_module(STRATEGY_FOLDER + "." + pair[0])
            moduleB = importlib.import_module(STRATEGY_FOLDER + "." + pair[1])
            history = simulate_round(moduleA, moduleB, get_game_length())
            scores = tallyRoundScores(history)
            output_results(result_file, pair, history, scores)
            score_keeper[pair[0]] += scores[0]
            score_keeper[pair[1]] += scores[1]

        output_final_scores(result_file, score_keeper, strategy_files)
    print("Done with everything! Results file already written to " + RESULTS_FILE)

def output_final_scores(file, score_keeper, strategies):
    sorted_scores = sorted(((score, strat) for strat, score in score_keeper.items()), reverse=True)
    file.write("\nTOTAL SCORES\n")
    for rank, (score, strat) in enumerate(sorted_scores, 1):
        score_per = score / (len(strategies) - 1)
        file.write(f"#{rank}: {strat.ljust(15)} {score:.3f} ({score_per:.3f} average)\n")

if __name__ == "__main__":
    run_tournament()
