import os
import sys
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import torch
import torch.nn as nn
import torch.optim as optim
import pygame
import random
from PIL import Image, ImageSequence
import csv
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV

predicted_choices = []  # 模型预测的结果
actual_choices = []  # 玩家实际的选择
last_round_choice = 1
damage_flag = 0
# Initialize Pygame
def main():
    # pygame.init()
    damage_flag = 0
    width, height = 800, 600
    # Set up the display loading
    current_dir = os.path.dirname(__file__)

    raw_path = os.path.join(current_dir, "venv", "image", "Phoenix_Objection.webp")
    background_path = 'fonts/Screenshot-court.jpg'
    frame_index = 0
    frame_index1 = 0
    clock = pygame.time.Clock()
    frame_rate = 10
    ##about gif
    gif_frames = []
    gif_frames1 = []
    # 使用Pillow拆解GIF为帧


    ##Artificial Intelligence Part
    data = pd.read_csv('game_data.csv')
    # Convert text labels to numbers
    le = LabelEncoder()
    data['player_choice'], _ = pd.factorize(data['player_choice'])
    data['computer_choice'], _ = pd.factorize(data['computer_choice'])
    # Assuming `data` includes multiple rounds of gameplay
    data['last_round_choice'] = data['player_choice'].shift(
        1)  # Shift the player choices down to align with the next round
    data['player_char'], _ = pd.factorize(data['player_char'])
    data.fillna(0, inplace=True)  # Handle any NaN values that appear as a result of the shift
    # data['last_round_choice_interaction'] = data['last_round_choice'] * data['player_health']

    # # Update your features list
    X = data[['round_number', 'player_health', 'computer_health', 'last_round_choice', 'player_char']]

    # Defining characteristics and target variables
    # X = data[['round_number', 'player_health', 'computer_health']]
    y = data['player_choice']

    # Segmented data sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    class_weight = {
        0: 1,  # Weighting of other categories
        1: 1000,
        2: 1,# Weights for category 2
    }
    model = RandomForestClassifier(class_weight=class_weight,random_state=42)
    model.fit(X_train, y_train)
    # Parameter search and model training
    param_grid = {
        'n_estimators': [100, 200],  # Add more options for number of estimators
        'max_depth': [10, 20],  # Include unlimited depth and increase search depth
        'min_samples_split': [2, 5],  # Add an option to refine the search
        'min_samples_leaf': [4, 2],
        'max_features': [ 'sqrt', 'log2'],  # Add the maximum number of features parameter
        # 'bootstrap': [True, False]  # Whether or not to use bootstrap sampling
    }
    grid_search = GridSearchCV(model, param_grid, cv=3)  # Decrease the value of the cv parameter to reduce computation time
    grid_search.fit(X_train,y_train)

    # Predictions using optimal models
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    # Calculation accuracy and other indicators
    from sklearn.metrics import accuracy_score
    print("Accuracy:", accuracy_score(y_test, y_pred))

    # Decision Tree model
    # model = DecisionTreeClassifier()
    # model.fit(X_train, y_train)
    #
    # # test validation set
    # y_pred = model.predict(X_test)
    #
    # # evaluation
    # print("Accuracy:", accuracy_score(y_test, y_pred))


    gif_s = Image.open(raw_path)

    for frame in ImageSequence.Iterator(gif_s):
        frame = frame.convert('RGBA')  # 转换为RGBA格式以处理透明度
        pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
        gif_frames1.append(pygame_image)

    ##gifstuff

    # # pygame.display.set_caption("Attorney")
    # bg_pic = pygame.image.load(background_path)

    three_options = ['Evidence', 'Cross-examination', 'Bluff']
    initial_option = 0
    WIN_LIST_RPS = [('Evidence', 'Cross-examination'),  # who can be defeated by ROCK
                    ('Cross-examination', 'Bluff'),  # who can be defeated by SCISSORS
                    ('Bluff', 'Evidence')]  # who can be defeated by PAPER
    # Colors 石头 (Rock) - 举证 (Evidence): 剪刀 (Scissors) - 质询 (Cross-examination):布 (Paper) - 虚张声势 (Bluff):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    last_round_choice = 1
    # Game variables
    player_health = 100
    computer_health = 100
    player_score = 0
    computer_score = 0
    ties = 0
    rounds = 0
    last_round_choice = None

    class Character:
        def __init__(self, name, rock_star, paper_star, scissors_star):
            self.name = name
            self.rock_star = rock_star
            self.paper_star = paper_star
            self.scissors_star = scissors_star

    # 生成随机角色
    # def generate_characters(num_characters):
    #     characters = []
    #     for i in range(num_characters):
    #         name = f"角色{i+1}"
    #         rock_star = random.randint(1, 5)
    #         paper_star = random.randint(1, 5)
    #         scissors_star = random.randint(1, 5)
    #         character = Character(name, rock_star, paper_star, scissors_star)
    #         characters.append(character)
    #     return characters
    #
    # # 生成7个随机角色
    # characters = generate_characters(7)

    # 显示生成的角色信息
    # print("生成的随机角色:")
    # for character in characters:
    #     print(f"角色名称: {character.name}, 拳头星级: {character.rock_star}, 布星级: {character.paper_star}, 剪刀星级: {character.scissors_star}")
    # Main game loop

    characters = [
        Character("Ryuji", 3, 4, 2),
        Character("Shinada", 5, 3, 4),
        Character("Frantze", 7, 5, 5),  ## fake evidence
        Character("Franziska", 4, 2, 5),
        Character("Godot", 4, 5, 4),
        Character("Edgeworth", 5, 5, 4),
        Character("Phoenix", 5, 4, 5)
    ]

    def write_data_to_csv(data, filename='game_data.csv'):
        file_exists = os.path.isfile(filename)
        with open(filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())

            # 如果文件是新创建的，就写入表头
            if not file_exists:
                writer.writeheader()

            # 写入数据
            writer.writerow(data)

    def choose_strategy1():
        # Create a DataFrame with the current state for the model to predict

        input_features = pd.DataFrame([{
            'round_number': rounds,
            'player_health': player_health,
            'computer_health': computer_health,
            'last_round_choice': last_round_choice if last_round_choice is not None else 0,
            'player_char': player_char,


            # Use 0 or another default if no last round exists
        }])

        # Predict the player's next move using the trained mode
        predicted_player_move_index = best_model.predict(input_features)[0]
        last_player_choice = predicted_player_move_index  # Update last_player_choice with the current move

        # Map the index back to the corresponding move
        moves = ['Evidence', 'Cross-examination', 'Bluff']  # Ensure this order matches the training data
        predicted_player_move = moves[predicted_player_move_index]

        # Define a counter strategy based on the predicted move
        counter_strategies = {
            'Cross-examination': 'Evidence',
            'Bluff': 'Cross-examination',
            'Evidence': 'Bluff'
        }

        # Select the counter move
        computer_strategy = counter_strategies[predicted_player_move]
        print(f"last round choice{last_round_choice}")
        print(f"bot predicted {predicted_player_move}")
        predicted_choices.append(predicted_player_move_index)
        return computer_strategy

    def generate_charts(game_data):
        # Converting game data to DataFrame
        df = pd.DataFrame(game_data)

        # Defining characteristics and target variables
        X = df[['round_number', 'player_health', 'computer_health', 'last_round_choice', 'player_char']]
        y = df['player_choice']

        # Segmented data sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create and train the model
        model = RandomForestClassifier(class_weight=class_weight,random_state=42)
        model.fit(X_train, y_train)

        # Predictive Test Set
        y_pred = model.predict(X_test)

        # Drawing the confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(10, 7))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.show()

        # Mapping the significance of features
        feature_importances = model.feature_importances_
        plt.figure(figsize=(10, 7))
        sns.barplot(x=feature_importances,
                    y=['round_number', 'player_health', 'computer_health', 'last_round_choice', 'player_char'])
        plt.title("Feature Importances")
        plt.xlabel("Importance")
        plt.ylabel("Feature")
        plt.show()

    def evaluate_predictions(predicted_choices, actual_choices):
        # Calculate the confusion matrix
        cm = confusion_matrix(actual_choices, predicted_choices)
        print("Confusion Matrix:")
        print(cm)

        # Drawing the confusion matrix
        plt.figure(figsize=(10, 7))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.show()

        # Calculation accuracy
        accuracy = accuracy_score(actual_choices, predicted_choices)
        print(f"Accuracy: {accuracy:.2f}")

        # Generation of classification reports
        report = classification_report(actual_choices, predicted_choices)
        print("Classification Report:")
        print(report)

    print("Characters Abilities:")
    for character in characters:
        print(
            f"Name: {character.name}, Evidence: {character.rock_star}, Cross-Examination: {character.paper_star}, Bluff: {character.scissors_star}")

    # 玩家选择角色
    print("\nCHOOSE YOUR HERO!：")
    for i, character in enumerate(characters):
        print(f"{i + 1}. {character.name}")

    player_char = int(input("The chosen one is：")) - 1
    player_character = characters[player_char]

    # 电脑随机选择角色
    computer_choice = random.randint(0, 6)
    computer_character = characters[computer_choice]

    def calculate_damage(self, player_selection, computer_selection):
        if damage_flag == 0:
            if (player_selection, computer_selection) in WIN_LIST_RPS:
                ##self = player_character
                if player_selection == 'Evidence' and computer_selection == 'Cross-examination':
                    return 10 + 3 * self.rock_star
                elif player_selection == 'Cross-examination' and computer_selection == 'Bluff':
                    return 10 + 3 * self.paper_star
                elif player_selection == 'Bluff' and computer_selection == 'Evidence':
                    return 10 + 3 * self.scissors_star
            elif (computer_selection, player_selection) in WIN_LIST_RPS:
                ##self = computer_character
                if player_selection == 'Cross-examination' and computer_selection == 'Evidence':
                    return 10 + 3 * self.rock_star
                elif player_selection == 'Bluff' and computer_selection == 'Cross-examination':
                    return 10 + 3 * self.paper_star
                elif player_selection == 'Evidence' and computer_selection == 'Bluff':
                    return 10 + 3 * self.scissors_star
        elif damage_flag == 1:
            if (player_selection, computer_selection) in WIN_LIST_RPS:
                if player_selection == 'Evidence' and computer_selection == 'Cross-examination':
                    return 30 - 3 * self.rock_star
                elif player_selection == 'Cross-examination' and computer_selection == 'Bluff':
                    return 30 - 3 * self.paper_star
                elif player_selection == 'Bluff' and computer_selection == 'Evidence':
                    return 30 - 3 * self.scissors_star
            elif (computer_selection, player_selection) in WIN_LIST_RPS:
                if player_selection == 'Cross-examination' and computer_selection == 'Evidence':
                    return 30 - 3 * self.rock_star
                elif player_selection == 'Bluff' and computer_selection == 'Cross-examination':
                    return 30 - 3 * self.paper_star
                elif player_selection == 'Evidence' and computer_selection == 'Bluff':
                    return 30 - 3 * self.scissors_star

    def record_game_data(player_choice, computer_choice, result, round_number, player_health,
                         computer_health, player_char):
        # 这里假设有一个函数用于记录游戏数据
        game_data = {

            'player_choice': player_choice,
            'computer_choice': computer_choice,
            'result': result,
            'round_number': round_number,
            'player_health': player_health,
            'computer_health': computer_health,
            'player_char': player_char
        }

        # 将game_data写入CSV文件或数据库
        write_data_to_csv(game_data)  # 你需要实现这个函数\

    def choose_strategy():
        # 获取玩家每个选项的星级
        # player_option_star_levels = get_player_option_star_levels()  # 假设这个函数返回如 {'Evidence': 4, 'Cross-examination': 5, 'Bluff': 3}

        # 根据星级选择玩家最强的策略
        strongest_player_option = \
            max(enumerate(
                [player_character.rock_star, player_character.paper_star, player_character.scissors_star]),
                key=lambda x: x[1])[0]

        # 如果电脑健康值低，尝试反击玩家最强的策略
        if computer_health < 50:
            if strongest_player_option == "Evidence":
                return "Cross-examination"
            elif strongest_player_option == "Cross-examination":
                return "Bluff"
            elif strongest_player_option == "Bluff":
                return "Evidence"
        else:
            # 健康值较高时，考虑玩家最常用的策略
            most_common_player_selection = max(set(player_selection), key=player_selection.count)
            if most_common_player_selection == "Evidence":
                return "Cross-examination"
            elif most_common_player_selection == "Cross-examination":
                return "Bluff"
            else:
                return "Evidence"

    # game_data = {
    #     'player_choice': player_choice,
    #     'computer_choice': computer_choice,
    #     'result': result,
    #     'round_number': round_number,
    #     'player_health': player_health,
    #     'computer_health': computer_health,
    # }

    # 显示玩家和电脑选择的角色信息
    print("\nPlayer picked the character of：" + player_character.name)
    print("Computer picked the character of" + computer_character.name)
    damage_flag = damage_flag
    running = True
    while running:

        # Player's choice (simulate button press)
        print("\nChoose from below：")
        for i, option in enumerate(three_options):
            print(f"{i + 1}. {three_options[i]}")
        player_choice = 0
        try:
            player_choice = int(input("Please choose your strat：")) - 1
            if player_choice not in [0, 1, 2]:
                raise ValueError("Invalid choice. Please select 1, 2, or 3.")
        except ValueError as e:
            print(e)
            print("Please enter a valid number.")
            continue  # 保持循环继续，回到选择开始的地方

        player_selection = three_options[player_choice]
        actual_choices.append(player_choice)
        damage_flag = 0
        try:
            change_flag = int(input("Do you want to switch the damage calculation mode? Enter 1 for YES, 0 for NO: "))
            if change_flag == 1:
                 if damage_flag == 0:
                    damage_flag = 1
                 else:
                     damage_flag = 0
            # switching
            elif change_flag != 0:
                raise ValueError("Please enter 1 or 0.")
        except ValueError as e:
            print(e)
            print("Continuing with current mode.")
        # Computer's choice
        computer_selection = choose_strategy1()
        rounds += 1
        print("\nPlayer chose strategy：" + player_selection)
        print("\nBot chose strategy：" + computer_selection)
        # Determine the winner
        if player_selection == computer_selection:
            ties += 1
        elif (player_selection, computer_selection) in WIN_LIST_RPS:
            print("\nplayer wins this round")
            player_score += 1

            computer_health -= calculate_damage(player_character, player_selection, computer_selection)
            print(f"\nbot health:{computer_health}" + f"player health:{player_health}")

        else:
            print("\nbot wins this round")
            computer_score += 1
            calculate_damage(computer_character, player_selection, computer_selection)
            player_health -= calculate_damage(computer_character, player_selection, computer_selection)
            print(f"\nbot health:{computer_health}" + f"player health:{player_health}")
        record_game_data(player_choice, computer_choice, player_score, rounds, player_health,
                         computer_health, player_char)
        last_round_choice = player_choice
        # Check for game over conditions
        if player_health <= 0 or computer_health <= 0:
            break

        # Update display

    # Game over
    if player_health <= 0:
        print("You lost!")
    elif computer_health <= 0:
        print("You won!")
    else:
        print("It's a tie!")
    generate_charts(data)
    evaluate_predictions(predicted_choices, actual_choices)
    # Quit Pygame


if __name__ == '__main__':
    main()
