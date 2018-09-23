# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
    

    open = util.Stack()
    path = [problem.getStartState()]
    
    open.push((problem.getStartState(),[],path))
    
    visited = []
    visited.append(problem.getStartState())
    
    while not open.isEmpty():
        
        
        state,actions,path = open.pop()
        
        
        if(problem.isGoalState(state)):
            return actions 
        
        for succ in problem.getSuccessors(state):
            
            n = succ[0]
            n_dir = succ[1]
            
            if not n in path:
                path2 = path + [n]
                open.push((n, actions+[n_dir],path2))
                visited.append(n)
                
                
                
    return False
    
    util.raiseNotDefined()
    
   
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    open = util.Queue()
    open.push((problem.getStartState(),[]))
    #actions = []
    visited = []
    visited.append(problem.getStartState())
    
    while not open.isEmpty():
        
        #n = open.pop()
        state,actions = open.pop()
        
        
        if(problem.isGoalState(state)):
            return actions 
        
        for succ in problem.getSuccessors(state):
            
            n = succ[0]
            n_dir = succ[1]
            
            if n not in visited:
                
                open.push((n,actions+[n_dir]))
                #actions.append(m_dir)
                visited.append(n)
                
                
                
    return False
    
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    open = util.PriorityQueue()
    open.push((problem.getStartState(),[]),0)
    
    seen = {problem.getStartState():0}
    
    #visited = []
    #visited.append(problem.getStartState())
    #state = problem.getStartState()
    
    while not open.isEmpty():
            
        state,actions = open.pop()
        
        if problem.getCostOfActions(actions) <= seen[state]:
            if(problem.isGoalState(state)):
                return actions 
            
            for succ in problem.getSuccessors(state):
                if not succ[0] in seen or problem.getCostOfActions(actions +[succ[1]]) < seen[succ[0]]:
                    n = succ[0]
                    n_dir = succ[1]
                    
                    dir = actions+[n_dir]
                    priority = problem.getCostOfActions(dir)
                    open.push((n,actions+[n_dir]),priority)
                    seen[n] = problem.getCostOfActions(actions+[n_dir])
        
    return False
   
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    #f(n) = cost + heuristic
    
    open = util.PriorityQueue()
    open.push((problem.getStartState(),[]),0)
    
    seen = {problem.getStartState():0}
    
    
    
    while not open.isEmpty():
            
        state,actions = open.pop()
        #print state
        
        if problem.getCostOfActions(actions) <= seen[state]:
            
            #print seen[state]
            if(problem.isGoalState(state)):
                #print actions
                return actions 
            
            for succ in problem.getSuccessors(state):
                n = succ[0]
                n_dir = succ[1]
                    
                dir = actions+[n_dir]
                priority = problem.getCostOfActions(dir) + heuristic(n,problem)
                #print priority
                
                if not succ[0] in seen or priority < seen[succ[0]]:
                    
                   
                    
                    n = succ[0]
                    
                    n_dir = succ[1]
                    #print n
                    # print seen[succ[0]]
                     
                    dir = actions+[n_dir]
                    priority = problem.getCostOfActions(dir) + heuristic(n,problem)
                    open.push((n,actions+[n_dir]),priority)
                    seen[n] = priority
                    #print seen[n]
        
    return False
   
    util.raiseNotDefined()

    
    

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
