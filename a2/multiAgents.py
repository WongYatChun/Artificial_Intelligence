from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print(prevFood)
        # print(successorGameState)
        MAX = 999999
        # print(newPos)
        food_coord = [i for i in newFood.asList()]
        if food_coord:
          min_dist_food = min([manhattanDistance(newPos, i) for i in food_coord])
        else:
          return MAX
        min_dist_ghost = min([manhattanDistance(newPos, i.getPosition()) for i in newGhostStates])
        

        if min_dist_food: 
          if min_dist_ghost > 2 or (min(newScaredTimes) > 0 and len(newScaredTimes) == 1):
            return successorGameState.getScore() + 10 / (min_dist_food) + 0.1 * sum(newScaredTimes)
          else:
            return successorGameState.getScore() + min_dist_ghost
        
        return successorGameState.getScore()
        

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """


    def getMax(self, gameState, currentDepth): # only call for the pacman
        values = [self.getValue(gameState.generateSuccessor(self.index, action), currentDepth, 1) for action in gameState.getLegalActions(self.index)]
        return max(values)

    def getMin(self, gameState, currentDepth, agentIndex): # only call for the ghost
        if agentIndex == gameState.getNumAgents()-1: # if this is the last agent, go deeper
          values = [self.getValue(gameState.generateSuccessor(agentIndex, action), currentDepth+1, self.index) for action in gameState.getLegalActions(agentIndex)]
        else: # else, getValue of the next agent
          values = [self.getValue(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1) for action in gameState.getLegalActions(agentIndex)]
        return min(values)

    def getValue(self, gameState, currentDepth, agentIndex):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose(): # leaf
            return self.evaluationFunction(gameState)
        elif agentIndex == self.index:# if the pacman
            return self.getMax(gameState,currentDepth) #getMax
        else: # if ghost
            return self.getMin(gameState,currentDepth,agentIndex) # getMin

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        maxValue, maxAction = float("-inf"), Directions.STOP
        initial_depth = 0
        for action in gameState.getLegalActions(self.index):
          # same logic as getMax, but we need to get the action this time
            nextState = gameState.generateSuccessor(self.index, action)
            nextValue = self.getValue(nextState, initial_depth, self.index+1)
            if nextValue > maxValue: maxValue, maxAction = nextValue, action
        return maxAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def getMax(self, gameState, currentDepth, currentMax, currentMin): # only call for the pacman
        v = float("-inf")
         
        for action in gameState.getLegalActions(self.index):
            v = max(v, self.getValue(gameState.generateSuccessor(self.index, action), currentDepth, 1, currentMax, currentMin))
            # currentMax = max(currentMax, v)
            if v > currentMin: return v
            currentMax = max(currentMax, v)
            
        return v

    def getMin(self, gameState, currentDepth, agentIndex,currentMax, currentMin): # only call for the ghost
        v = float("inf")
        if agentIndex == gameState.getNumAgents()-1: # if this is the last agent, go deeper
            for action in gameState.getLegalActions(agentIndex):
                v = min(v, self.getValue(gameState.generateSuccessor(agentIndex, action), currentDepth+1, self.index, currentMax, currentMin))
                # currentMin = min(currentMin, v)
                if v < currentMax: return v
                currentMin = min(currentMin, v)
                
        
        else: # else, getValue of the next agent
            for action in gameState.getLegalActions(agentIndex):
                v = min(v, self.getValue(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1, currentMax, currentMin))
                # currentMin = min(currentMin, v)
                if v < currentMax: return v
                currentMin = min(currentMin, v)
        return v

    def getValue(self, gameState, currentDepth, agentIndex,currentMax, currentMin):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose(): # leaf
            return self.evaluationFunction(gameState)
        elif agentIndex == self.index:# if the pacman
            return self.getMax(gameState,currentDepth, currentMax, currentMin) #getMax
        else: # if ghost
            return self.getMin(gameState,currentDepth,agentIndex, currentMax, currentMin) # getMin


    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        maxValue, maxAction = float("-inf"), Directions.STOP
        currentMax, currentMin = float('-inf'),  float('inf')
        initial_depth = 0
        for action in gameState.getLegalActions(self.index):
          # same logic as getMax, but we need to get the action this time
            nextState = gameState.generateSuccessor(self.index, action)
            nextValue = self.getValue(nextState, initial_depth, self.index+1, currentMax, currentMin)
            if nextValue > maxValue: maxValue, maxAction = nextValue, action
            currentMax = max(currentMax, maxValue)
        # print(gameState.getLegalActions(self.index))
        # print(maxAction)
        return maxAction
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    
    def getMax(self, gameState, currentDepth): # only call for the pacman
        values = [self.getValue(gameState.generateSuccessor(self.index, action), currentDepth, 1) for action in gameState.getLegalActions(self.index)]
        return max(values)

    def getExp(self, gameState, currentDepth, agentIndex): # only call for the ghost
        if agentIndex == gameState.getNumAgents()-1: # if this is the last agent, go deeper
          values = [self.getValue(gameState.generateSuccessor(agentIndex, action), currentDepth+1, self.index) for action in gameState.getLegalActions(agentIndex)]
        else: # else, getValue of the next agent
          values = [self.getValue(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1) for action in gameState.getLegalActions(agentIndex)]
        return sum(values) / len(values)

    def getValue(self, gameState, currentDepth, agentIndex):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose(): # leaf
            return self.evaluationFunction(gameState)
        elif agentIndex == self.index:# if the pacman
            return self.getMax(gameState,currentDepth) #getMax
        else: # if ghost
            return self.getExp(gameState,currentDepth,agentIndex) # getMin

    def getAction(self, gameState):
        "*** YOUR CODE HERE ***"
        maxValue, maxAction = float("-inf"), Directions.STOP
        initial_depth = 0
        for action in gameState.getLegalActions(self.index):
          # same logic as getMax, but we need to get the action this time
            nextState = gameState.generateSuccessor(self.index, action)
            nextValue = self.getValue(nextState, initial_depth, self.index+1)
            if nextValue > maxValue: maxValue, maxAction = nextValue, action
        return maxAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      Similar to my solution in Q1
      if the ghost is away from the pacmen
          It is a weighted combination of (the score of the state) + (1 / min. dist to food) + (sum of scared time)
      else:
          it is a weighted combination of (the score of the state) + (dist to the nearest ghost) + (sum of scared time)

      

    """
    "*** YOUR CODE HERE ***"
    prevFood = currentGameState.getFood()
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    MAX = 999999
    
    food_coord = [i for i in newFood.asList()]
    if food_coord:
      min_dist_food = min([manhattanDistance(newPos, i) for i in food_coord])
    else:
      return MAX
    min_dist_ghost = min([manhattanDistance(newPos, i.getPosition()) for i in newGhostStates])
    

    if min_dist_food: 
      if min_dist_ghost > 2 or (min(newScaredTimes) > 0 and len(newScaredTimes) == 1):
        return currentGameState.getScore() + 35 / (min_dist_food) + 0.1 * sum(newScaredTimes)
      else:
        return currentGameState.getScore() + min_dist_ghost + sum(newScaredTimes)

    return currentGameState.getScore()


# Abbreviation
better = betterEvaluationFunction

