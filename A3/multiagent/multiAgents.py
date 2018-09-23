# multiAgents.py
# --------------
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostPositions()
        #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        
        foodWeight = 10
        GhostWeight = 10
        
        newFood = newFood.asList()
        
        score = successorGameState.getScore()
       
        food = [manhattanDistance(newPos, food) for food in newFood]
        if len(food) != 0:
            score += foodWeight/(min(food))
            
        
        ghost = newGhostStates[0]
         
        ghostd = manhattanDistance(ghost,newPos)
        
        if ghostd > 0:
            score -= GhostWeight/ghostd

        
        return score
        
        

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
        """
      
        
        def minValue(state,depth, agent, ghosts):
            minval = 100000
            if state.isWin() or state.isLose() or depth ==0:
                return self.evaluationFunction(state)
            
            if agent == ghosts:
                actions = state.getLegalActions(agent)
                for action in actions:
                    minval = min(minval, maxValue(state.generateSuccessor(agent, action), depth-1, ghosts))
            
            else:
                
                actions = state.getLegalActions(agent)
                for action in actions:
                    minval =  min(minval, minValue(state.generateSuccessor(agent,action), depth, agent +1, ghosts))
                    
            return minval


        def maxValue(state,depth,ghosts):
            maxval = -1000000
            if state.isWin() or state.isLose() or depth ==0:
                return self.evaluationFunction(state)
            
            else:
                actions = state.getLegalActions()
                
                for action in actions:
                    maxval = max(maxval,minValue(state.generateSuccessor(0,action),depth,1,numghosts))
            return maxval

        legalActions = gameState.getLegalActions()
        best = legalActions[0]
        numghosts = gameState.getNumAgents() -1
        
        score = -(float("inf"))
        for action in legalActions:
            
            nextState = gameState.generateSuccessor(0, action)
            prevscore = score
            score = max(score, minValue(nextState, self.depth, 1, numghosts))
            if score > prevscore:
                bestaction = action
        return bestaction
        
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        ghosts = gameState.getNumAgents() -1
        "*** YOUR CODE HERE ***"
        def minValue(state,depth, agent, ghosts, alpha, beta):
            minval = 100000
            if state.isWin() or state.isLose() or depth ==0:
                return self.evaluationFunction(state)
            
            if agent == ghosts:
                actions = state.getLegalActions(agent)
                for action in actions:
                    minval = min(minval, maxValue(state.generateSuccessor(agent, action), depth-1, ghosts, alpha, beta))
                    if minval <= alpha:
                        return minval
                    beta = min(beta,minval)
            
            else:
                
                actions = state.getLegalActions(agent)
                for action in actions:
                    minval =  min(minval, minValue(state.generateSuccessor(agent,action), depth, agent +1, ghosts, alpha, beta))
                    if minval <= alpha:
                        return minval
                    beta = min(beta,minval)
            
                    
            return minval


        def maxValue(state,depth,ghosts, alpha, beta):
            maxval = -float("inf")
            if state.isWin() or state.isLose() or depth ==0:
                return self.evaluationFunction(state)
            
            else:
                actions = state.getLegalActions()
                
                for action in actions:
                    maxval = max(maxval,minValue(state.generateSuccessor(0,action),depth,1,ghosts,alpha,beta))
                    if beta <= maxval:
                        return maxval
                    alpha = max(alpha,maxval)
            return maxval

        legalActions = gameState.getLegalActions()
        bestaction = legalActions[0]
        score = -(float("inf"))
        alpha = -(float("inf"))
        beta = float("inf")
        
        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            prevscore = score
            score = max(score, minValue(nextState, self.depth, 1, ghosts, alpha, beta))
            
            if score > prevscore:
                bestaction = action
            if score >= beta:
                return bestaction
            alpha = max(alpha, score)
        return bestaction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
     
     
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        
        def expectedvalue(state, agent, depth):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            ghosts = state.getNumAgents() - 1
            actions = state.getLegalActions(agent)
            numactions = len(actions)
            sum = 0
            for action in actions:
                nextState = state.generateSuccessor(agent, action)
                if (agent == ghosts):
                    sum += maxvalue(nextState, depth - 1)
                else:
                    sum += expectedvalue(nextState, agent + 1, depth)
            return sum / numactions
        
        
        def maxvalue(state, depth):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
                
            actions = state.getLegalActions(0)
            bestAction = Directions.STOP
            score = -(float("inf"))
            
            for action in actions:
                prevscore = score
                nextState = state.generateSuccessor(0, action)
                score = max(score, expectedvalue(nextState, 1, depth))
            return score
            
            
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(state)
            
        actions = gameState.getLegalActions(0)
        bestaction = Directions.STOP
        score = -(float("inf"))
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            prevscore = score
            score = max(score, expectedvalue(nextState, 1, self.depth))
            if score > prevscore:
                bestaction = action
        return bestaction
        
        
        
      
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    #find food
    #avoid ghosts
    #get pellets
    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostPositions()
        
    foodWeight = 10
    GhostWeight = 10
        
    newFood = newFood.asList()
        
    score = currentGameState.getScore()
       
    food = [manhattanDistance(newPos, food) for food in newFood]
    if len(food) != 0:
        score += 1.5* foodWeight/(min(food))
            
        
    ghost = newGhostStates[0]
         
    ghostd = manhattanDistance(ghost,newPos)
        
    if ghostd > 0:
        score -= 2 * GhostWeight/ghostd
    
    capsulelocations = currentGameState.getCapsules()
    score -= 3*len(capsulelocations)
    score -= 4*len(newFood)

        
    return score
    
# Abbreviation
better = betterEvaluationFunction

