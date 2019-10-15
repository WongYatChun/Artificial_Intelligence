#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying 
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
import util 
import sys
import random
import time
from optparse import OptionParser

class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """
    def __init__(self):
        """
          Represent 3 boards with lists of boolean value 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]: 
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)

class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        self.fp_1 = [[True, False, False, False, False, False, False, False, False],
                     [False, True, False, False, False, False, False, False, False],
                     [True, True, True, False, False, False, False, False, False],
                     [True, False, False, False, True, False, False, False, True],
                     [True, False, False, False, False, True, False, True, False],
                     [False, True, False, False, True, False, False, True, False],
                     [True, True, True, True, False, False, False, False, False],
                     [True, True, True, False, True, False, False, False, False],
                     [True, True, True, False, False, False, True, False, False],
                     [True, True, True, False, False, False, False, True, False],
                     [True, True, False, False, True, False, False, True, False],
                     [True, True, False, False, True, False, False, False, True],
                     [True, False, True, False, True, False, True, False, False]
                    ]
        
        self.fp_a = [[True, False, False, False, False, False, False, False, True],
                     [False, True, False, True, False, False, False, False , False],
                     [False, True, False, False, False, False, False, True , False],
                     [True, True, False, False, False, False, True, False, False],
                     [True, False, True, False, True, False, False, False, False],
                     [True, False, True, False, False, False, False, True, False],
                     [True, False, False, False, True, True, False, False, False],
                     [True, True, False, True, True, False, False, False, False],
                     [True, True, False, True, False, True, False, False, False],
                     [True, True, False, True, False, False, False, False, True],
                     [True, True, False, False, False, False, False, True, True],
                     [True, False, True, False, False, False, True, False, True],
                     [False, True, False, True, False, True, False, True, False],
                     [True, True, False, False, True, True, True, False, False],
                     [True, True, False, False, False, True, True, True, False],
                     [True, True, False, False, False, True, True, False, True],
                     [True, True, False, True, False, True, False, True, True]]

        self.fp_b = [[True, False, True, False, False, False, False, False, False],
                     [True, False, False, False, True, False, False, False, False],
                     [True, False, False, False, False, True, False, False, False],
                     [False, True, False, False, True, False, False, False, False],
                     [True, True, False, True, False, False, False, False, False],
                     [False, True, False, True, False, True, False, False, False],
                     [True, True, False, False, True, True, False, False, False],
                     [True, True, False, False, True, False, True, False, False],
                     [True, True, False, False, False, True, True, False, False],
                     [True, True, False, False, False, False, True, True, False],
                     [True, True, False, False, False, False, True, False, True],
                     [True, False, True, False, True, False, False, True, False],
                     [True, False, False, False, True, True, False, True, False],
                     [True, True, False, True, False, True, False, True, False],
                     [True, True, False, True, False, True, False, False, True]]
        
        self.fp_d = [[True, True, False, False, False, True, False, False, False],
                     [True, True, False, False, False, False, False, True, False],
                     [True, True, False, False, False, False, False, False, True]]

        self.fp_ab = [[True, True, False, False, True, False, False, False, False],
                      [True, False, True, False, False, False, True, False, False],
                      [False, True, False, True, True, False, False, False, False],
                      [True, True, False, False, False, True, False, True, False],
                      [True, True, False, False, False, True, False, False, True]]
        
        self.fp_ad = [[True, True, False, False, False, False, False, False, False]]

        
        self.fp_c2 = [[False, False, False, False, True, False, False, False, False]]
        
    
        self.fp = self.fp_1 + self.fp_a + self.fp_ab + self.fp_ad + self.fp_b + self.fp_c2 + self.fp_d

        self.fp_1_all = self.transform(self.fp_1)
        self.fp_a_all = self.transform(self.fp_a)
        self.fp_b_all = self.transform(self.fp_b)
        self.fp_d_all = self.transform(self.fp_d)
        self.fp_ab_all = self.transform(self.fp_ab)
        self.fp_ad_all = self.transform(self.fp_ad)
        self.fp_c2_all = self.transform(self.fp_c2)

    
    def transform(self, boards):
        
        
        # print(boards)
        all_boards = boards.copy()
        # print(all_boards)
        for board in boards:
            tmp = board.copy()
            for _ in range(3):
                tmp = self.rot90(tmp)
                # print(tmp)
                all_boards.append(tmp)
                # print(all_boards)
                
            all_boards.append(self.v_mirror(board)) 
            all_boards.append(self.h_mirror(board))
            all_boards.append(self.diag1_mirror(board))
            all_boards.append(self.diag2_mirror(board))
            # print(all_boards)

        return all_boards
            
    def rot90(self, board):
        tmp = board.copy()
        tmp[0] = board[6]
        tmp[1] = board[3]
        tmp[2] = board[0]
        tmp[3] = board[7]
        tmp[5] = board[1]
        tmp[6] = board[8]
        tmp[7] = board[5]
        tmp[8] = board[2]

        return tmp


    def v_mirror(self, board):
        temp = board.copy()
        temp[0] = board[2]
        temp[2] = board[0]
        temp[3] = board[5]
        temp[5] = board[3]
        temp[6] = board[8]
        temp[8] = board[6]
        return temp
        

    def h_mirror(self, board):
        temp = board.copy()
        temp[0] = board[6]
        temp[6] = board[0]
        temp[1] = board[7]
        temp[7] = board[1]
        temp[2] = board[8]
        temp[8] = board[2]
        return temp

    def diag1_mirror(self, board):
        temp = board.copy()
        temp[1] = board[3]
        temp[3] = board[1]
        temp[2] = board[6]
        temp[6] = board[2]
        temp[7] = board[5]
        temp[5] = board[7]
        return temp
    
    def diag2_mirror(self, board):
        temp = board.copy()
        temp[0] = board[8]
        temp[8] = board[0]
        temp[1] = board[5]
        temp[5] = board[1]
        temp[7] = board[3]
        temp[3] = board[7]
        return temp

    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

    def get_fp(self, board):


        if sum(board) == 0:
            return {'c':1}
        
        elif self.deadTest(board):
            return {'1':1}

        elif board in self.fp_1_all:
            return {'1':1}
        
        elif board in self.fp_a_all:
            return {'a':1}

        elif board in self.fp_b_all:
            return {'b':1}
        
        elif board in self.fp_d_all:
            return {'d':1}
        
        elif board in self.fp_ab_all:
            return {'a':1,'b':1}

        elif board in self.fp_ad_all:
            return {'a':1,'d':1}

        elif board in self.fp_c2_all:
            return {'c':2,}
        else:

            return False
        
    def fpMath(self, boards):
        """
        This section is inspired by kelvin0815
        https://github.com/kelvin0815/notakto/blob/master/solveTicTacToe.py
        """
        fps = [self.get_fp(board) for board in boards]

        result = {}
        # print(fps)
        for fp in fps:
            # print(fp)
            for sym in fp:
                if sym not in result.keys():
                    result[sym] = fp[sym]
                else:
                    result[sym] += fp[sym]

        if '1' in result.keys():
            if result.keys() == ['1']: return {'1':1}
            else: del result['1']
        
        return result  
        

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])

class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the 
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        


    def getValue(self, gameState, gameRules):
        
        MAX = 999
        
        winners = [{"a":1}, {"b":2}, {"c":2}, {"b":1, "c":1}]

        result = gameRules.fpMath(gameState.boards)

        if result in winners:
            if result == {"c":2}:return MAX + MAX
            return MAX

        return 0


    def getAction(self, gameState, gameRules):
        "*** YOUR CODE HERE ***"
        maxValue, maxAction = float("-inf"), gameState.getLegalActions(gameRules)[0]
        initial_depth = 0
        agentIndex = 0
        for action in gameState.getLegalActions(gameRules):
          # same logic as getMax, but we need to get the action this time
            nextState = gameState.generateSuccessor(action)
            nextValue = self.getValue(nextState, gameRules)
            if nextValue > maxValue: 
                maxValue, maxAction = nextValue, action
                
        
        return maxAction


class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """
    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)


class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """
    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action 

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 30 

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    #random.seed(1)  
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
