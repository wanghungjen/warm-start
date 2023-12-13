from RegretMatching import create
from RegretMatching import Finder
import numpy as np
import matplotlib.pyplot as plt

def get_row_best_response(matrix, col_strategy):
        # Given a matrix game and col_strategy, the best response is the row which maximizes expected payoff
    return (matrix @ col_strategy).argmax()

def DOadd(indexes: list, response: int):
    if response in indexes:
        return indexes
    else:
        indexes.append(response)
        indexes.sort()
        return indexes

# Initialize 100 x 100 matrix (& opp.matrix)
gameSize = 100
game = create(gameSize, gameSize)

myMatrix = game
oppMatrix = -game.T

# Initialize all strategies for both players
myMixedStrategy = np.array([0.0] * gameSize)
oppMixedStrategy = np.array([0.0] * gameSize)

# Choose (0,0) as starting point and update actions
myCurBestIndex = 0
oppCurBestIndex = 0
myMixedStrategy[myCurBestIndex] = 1
oppMixedStrategy[oppCurBestIndex] = 1

# Initialize indexes for both players
myIndexes = [0]
oppIndexes = [0]

# Initializing exploitabilities
exploitabilities = []

# Loop Starts

while(True):
    print("ITERATION START\n")

    # Determine "best response" indexes for both player 1 and player 2
    myBestResponse = get_row_best_response(myMatrix, oppMixedStrategy)
    oppBestResponse = get_row_best_response(oppMatrix, myMixedStrategy)

    # print("myBestReponse: ", myBestResponse)
    # print("oppBestReponse: ", oppBestResponse)
    # print("myIndexes: ", myIndexes)
    # print("oppIndexes: ", oppIndexes)

    # Exit Condition
    if (myBestResponse in myIndexes) and (oppBestResponse in oppIndexes):
        break

    DOadd(myIndexes, myBestResponse)
    DOadd(oppIndexes, oppBestResponse)

    # Create minigame
    # print("myIndexes: ", myIndexes)
    # print("oppIndexes: ", oppIndexes)
    minigame = [[0] * len(oppIndexes) for _ in range(len(myIndexes))]
    # print("minigame: ", minigame)

    cur_x = 0
    cur_y = 0
    for x in range(0, gameSize):
        if x in myIndexes:
            for y in range(0, gameSize):
                if y in oppIndexes:
                    # print("cur_x: ", cur_y)
                    # print("cur_y: ", cur_y)
                    minigame[cur_x][cur_y] = game[x][y]
                    cur_y += 1
            cur_x += 1
            cur_y = 0
    # print("game: ", game)
    # print("minigame: ", minigame)

    # Implement Regret Matching & Find New Mixed Strategies
    finder = Finder(np.array(minigame))
    new_exploitabilities = finder.train(10000)
    exploitabilities = np.concatenate((exploitabilities, new_exploitabilities))
    myNewMixedStrategy = finder.getMyAverageStrategy()
    oppNewMixedStrategy = finder.getOppAverageStrategy()
    # print("myNewMixedStrategy: ", myNewMixedStrategy)
    # print("oppNewMixedStrategy: ", oppNewMixedStrategy)

    my_cur_index = 0
    opp_cur_index = 0
    for index in range(0, gameSize):
        if index in myIndexes:
            myMixedStrategy[index] = myNewMixedStrategy[my_cur_index]
            my_cur_index += 1
        if index in oppIndexes:
            oppMixedStrategy[index] = oppNewMixedStrategy[opp_cur_index]
            opp_cur_index += 1

    # print(myMixedStrategy)
    # print(oppMixedStrategy)

print("My Nash Equilibrium: ", myMixedStrategy)
print("Opp Nash Equilibrium: ", oppMixedStrategy)
# print(exploitabilities)

plt.plot(exploitabilities)
# plt.yscale('log')
# plt.xscale('log')
plt.title('DO')
plt.show()