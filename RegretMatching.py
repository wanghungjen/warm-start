import random
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import time

# TODO: Figure out numberOfActions correctly
class Finder():
    # Definitions
    # numberOfActions: int
    
    # Constructor
    def __init__(self, matrix):
        self.matrix = matrix
        self.oppMatrix = -self.matrix.T
        self.numberOfOppActions = matrix[0].size
        self.numberOfMyActions = matrix.size // self.numberOfOppActions
        self.regretSum: list[float] = [0] * self.numberOfMyActions
        self.strategy: list[float] = [0] * self.numberOfMyActions
        self.strategySum: list[float] = [0] * self.numberOfMyActions
        self.oppRegretSum: list[float] = [0] * self.numberOfOppActions
        self.oppStrategy: list[float] = [0] * self.numberOfOppActions
        self.oppStrategySum: list[float] = [0] * self.numberOfOppActions
        self.exploitabilities: list[float] = []
        self.tippingPoint = -1

    # Get current mixed strategy through regret-matching
    def getStrategy(self) -> list[float]:
        normalizingSum: float = 0
        for i in range(0, self.numberOfMyActions):
            if (self.regretSum[i] > 0):
                self.strategy[i] = self.regretSum[i]
            else:
                self.strategy[i] = 0
            normalizingSum += self.strategy[i]
        for i in range(0, self.numberOfMyActions):
            if (normalizingSum > 0):
                self.strategy[i] /= normalizingSum
            else:
                self.strategy[i] = 1 / self.numberOfMyActions
            self.strategySum[i] += self.strategy[i]
        return self.strategy

    def getOppStrategy(self) -> list[float]:
        normalizingSum: float = 0
        for i in range(0, self.numberOfOppActions):
            if (self.oppRegretSum[i] > 0):
                self.oppStrategy[i] = self.oppRegretSum[i]
            else:
                self.oppStrategy[i] = 0
            normalizingSum += self.oppStrategy[i]
        for i in range(0, self.numberOfOppActions):
            if (normalizingSum > 0):
                self.oppStrategy[i] /= normalizingSum
            else:
                self.oppStrategy[i] = 1 / self.numberOfOppActions
            self.oppStrategySum[i] += self.oppStrategy[i]
        return self.oppStrategy

    def getMyAction(self, myStrategy: list[float]) -> int:
        randomNum: float = random.uniform(0, 1)
        i: int = 0
        cumulativeProbability: float = 0
        while(i < (self.numberOfMyActions - 1)):
            cumulativeProbability += myStrategy[i]
            if (randomNum < cumulativeProbability):
                break
            i += 1
        return i

    def getOppAction(self, myStrategy: list[float]) -> int:
        randomNum: float = random.uniform(0, 1)
        i: int = 0
        cumulativeProbability: float = 0
        while(i < (self.numberOfOppActions - 1)):
            cumulativeProbability += myStrategy[i]
            if (randomNum < cumulativeProbability):
                break
            i += 1
        return i

    def get_row_best_response(self, matrix, col_strategy):
        # Given a matrix game and col_strategy, the best response is the row which maximizes expected payoff
        
        # WORKS BUT IS INCREDIBLY SLOW - ASK WHY 
        
        # acc = []
        # for i in range(0, self.numberOfActions - 1):
        #     sum = 0
        #     for j in range(0, self.numberOfActions - 1):
        #         sum += matrix[i][j] * col_strategy[j]
        #     acc.append(sum)
        
        # return np.array(acc).argmax()

        return (matrix @ col_strategy).argmax()

    def get_exploitability(self, matrix, row_strategy, col_strategy):
        # Given a matrix game and a row_strategy and col_strategy, exploitability measures how
        # "far away" the strategies are from a Nash equilibrium. When they are perfect, exploitability is 0.
        br_row = self.get_row_best_response(matrix, col_strategy)
        br_col = self.get_row_best_response(-matrix.T, row_strategy)
        return ((matrix @ col_strategy)[br_row] + (-matrix.T @ row_strategy)[br_col]) / 2

    def train(self, iterations: int):
        exploitabilities = []
        
        myActionUtility: list[float] = [0] * self.numberOfMyActions
        oppActionUtility: list[float] = [0] * self.numberOfOppActions

        for i in range(0, iterations):
            # print(i)
            myStrategy: list[float] = self.getStrategy()
            oppStrategy: list[float] = self.getOppStrategy()
            
            myAction: int = self.getMyAction(myStrategy)
            oppAction: int = self.getOppAction(oppStrategy)
            # myAction: int = get_row_best_response(matrix, np.array(oppStrategy))
            # oppAction: int = get_row_best_response(oppMatrix, np.array(myStrategy))
            
            for j in range(0, self.numberOfMyActions):
                myActionUtility[j] = self.matrix[j][oppAction]
                
            for j in range(0, self.numberOfOppActions):    
                oppActionUtility[j] = self.oppMatrix[j][myAction]
            
            for j in range(0, self.numberOfMyActions):
                self.regretSum[j] += myActionUtility[j] - myActionUtility[myAction]
            
            for j in range(0, self.numberOfOppActions):
                self.oppRegretSum[j] += oppActionUtility[j] - oppActionUtility[oppAction]

            currentExploitability = self.get_exploitability(self.matrix, np.array(self.getMyAverageStrategy()), np.array(self.getOppAverageStrategy()))
            if (currentExploitability <= 0.01 and self.tippingPoint == -1):
                # print(currentExploitability)
                # print(i)
                self.tippingPoint = i

            exploitabilities.append(currentExploitability)
            # print(i)
        return exploitabilities

    def getMyAverageStrategy(self) -> list[float]:
        averageStrategy: list[float] = [0] * self.numberOfMyActions
        normalizingSum: float = 0
        for i in range(0, self.numberOfMyActions):
            normalizingSum += self.strategySum[i]
        for i in range(0, self.numberOfMyActions):
            if (normalizingSum > 0):
                averageStrategy[i] = self.strategySum[i] / normalizingSum
            else:
                averageStrategy[i] = 1 / self.numberOfMyActions
        return averageStrategy

    def getOppAverageStrategy(self) -> list[float]:
        averageStrategy: list[float] = [0] * self.numberOfOppActions
        normalizingSum: float = 0
        for i in range(0, self.numberOfOppActions):
            normalizingSum += self.oppStrategySum[i]
        for i in range(0, self.numberOfOppActions):
            if (normalizingSum > 0):
                averageStrategy[i] = self.oppStrategySum[i] / normalizingSum
            else:
                averageStrategy[i] = 1 / self.numberOfOppActions
        return averageStrategy



def create(x: int, y: int):
    # Populating the game
    matrix = [[0] * y for _ in range(x)]

    for playerOneStrategy in range(0, x):
        for playerTwoStrategy in range(0, y):
            matrix[playerOneStrategy][playerTwoStrategy] = random.uniform(-1, 1)

    return np.array(matrix)
    # self.oppMatrix = -self.matrix.T

# rm_exploitabilitiesz = []
# print(create(5, 3))

# # Initialize Game
# myGame = create(100, 100)
# print(myGame)
# for t in tqdm(range(8)):
#     # print(myGame)
    
#     # Initialize number of actions
#     finder = Finder(myGame)

#     # Train!
#     rm_exploitabilitiesz.append(finder.train(10000))

#     # Nash Equilibrium!
#     print(finder.getMyAverageStrategy())
#     print(finder.getOppAverageStrategy())

# plt.plot([sum(x)/len(x) for x in zip(*rm_exploitabilitiesz)])
# plt.yscale('log')
# plt.xscale('log')
# plt.title('RM')
# plt.show()