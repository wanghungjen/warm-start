import random
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

class Finder():
    # Definitions
    numberOfActions: int
    
    # Constructor
    def __init__(self, strategies: int):
        self.numberOfActions = strategies
        self.regretSum: list[float] = [0] * self.numberOfActions
        self.strategy: list[float] = [0] * self.numberOfActions
        self.strategySum: list[float] = [0] * self.numberOfActions
        self.oppRegretSum: list[float] = [0] * self.numberOfActions
        self.oppStrategy: list[float] = [0] * self.numberOfActions
        self.oppStrategySum: list[float] = [0] * self.numberOfActions
        self.exploitabilities: list[float] = []
    
    # Creating Matrix
    def start(self):
        # Populating the game
        self.matrix = [[0] * self.numberOfActions for _ in range(self.numberOfActions)]

        for playerOneStrategy in range(0, self.numberOfActions):
            for playerTwoStrategy in range(0, self.numberOfActions):
                self.matrix[playerOneStrategy][playerTwoStrategy] = random.uniform(-1, 1)

        self.matrix = np.array(self.matrix)
        self.oppMatrix = -self.matrix.T

    # Get current mixed strategy through regret-matching
    def getStrategy(self) -> list[float]:
        normalizingSum: float = 0
        for i in range(0, self.numberOfActions):
            if (self.regretSum[i] > 0):
                self.strategy[i] = self.regretSum[i]
            else:
                self.strategy[i] = 0
            normalizingSum += self.strategy[i]
        for i in range(0, self.numberOfActions):
            if (normalizingSum > 0):
                self.strategy[i] /= normalizingSum
            else:
                self.strategy[i] = 1 / self.numberOfActions
            self.strategySum[i] += self.strategy[i]
        return self.strategy

    def getOppStrategy(self) -> list[float]:
        normalizingSum: float = 0
        for i in range(0, self.numberOfActions):
            if (self.oppRegretSum[i] > 0):
                self.oppStrategy[i] = self.oppRegretSum[i]
            else:
                self.oppStrategy[i] = 0
            normalizingSum += self.oppStrategy[i]
        for i in range(0, self.numberOfActions):
            if (normalizingSum > 0):
                self.oppStrategy[i] /= normalizingSum
            else:
                self.oppStrategy[i] = 1 / self.numberOfActions
            self.oppStrategySum[i] += self.oppStrategy[i]
        return self.oppStrategy

    def getAction(self, myStrategy: list[float]) -> int:
        randomNum: float = random.uniform(0, 1)
        i: int = 0
        cumulativeProbability: float = 0
        while(i < (self.numberOfActions - 1)):
            cumulativeProbability += myStrategy[i]
            if (randomNum < cumulativeProbability):
                break
            i += 1
        return i


    # TODO: Write it my own way
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
        
        myActionUtility: list[float] = [0] * self.numberOfActions
        oppActionUtility: list[float] = [0] * self.numberOfActions

        for i in range(0, iterations):
            myStrategy: list[float] = self.getStrategy()
            oppStrategy: list[float] = self.getOppStrategy()
            
            myAction: int = self.getAction(myStrategy)
            oppAction: int = self.getAction(oppStrategy)
            # myAction: int = get_row_best_response(matrix, np.array(oppStrategy))
            # oppAction: int = get_row_best_response(oppMatrix, np.array(myStrategy))
            
            for i in range(0, self.numberOfActions):
                myActionUtility[i] = self.matrix[i][oppAction]
                oppActionUtility[i] = self.oppMatrix[i][myAction]
            
            for i in range(0, self.numberOfActions):
                self.regretSum[i] += myActionUtility[i] - myActionUtility[myAction]
                self.oppRegretSum[i] += oppActionUtility[i] - oppActionUtility[oppAction]

            exploitabilities.append(self.get_exploitability(self.matrix, np.array(self.getMyAverageStrategy()), np.array(self.getOppAverageStrategy())))
        return exploitabilities


    def getMyAverageStrategy(self) -> list[float]:
        averageStrategy: list[float] = [0] * self.numberOfActions
        normalizingSum: float = 0
        for i in range(0, self.numberOfActions):
            normalizingSum += self.strategySum[i]
        for i in range(0, self.numberOfActions):
            if (normalizingSum > 0):
                averageStrategy[i] = self.strategySum[i] / normalizingSum
            else:
                averageStrategy[i] = 1 / self.numberOfActions
        return averageStrategy

    def getOppAverageStrategy(self) -> list[float]:
        averageStrategy: list[float] = [0] * self.numberOfActions
        normalizingSum: float = 0
        for i in range(0, self.numberOfActions):
            normalizingSum += self.oppStrategySum[i]
        for i in range(0, self.numberOfActions):
            if (normalizingSum > 0):
                averageStrategy[i] = self.oppStrategySum[i] / normalizingSum
            else:
                averageStrategy[i] = 1 / self.numberOfActions
        return averageStrategy


rm_exploitabilitiesz = []
for t in tqdm(range(8)):
    # Initialize number of actions
    finder = Finder(100)

    # Generate random matrix
    finder.start()

    # Train!
    rm_exploitabilitiesz.append(finder.train(1000))

plt.plot([sum(x)/len(x) for x in zip(*rm_exploitabilitiesz)])
plt.yscale('log')
plt.xscale('log')
plt.title('RM')
plt.show()