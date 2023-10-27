import random

# Make a function that makes random 2-player zero-sum matrix games, or make some 2-player zero-sum matrix games like rock-paper-scissors.

def create(strategiesForOne: int, strategiesForTwo: int, myBound: int) -> list[tuple]:
    # Payoff Matrix
    matrix = [[0] * strategiesForTwo for _ in range(strategiesForOne)]

    # Populating the game
    for playerOneStrategy in range(0, strategiesForOne):
        for playerTwoStrategy in range(0, strategiesForTwo):
            matrix[playerOneStrategy][playerTwoStrategy] = random.randint(-1 * myBound, myBound)

    return matrix

# Printing for debugging purposes
# matrix = create(5, 5, 5)
# print(matrix)

# Implement a regret matching function that takes in a matrix game and outputs an approximated Nash equilibrium strategy profile. 
# (Both Players use regret matching)
# I am the row player; Opponent is the column player
# Three actions , Bounded by three

# Our Payoff Matrix
matrix = create(3, 3, 3)
print(matrix)
oppMatrix = [[j*-1 for j in i] for i in matrix]
print(oppMatrix)

# Definitions
numberOfActions: int = 3
regretSum: list[float] = [0] * numberOfActions
strategy: list[float] = [0] * numberOfActions
strategySum: list[float] = [0] * numberOfActions
oppRegretSum: list[float] = [0] * numberOfActions
oppStrategy: list[float] = [0] * numberOfActions
oppStrategySum: list[float] = [0] * numberOfActions

# Get current mixed strategy through regret-matching
def getStrategy() -> list[float]:
    global strategySum
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

def train(iterations: int):
    global regretSum
    global oppRegretSum
    
    myActionUtility: list[float] = [0] * numberOfActions
    oppActionUtility: list[float] = [0] * numberOfActions

    for i in range(0, iterations):
        myAction: int = getAction(getStrategy())
        oppAction: int = getAction(getOppStrategy())

        for i in range(0, numberOfActions):
            myActionUtility[i] = matrix[i][oppAction]
            oppActionUtility[i] = oppMatrix[myAction][i]
        
        for i in range(0, numberOfActions):
            regretSum[i] += myActionUtility[i] - myActionUtility[myAction]
            oppRegretSum[i] += oppActionUtility[i] - oppActionUtility[oppAction]


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

train(100)
print(getMyAverageStrategy())
print(getOppAverageStrategy())