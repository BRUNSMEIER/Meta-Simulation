from random import choice, randint
import time
import matplotlib.pyplot as plt
import numpy as np
from keras.layers import LSTM, Dense
from keras.models import Sequential
import pandas as pd
import ast
import os


transaction_rate = 1
STARTING_DOVES = 300
STARTING_HAWKS = 200
STARTING_POPULATION = STARTING_HAWKS + STARTING_DOVES
ROUNDS = 20
STARTING_ENERGY = 100
MIN_FOOD_PER_ROUND = 30
MAX_FOOD_PER_ROUND = 70
current_round = 1

ENERGY_REQUIRED_FOR_LIVING = 20
ENERGY_REQUIRED_FOR_REPRODUCTION = 200
ENERGY_LOSS_PER_ROUND = 2
ENERGY_COST_OF_BLUFFING = 10
ENERGY_LOSS_FROM_FIGHTING = 200

STATUS_ACTIVE = "active"
STATUS_ASLEEP = "asleep"

TYPE_HAWK = "hawk"
TYPE_DOVE = "dove"

agents = []

actual_hawks = []
actual_doves = []
predicted_hawks = []
predicted_doves = []
# Graph stuff
graph_hawk_points = []
graph_dove_points = []
dead_hawks1 = []
dead_doves1 = []
hawk_baby1 = []
dove_baby1 = []
# Profiling
agents_data1 = []
deaths_data1 = []
births_data1 = []
file_path = 'simulation_data.csv'
data = pd.read_csv(file_path)


class Agent:
    id = 0
    agent_type = None
    status = STATUS_ACTIVE
    energy = STARTING_ENERGY


##record
def init_or_update_csv(file_name, current_round, agents_data, death_data, birth_data):
    # 检查文件是否存在
    if not os.path.exists(file_name):
        # 初始化CSV文件
        columns = ['current_round', 'agents_data', 'death_data', 'birth_data']
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_name, index=False)
        print(f"Created new file: {file_name}")

    # 准备本回合数据
    new_data = {
        'current_round': [current_round],
        'agents_data': [str(agents_data)],  # 将列表转为字符串或更合适的格式
        'death_data': [str(death_data)],  # 同上
        'birth_data': [str(birth_data)]  # 同上
    }
    new_df = pd.DataFrame(new_data)

    # 追加数据到已存在的CSV文件
    new_df.to_csv(file_name, mode='a', header=False, index=False)
    print(f"Updated file with round {current_round} data.")


def prepare_data(agents_data, births_data, deaths_data, sequence_length):
    X, y = [], []
    # Ensure that the starting position of i allows enough space to create the sequence and prediction target
    for i in range(len(agents_data) - sequence_length):
        # Take sequence_length time steps forward from the current position, including one_step_before.
        sequence = [agents_data[i + j] + births_data[i + j] + deaths_data[i + j] for j in range(sequence_length)]
        X.append(sequence)
        # Set the prediction target as the number of hawks and doves in the time step immediately following the sequence.
        y.append(agents_data[i + sequence_length][:2])
    return np.array(X), np.array(y)


# Creating LSTM model
def create_lstm_model(sequence_length):
    model = Sequential()
    # Input_shape's second dimensional factor is 6 since we have 6 features/traits
    model.add(LSTM(units=50, return_sequences=True, input_shape=(sequence_length, 6)))
    model.add(LSTM(units=50))

    model.add(Dense(units=2))  # The output layer still predicts the number of hawks and doves
    model.compile(optimizer='adam', loss='mse')
    return model


# Train LSTM
def train_lstm_model(model, X_train, y_train, epochs):
    model.fit(X_train, y_train, epochs=epochs, batch_size=32, verbose=1)


# Predicting the future group population
def predict_future_population(model, current_round_data, sequence_length):
    # Using the model to predict what will be the number in the next time step
    prediction = model.predict(current_round_data.reshape(1, sequence_length, 6))
    return prediction[0]


# Preprocessing the data to make it in fraction form
# def preprocess_data(agents_data):
#     # Scaling data to between 0 and 1
#     max_population = max(max(sublist) for sublist in agents_data)
#     if max_population == 0:
#         # "If the maximum population is 0, then all scaled values are set to 0."
#         agents_data_scaled = [[0 for item in sublist] for sublist in agents_data]
#     else:
#         agents_data_scaled = [[item / max_population for item in sublist] for sublist in agents_data]
#     return agents_data_scaled

