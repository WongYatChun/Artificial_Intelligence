"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]
            

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    """
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    
    stack = util.Stack()
    stack.push(state)
    queue2 = util.Queue()

    visited = set(state)
    parent = dict()
    

    while not stack.isEmpty():
        s = stack.pop()
        visited.add(s)

        if problem.isGoalState(s):
            goal = s
            
            while parent[goal][0] != state:
                
                queue2.push(parent[goal][1])
                goal = parent[goal][0]
                
            queue2.push(parent[goal][1])
            return queue2.list   


        for next_state in problem.getSuccessors(s):
            
            if next_state[0] not in visited:
                stack.push(next_state[0])
                
                parent[next_state[0]] = (s, next_state[1])
    return list

    

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    state = problem.getStartState()

    queue = util.Queue()
    queue.push(state)
    queue2 = util.Queue()

    visited = set(state)
    parent = dict()
    

    while not queue.isEmpty():
        s = queue.pop()

        if problem.isGoalState(s):
            goal = s
            
            while parent[goal][0] != state:
                
                queue2.push(parent[goal][1])
                goal = parent[goal][0]
                
            queue2.push(parent[goal][1])
            return queue2.list   


        for next_state in problem.getSuccessors(s):
            
            if next_state[0] not in visited:
                queue.push(next_state[0])
                visited.add(next_state[0])
                parent[next_state[0]] = (s, next_state[1])
    return list


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"

    state = problem.getStartState()
    cost = dict()
    cost[state] = 0
    pqueue = util.PriorityQueue()
    pqueue.push(state, cost[state])
    queue2 = util.Queue()
    parent = dict()
    visited = set()
       

    while not pqueue.isEmpty():
        s = pqueue.pop()
        if s not in visited:
            # print(s)
            visited.add(s)
            # print(visited)

            if problem.isGoalState(s):
                goal = s
                
                while parent[goal][0] != state:
                    
                    queue2.push(parent[goal][1])
                    goal = parent[goal][0]
                    
                queue2.push(parent[goal][1])
                return queue2.list   


            for next_state in problem.getSuccessors(s):
                if next_state[0] not in visited:
                    if cost.get(next_state[0], False) == False or cost[next_state[0]] > cost[s]+next_state[2]:
                        # print("Has not visited: ",next_state[0])
                        # print("Cost if available: ",cost.get(next_state[0], True))
                        cost[next_state[0]] = cost[s]+next_state[2]
                        pqueue.push(next_state[0], cost[next_state[0]])
                        
                        parent[next_state[0]] = (s, next_state[1])
                    
                            
    return list()
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    bCost = dict()
    bCost[state] = 0
    aCost = dict()
    aCost[state] = 0
    pqueue = util.PriorityQueue()
    pqueue.push(state, aCost[state])
    queue2 = util.Queue()
    parent = dict()
    visited = set()
       

    while not pqueue.isEmpty():
        s = pqueue.pop()
        if s not in visited:
            # print(s)
            visited.add(s)
            # print(visited)

            if problem.isGoalState(s):
                goal = s
                
                while parent[goal][0] != state:
                    
                    queue2.push(parent[goal][1])
                    goal = parent[goal][0]
                    
                queue2.push(parent[goal][1])
                return queue2.list   


            for next_state in problem.getSuccessors(s):
                if next_state[0] not in visited:
                    
                    if aCost.get(next_state[0], False) == False or aCost[next_state[0]] > bCost[s] + next_state[2] + heuristic(next_state[0], problem):
                        # print("Has not visited: ",next_state[0]
                        # print("Cost if available: ",cost.get(next_state[0], True))
                        bCost[next_state[0]] = bCost[s]+next_state[2]
                        aCost[next_state[0]] = bCost[next_state[0]] + heuristic(next_state[0], problem)
                        pqueue.push(next_state[0], aCost[next_state[0]])
                        
                        parent[next_state[0]] = (s, next_state[1])
                    
                            
    return list()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
