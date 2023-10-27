import random
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Make a function that makes random 2-player zero-sum matrix games, or make some 2-player zero-sum matrix games like rock-paper-scissors.

def create(strategies: int) -> list[list[float]]:
    # Payoff Matrix
    matrix = [[0] * strategies for _ in range(strategies)]

    # Populating the game
    for playerOneStrategy in range(0, strategies):
        for playerTwoStrategy in range(0, strategies):
            matrix[playerOneStrategy][playerTwoStrategy] = random.uniform(-1, 1)

    return matrix

# Printing for debugging purposes
# sample_matrix = create(5)
# print(sample_matrix)

# Implement a regret matching function that takes in a matrix game and outputs an approximated Nash equilibrium strategy profile. 
# (Both Players use regret matching)
# I am the row player; Opponent is the column player
# Three actions , Bounded by three


numberOfActions: int = 100
# Our Payoff Matrix
# print(matrix)
# print(oppMatrix)

# Definitions
regretSum: list[float] = [0] * numberOfActions
strategy: list[float] = [0] * numberOfActions
strategySum: list[float] = [0] * numberOfActions
oppRegretSum: list[float] = [0] * numberOfActions
oppStrategy: list[float] = [0] * numberOfActions
oppStrategySum: list[float] = [0] * numberOfActions
exploitabilities: list[float] = []

# Get current mixed strategy through regret-matching
def getStrategy() -> list[float]:
    global strategySum
    global strategy
    normalizingSum: float = 0
    for i in range(0, numberOfActions):
        if (regretSum[i] > 0):
            strategy[i] = regretSum[i]
        else:
            strategy[i] = 0
        normalizingSum += strategy[i]
    for i in range(0, numberOfActions):
        if (normalizingSum > 0):
            strategy[i] /= normalizingSum
        else:
            strategy[i] = 1 / numberOfActions
        strategySum[i] += strategy[i]
    return strategy

def getOppStrategy() -> list[float]:
    global oppStrategySum
    global oppStrategy
    normalizingSum: float = 0
    for i in range(0, numberOfActions):
        if (oppRegretSum[i] > 0):
            oppStrategy[i] = oppRegretSum[i]
        else:
            oppStrategy[i] = 0
        normalizingSum += oppStrategy[i]
    for i in range(0, numberOfActions):
        if (normalizingSum > 0):
            oppStrategy[i] /= normalizingSum
        else:
            oppStrategy[i] = 1 / numberOfActions
        oppStrategySum[i] += oppStrategy[i]
    return oppStrategy

def getAction(myStrategy: list[float]) -> int:
    randomNum: float = random.uniform(0, 1)
    i: int = 0
    cumulativeProbability: float = 0
    while(i < (numberOfActions - 1)):
        cumulativeProbability += myStrategy[i]
        if (randomNum < cumulativeProbability):
            break
        i += 1
    return i


def get_row_best_response(matrix, col_strategy):
    # Given a matrix game and col_strategy, the best response is the row which maximizes expected payoff
    return (matrix @ col_strategy).argmax()
def get_exploitability(matrix, row_strategy, col_strategy):
    # Given a matrix game and a row_strategy and col_strategy, exploitability measures how
    # "far away" the strategies are from a Nash equilibrium. When they are perfect, exploitability is 0.
    br_row = get_row_best_response(matrix, col_strategy)
    br_col = get_row_best_response(-matrix.T, row_strategy)
    return ((matrix @ col_strategy)[br_row] + (-matrix.T @ row_strategy)[br_col]) / 2

def train(iterations: int):
    global regretSum
    global oppRegretSum
    global exploitabilities
    
    myActionUtility: list[float] = [0] * numberOfActions
    oppActionUtility: list[float] = [0] * numberOfActions

    for i in range(0, iterations):
        myStrategy: list[float] = getStrategy()
        oppStrategy: list[float] = getOppStrategy()
        
        myAction: int = getAction(myStrategy)
        oppAction: int = getAction(oppStrategy)

        for i in range(0, numberOfActions):
            myActionUtility[i] = matrix[i][oppAction]
            oppActionUtility[i] = oppMatrix[i][myAction]
        
        for i in range(0, numberOfActions):
            regretSum[i] += myActionUtility[i] - myActionUtility[myAction]
            oppRegretSum[i] += oppActionUtility[i] - oppActionUtility[oppAction]

        exploitabilities.append(get_exploitability(matrix, np.array(myStrategy), np.array(oppStrategy)))
        # print(strategy)
        # print(oppStrategy)


def getMyAverageStrategy() -> list[float]:
    averageStrategy: list[float] = [0] * numberOfActions
    normalizingSum: float = 0
    for i in range(0, numberOfActions):
        normalizingSum += strategySum[i]
    for i in range(0, numberOfActions):
        if (normalizingSum > 0):
            averageStrategy[i] = strategySum[i] / normalizingSum
        else:
            averageStrategy[i] = 1 / numberOfActions
    return averageStrategy

def getOppAverageStrategy() -> list[float]:
    averageStrategy: list[float] = [0] * numberOfActions
    normalizingSum: float = 0
    for i in range(0, numberOfActions):
        normalizingSum += oppStrategySum[i]
    for i in range(0, numberOfActions):
        if (normalizingSum > 0):
            averageStrategy[i] = oppStrategySum[i] / normalizingSum
        else:
            averageStrategy[i] = 1 / numberOfActions
    return averageStrategy

# print(getMyAverageStrategy())
# print(getOppAverageStrategy())

rm_exploitabilitiesz = []
for t in tqdm(range(8)):
    exploitabilities = []
    matrix = np.array(create(numberOfActions))
    oppMatrix = -matrix.T
    train(10000)
    rm_exploitabilitiesz.append(exploitabilities)

plt.plot([sum(x)/len(x) for x in zip(*rm_exploitabilitiesz)])
plt.yscale('log')
plt.xscale('log')
plt.title('RM')
plt.show()