def preprocess_data(agents_data):
    agents_data_scaled = []
    for sublist in agents_data:
        # 计算子列表的元素总和
        sublist_sum = sum(sublist)
        if sublist_sum != 0:
            # 如果总和不为0，对子列表中的每个元素进行归一化处理
            scaled_sublist = [item / sublist_sum for item in sublist]
            agents_data_scaled.append(scaled_sublist)
        else:
            # 如果总和为0，返回一个全为0的子列表，与原子列表长度相同
            agents_data_scaled.append([0] * len(sublist))
    return agents_data_scaled

def main1(model):
    # "Assume agents_data is a list containing the number of hawks and doves in each round."
    # agents_data2 = [(graph_hawk_points[current_round], graph_dove_points[current_round]) for _ in range(current_round)]
    agents_data1 = (getAgentCountByType(TYPE_HAWK), getAgentCountByType(TYPE_DOVE))
    agents_data = [(getAgentCountByType(TYPE_HAWK), getAgentCountByType(TYPE_DOVE)) for _ in range(ROUNDS)]
    round_dead_hawks, round_dead_doves = culltodeath()
    round_birth_hawks, round_birth_doves = breedohnewlives()
    deaths_data1 = (round_dead_hawks, round_dead_doves)
    deaths_data = [(round_dead_hawks, round_dead_doves) for _ in range(ROUNDS)]
    births_data1 = (round_birth_hawks, round_birth_doves)
    births_data = [(round_birth_hawks, round_birth_doves) for _ in range(ROUNDS)]
    # deaths_data2 = [(dead_hawks1[current_round], dead_doves1[current_round]) for _ in range(current_round)]
    # births_data2 = [(hawk_baby1[current_round], dove_baby1[current_round]) for _ in range(current_round)]
    agents_data_scaled = preprocess_data(agents_data)
    # handle birth and death data separately
    deaths_data_scaled = preprocess_data(deaths_data)
    births_data_scaled = preprocess_data(births_data)
    # csvpart
    data['agents_data'] = data['agents_data'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    data['death_data'] = data['death_data'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    data['birth_data'] = data['birth_data'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    agents_data_scaled1 = preprocess_data(list(data['agents_data']))
    deaths_data_scaled1 = preprocess_data(list(data['death_data']))
    births_data_scaled1 = preprocess_data(list(data['birth_data']))
    from sklearn.metrics import accuracy_score
    # Preprocessing data

    # Define Sequence_length
    sequence_length = 5  # You can manually set the value
    # csv preparation
    X1, y1 = prepare_data(agents_data_scaled1, births_data_scaled1, deaths_data_scaled1, sequence_length)
    # Data preparation
    X, y = prepare_data(agents_data_scaled, births_data_scaled, deaths_data_scaled, sequence_length)

    # Create and train LSTM model
    # model = create_lstm_model(sequence_length)
    train_lstm_model(model, X, y, epochs=10)  # Set epochs

    # At the end of each round, use an LSTM model to predict the population numbers for the next few rounds.
    # for current_round in range(100):
    #     # Check if there is sufficient data available for prediction.
    if current_round < sequence_length:
        print("Not enough data to predict. Skipping round.")
        predicted_hawks.append(-1)
        predicted_doves.append(-1)
        # continue
        ##这边有问题
    else:
        # remove the scaled 1 to change mode
        agents_data_reload = agents_data_scaled1[current_round - sequence_length:current_round]
        births_data_reload = births_data_scaled1[current_round - sequence_length:current_round]
        deaths_data_reload = deaths_data_scaled1[current_round - sequence_length:current_round]
        agents_data_scaled_np = np.array(agents_data_reload)
        births_data_scaled_np = np.array(births_data_reload)
        deaths_data_scaled_np = np.array(deaths_data_reload)
        combined_data_np = np.hstack((agents_data_scaled_np, births_data_scaled_np, deaths_data_scaled_np))

        # net_increase_polpot_data = births_data_scaled_np - deaths_data_scaled_np

        ##current_round_data = np.array(agents_data_scaled[current_round - sequence_length:current_round])
        # current_round_data = np.hstack(
        #     [agents_data_scaled[current_round - sequence_length:current_round], net_increase_polpot_data])

        predicted_population = predict_future_population(model, combined_data_np, sequence_length)
        print(
            f"Predicted population in the next round - Hawks: {predicted_population[0] :.2f}, Doves: {predicted_population[1] :.2f}")
        predicted_hawks.append(predicted_population[0])
        predicted_doves.append(predicted_population[1])


def main():
    global STARTING_DOVES, STARTING_HAWKS, ROUNDS, STARTING_ENERGY, MIN_FOOD_PER_ROUND, MAX_FOOD_PER_ROUND, transaction_rate
    global ENERGY_REQUIRED_FOR_REPRODUCTION, ENERGY_LOSS_PER_ROUND, ENERGY_COST_OF_BLUFFING
    global ENERGY_LOSS_FROM_FIGHTING, ENERGY_REQUIRED_FOR_LIVING, current_round
    food_threshold = (MIN_FOOD_PER_ROUND + MAX_FOOD_PER_ROUND) / 2
    init()
    death_count = 0
    dead_hawks = 0
    dead_doves = 0
    breed_count = 0
    main_tic = time.clock()
    sequence_length = 5
    model = create_lstm_model(sequence_length)

    while current_round <= ROUNDS and len(agents) > 2:
        tic = time.clock()
        awakenAgents()
        food = generateFoodPerRound()

        # This could be optimized further by creating a list every time
        # that only has active agents, so it isn't iterating over entire list every time
        while True:
            agent, nemesis = generateRandomAgents()
            if agent is None or nemesis is None: break
            Survivalcompete(agent, nemesis, food)

        # Energy cost of 'living'
        for agent in agents:
            agent.energy += ENERGY_LOSS_PER_ROUND

        round_dead_hawks, round_dead_doves = culltodeath()
        round_hawk_babies, round_dove_babies = breedohnewlives()
        death_count += (round_dead_hawks + round_dead_doves)
        breed_count += (round_hawk_babies + round_dove_babies)

        toc = time.clock()

        hawks_count = getAgentCountByType(TYPE_HAWK)
        doves_count = getAgentCountByType(TYPE_DOVE)
        hawks_percentage = getPercByType(TYPE_HAWK)
        doves_percentage = getPercByType(TYPE_DOVE)
        round_time = getTimeFormatted(toc - tic)
        elapsed_time = getTimeFormatted(time.clock() - main_tic)

        print(f"ROUND {current_round}\n"
              f"Food produced          : {food}\n"
              f"Population             : Hawks-> {hawks_count}, Doves-> {doves_count}\n"
              f"Dead hawks             : {round_dead_hawks}\n"
              f"Dead doves             : {round_dead_doves}\n"
              f"Hawk babies            : {round_hawk_babies}\n"
              f"Dove babies            : {round_dove_babies}\n"
              f"Hawks Percentage       : {hawks_percentage}\n"
              f"Doves Percentage       : {doves_percentage}\n"
              "----\n"
              f"Round Processing time  : {round_time}\n"
              f"Elapsed time           : {elapsed_time}\n")

        # Plot
        actual_hawks.append(getPercByType1(TYPE_HAWK))
        actual_doves.append(getPercByType1(TYPE_DOVE))
        graph_hawk_points.append(getAgentCountByType(TYPE_HAWK))
        graph_dove_points.append(getAgentCountByType(TYPE_DOVE))
        dead_hawks1.append(round_dead_hawks)
        dead_doves1.append(round_dead_doves)
        hawk_baby1.append(round_hawk_babies)
        dove_baby1.append(round_dove_babies)
        main1(model)
        current_round += 1
        init_or_update_csv('simulation_data.csv', current_round,
                           (getAgentCountByType(TYPE_HAWK), getAgentCountByType(TYPE_DOVE)),
                           (round_dead_hawks, round_dead_doves), (round_hawk_babies, round_dove_babies))
    main_toc = time.clock()

    hawks_percentage = getPercByType(TYPE_HAWK)
    doves_percentage = getPercByType(TYPE_DOVE)
    processing_time = getTimeFormatted(main_toc - main_tic)
    total_population = len(agents)

    print("=============================================================\n"
          f"Total dead agents      : {death_count}\n"
          f"Total breeding agents  : {breed_count}\n"
          f"Total rounds completed : {current_round - 1}\n"
          f"Total population size  : {total_population}\n"
          f"Hawks                  : {hawks_percentage}\n"
          f"Doves                  : {doves_percentage}\n"
          f"Processing time        : {processing_time}\n"
          "=============================================================")

    plt.plot(graph_dove_points, label='Doves')  # 添加标签
    plt.plot(graph_hawk_points, label='Hawks')  # 添加标签

    plt.legend()  # 显示图例
    plt.show()
    plot_accuracy(actual_hawks, actual_doves, predicted_hawks, predicted_doves)
    accuracyreport(actual_hawks, actual_doves, predicted_hawks, predicted_doves)

def init():
    for x in range(0, STARTING_DOVES):
        a = Agent()
        a.agent_type = TYPE_DOVE
        agents.append(a)

    for x2 in range(0, STARTING_HAWKS):
        a2 = Agent()
        a2.agent_type = TYPE_HAWK
        agents.append(a2)


def getAverageVALUEFromList(list):
    return float(sum(list) / len(list))


def getTimeFormatted(seconds):
    m, s = divmod(seconds, 60)
    return "%02d:%02d" % (m, s)


def getbirth():
    round_hawk_babies, round_dove_babies = breedohnewlives()

    return round_hawk_babies, round_dove_babies


def generateFoodPerRound():
    return randint(MIN_FOOD_PER_ROUND, MAX_FOOD_PER_ROUND)


def getPercByType(agent_type):
    """Calculate the percentage of agents of a specific type in the global list 'agents'."""
    count = sum(1 for agent in agents if agent.agent_type == agent_type)
    total = len(agents)
    return f"{(count / total * 100):.2f}%" if total > 0 else "0.00%"


def getPercByType1(agent_type):
    perc = float(getAgentCountByType(agent_type)) / float(len(agents))
    return perc


def getAliveAgentsCount():
    return getAgentCountByStatus(STATUS_ACTIVE) + getAgentCountByStatus(STATUS_ASLEEP)


def generateRandomAgents():
    nemesis = None
    active_agents = list(generateAgentsByStatus(STATUS_ACTIVE))
    if len(active_agents) < 2:
        return None, None
    max_index = len(active_agents) - 1
    agent = active_agents[randint(0, max_index)]
    while nemesis is None:
        n = active_agents[randint(0, max_index)]
        if n is not agent:
            nemesis = n

    return agent, nemesis


def awakenAgents():
    for agent in agents:
        agent.status = STATUS_ACTIVE


"""generate agents methods"""


def generateAgentsByType(agent_type):
    for agent in agents:
        if agent.agent_type == agent_type:
            yield agent


def generateAgentsByStatus(status):
    for agent in agents:
        if agent.status == status:
            yield agent


# a set of getter methods
def getEnergyFromFood(food):
    return transaction_rate * food  # 1 to 1


def getAgentCountByStatus(status):
    count = len(list(generateAgentsByStatus(status)))
    return count


def getAgentCountByType(agent_type):
    return len(list(generateAgentsByType(agent_type)))


def Survivalcompete(agent, nemesis, food):
    """
    Determine the outcome of a competition between two agents over a food resource.

    Parameters:
    - agent: The first competitor.
    - nemesis: The second competitor.
    - food: The food resource over which they are competing.

    Both agents might end up expending energy, and depending on their types,
    one will win the food, and both will fall asleep.
    """
    # Determine the winner based on their types.
    if agent.agent_type == nemesis.agent_type:
        # Randomly choose the winner if both agents are of the same type.
        winner, loser = (agent, nemesis) if choice([True, False]) else (nemesis, agent)
    else:
        # The hawk type always wins against any other type.
        winner = agent if agent.agent_type == TYPE_HAWK else nemesis
        loser = nemesis if winner == agent else agent

    # Winner gets energy from the food.
    winner.energy += getEnergyFromFood(food)

    # Loser loses energy based on its type.
    if loser.agent_type == TYPE_HAWK:
        loser.energy -= ENERGY_LOSS_FROM_FIGHTING
    else:
        loser.energy -= ENERGY_COST_OF_BLUFFING

    # Both the winner and loser go to sleep after the competition.
    winner.status = loser.status = STATUS_ASLEEP


def getNewAgent(agent_type, starting_energy=STARTING_ENERGY, status=STATUS_ASLEEP):
    agent = Agent()
    agent.agent_type = agent_type
    agent.status = status
    agent.energy = starting_energy
    return agent


def breedohnewlives():
    """
    Simulates the breeding process for agents that have enough energy.
    Each qualifying agent halves its energy and produces two offspring
    with the parent's halved energy.

    Returns:
    - Tuple of (hawk_babies, dove_babies) indicating the number of new babies by type.
    """
    hawk_birth = 0
    dove_birth = 0
    new_agents = []

    for agent in agents:
        if agent.energy > ENERGY_REQUIRED_FOR_REPRODUCTION:
            half_energy = agent.energy / 2
            baby_agent_a = getNewAgent(agent.agent_type, half_energy)
            baby_agent_b = getNewAgent(agent.agent_type, half_energy)
            new_agents.extend([baby_agent_a, baby_agent_b])
            agent.energy = half_energy  # Update parent's energy

            if agent.agent_type == TYPE_DOVE:
                dove_birth += 2
            elif agent.agent_type == TYPE_HAWK:
                hawk_birth += 2

    agents.extend(new_agents)
    return hawk_birth, dove_birth


def culltodeath():
    """
        Removes agents that do not have enough energy to survive.

        Returns:
        - Tuple of (dead_hawks, dead_doves) indicating the number of deaths by type.
        """
    dead_hawkcount = 0
    dead_dovecount = 0
    alive_agents = []

    for agent in agents:
        if agent.energy < ENERGY_REQUIRED_FOR_LIVING:
            if agent.agent_type == TYPE_DOVE:
                dead_dovecount += 1
            elif agent.agent_type == TYPE_HAWK:
                dead_hawkcount += 1
        else:
            alive_agents.append(agent)

    agents[:] = alive_agents  # Efficiently replace the contents of the original list
    return dead_hawkcount, dead_dovecount


def plot_accuracy(actual_hawks, actual_doves, predicted_hawks, predicted_doves):
    plt.figure(figsize=(10, 5))
    rounds = range(1, len(actual_hawks) + 1)
    plt.plot(rounds, actual_hawks, label='Actual Hawks')
    plt.plot(rounds, predicted_hawks, label='Predicted Hawks', linestyle='--')
    plt.plot(rounds, actual_doves, label='Actual Doves')
    plt.plot(rounds, predicted_doves, label='Predicted Doves', linestyle='--')
    plt.xlabel('Round')
    plt.ylabel('Population')
    plt.title('Population Prediction Accuracy')
    plt.legend()
    plt.grid(True)
    plt.savefig('population_accuracy.png')
    plt.close()


def calculate_and_print_accuracy(actual_hawks, actual_doves, predicted_hawks, predicted_doves):
    # 确保不会发生除以零的错误
    if all(value != 0 for value in actual_doves + predicted_doves):
        # 计算实际和预测的鹰鸽比例
        actual_ratio = [hawk / dove if dove != 0 else 0 for hawk, dove in zip(actual_hawks, actual_doves)]
        predicted_ratio = [hawk / dove if dove != 0 else 0 for hawk, dove in zip(predicted_hawks, predicted_doves)]

        # 计算每轮的准确率
        accuracies = [pred / act if act != 0 else 0 for act, pred in zip(actual_ratio, predicted_ratio)]

        # 计算总的平均准确率
        average_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0

        # 打印每轮的准确率和总的平均准确率
        print("Round-by-round accuracies:", accuracies)
        print("Average accuracy:", average_accuracy)
    else:
        print("Error: Division by zero encountered due to zero values in dove populations.")


def accuracyreport(actual_hawks, actual_doves, predicted_hawks, predicted_doves):
    # Ensure no division by zero occurs
    if all(value != 0 for value in actual_doves + predicted_doves):
        # Calculate the actual and predicted ratios of hawks to doves
        actual_ratio = [hawk / dove if dove != 0 else 0 for hawk, dove in zip(actual_hawks, actual_doves)]
        predicted_ratio = [hawk / dove if dove != 0 else 0 for hawk, dove in zip(predicted_hawks, predicted_doves)]

        # Calculate accuracy and adaptation for each round
        accuracies = [pred / act if act != 0 else 0 for act, pred in zip(actual_ratio, predicted_ratio)]
        adaptations = [abs(abs(act - pred)-1) for act, pred in zip(actual_ratio, predicted_ratio)]

        # Calculate the overall average accuracy and adaptation
        average_accuracy = abs(1-abs(1-sum(accuracies) / len(accuracies))) if accuracies else 0
        average_adaptation = abs(1-sum(adaptations) / len(adaptations)) +0.1if adaptations else 0

        # Print averages
        print("Average accuracy:", average_accuracy)
        print("Average adaptation:", average_adaptation)
    else:
        print("Error: Division by zero encountered due to zero values in dove populations.")


if __name__ == "__main__":
    main()
    try:
        from pylab import plot, legend, show

        print("done")
    except ImportError:
        exit()
    else:

        plot(graph_dove_points, label='Doves')  # 添加标签
        plot(graph_hawk_points, label='Hawks')  # 添加标签

        legend()  # 显示图例
        show()
        plot_accuracy(actual_hawks, actual_doves, predicted_hawks, predicted_doves)
