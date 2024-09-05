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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        currentGameState = currentGameState.getScore()
        nextScore = successorGameState.getScore()
        ghostLocations = successorGameState.getGhostPositions()


        foodScore = 0
        ghostScore = 0

        food_distances = [manhattanDistance(newPos, fs) for fs in newFood.asList()]
        foodScore -= 4 * len(food_distances)
        if food_distances:
            foodScore -= 0.2 * min(food_distances)
        ghostLocs = [manhattanDistance(newPos, fs) for fs in ghostLocations]
        min_ghost_dist = min(ghostLocs)
        if min_ghost_dist == 0:
            return -10000
        if newScaredTimes[ghostLocs.index(min_ghost_dist)] < min_ghost_dist:
            if min_ghost_dist < 4:
                return -(100/(min_ghost_dist + 1))
        if newScaredTimes[ghostLocs.index(min_ghost_dist)] > min_ghost_dist:
            ghostScore += (10/(min_ghost_dist + 1)) * 10
        
        return nextScore + foodScore + ghostScore

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimaxrec(gameState, 0, 0)[1]

    def minimaxrec(self, gameState, agent, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState), None

        numAgents = gameState.getNumAgents()
        if agent == 0: 
            value = float("-inf")
            bestAction = None
            for action in gameState.getLegalActions(agent):
                successorState = gameState.generateSuccessor(agent, action)
                score, _ = self.minimaxrec(successorState, (agent + 1) % numAgents, depth + 1)
                if score > value:
                    value, bestAction = score, action
            return value, bestAction
        else: 
            value = float("inf")
            bestAction = None
            for action in gameState.getLegalActions(agent):
                successorState = gameState.generateSuccessor(agent, action)
                score, _ = self.minimaxrec(successorState, (agent + 1) % numAgents, depth + 1)
                if score < value:
                    value, bestAction = score, action
            return value, bestAction
        

    # def pacActions(self, possibleGameStates):
    #     possiblePacActions = possibleGameStates.getLegalActions(0)
    #     possiblePacStates = []
    #     for action in possiblePacActions:
    #          possiblePacStates.append((possibleGameStates.generateSuccessor(0, action), action))
    #     return possiblePacStates
    
    # def ghostActions(self, possibleGameStates, index):
    #     tempGhostStates = []
    #     possibleGhostStates = []
    #     scores = []
    #     for gameState in possibleGameStates:
    #         tempGhostActions = gameState.getLegalActions(index)
    #         for action in tempGhostActions:
    #             tempGhostStates.append(gameState.generateSuccessor(index, action))
    #         for gameState in tempGhostStates:
    #             scores.append(gameState.getScore())
    #         possibleGhostStates.append(tempGhostActions[tempGhostActions.index(max(scores))])
    #     return possibleGhostStates

                             
            
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -float("inf")
        beta = float("inf")
        return self.alphabetarec(gameState, 0, 0, alpha, beta)[1]

    
    def alphabetarec(self, gameState, depth, agent, alpha, beta):
        numAgents = gameState.getNumAgents()
        newAgent = (agent + 1) % numAgents
        newDepth = depth + 1 if newAgent == 0 else depth

        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None

        if agent == 0:
            value = -float("inf")
            bestAction = None
            for action in gameState.getLegalActions(agent):
                newStates = gameState.generateSuccessor(agent, action)
                score, _ = self.alphabetarec(newStates, newDepth, newAgent, alpha, beta)
                if score > value:
                    value, bestAction = score, action
                if value > beta:
                    return value, bestAction
                alpha = max(alpha, value)
            return value, bestAction
                
        else:
            value = float("inf")
            bestAction = None
            for action in gameState.getLegalActions(agent):
                newStates = gameState.generateSuccessor(agent, action)
                score, _ = self.alphabetarec(newStates, newDepth, newAgent, alpha, beta)
                if score < value:
                    value, bestAction = score, action
                if value < alpha:
                    return value, bestAction
                beta = min(beta, value)
            return value, bestAction

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
        "*** YOUR CODE HERE ***"
        return self.expectirec(gameState, 0, 0)[1]

    def expectirec(self, gameState, agent, depth):
        numAgents = gameState.getNumAgents()
        newAgent = (agent + 1) % numAgents
        newDepth = depth + 1 if newAgent == 0 else depth

        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None

        allStates = gameState.getLegalActions(agent)
        if agent == 0: 
            value = float("-inf")
            bestAction = None
            for action in allStates:
                successorState = gameState.generateSuccessor(agent, action)
                score, _ = self.expectirec(successorState, newAgent, newDepth)
                if score > value:
                    value, bestAction = score, action
            return value, bestAction
        else: 
            totalValue = 0
            for action in allStates:
                successorState = gameState.generateSuccessor(agent, action)
                score, _ = self.expectirec(successorState, newAgent, newDepth)
                totalValue += score
            expValue = totalValue/len(allStates) if allStates else 0
            return expValue, None

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    return alphabetarec(currentGameState, 0, 0, -float("inf"), float("inf"))

    
def alphabetarec(gameState, depth, agent, alpha, beta):
    numAgents = gameState.getNumAgents()
    newAgent = (agent + 1) % numAgents
    newDepth = depth + 1 if newAgent == 0 else depth

    if gameState.isWin() or gameState.isLose() or depth == 2:
        return heuristicEvaluationFunction(gameState)

    if agent == 0:
        value = -float("inf")
        for action in gameState.getLegalActions(agent):
            newStates = gameState.generateSuccessor(agent, action)
            score = alphabetarec(newStates, newDepth, newAgent, alpha, beta)
            if score > value:
                value = score
            if value > beta:
                return value
            alpha = max(alpha, value)
        return value
                
    else:
        value = float("inf")
        for action in gameState.getLegalActions(agent):
            newStates = gameState.generateSuccessor(agent, action)
            score = alphabetarec(newStates, newDepth, newAgent, alpha, beta)
            if score < value:
                value = score
            if value < alpha:
                return value
            beta = min(beta, value)
        return value

def heuristicEvaluationFunction(currentGameState):
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    nextScore = currentGameState.getScore()
    ghostLocations = currentGameState.getGhostPositions()


    foodScore = 0
    ghostScore = 0

    food_distances = [manhattanDistance(newPos, fs) for fs in newFood.asList()]
    foodScore -= 4 * len(food_distances)
    if food_distances:
        foodScore -= 0.2 * min(food_distances)
    ghostLocs = [manhattanDistance(newPos, fs) for fs in ghostLocations]
    min_ghost_dist = min(ghostLocs)
    if min_ghost_dist == 0:
        return -10000
    if newScaredTimes[ghostLocs.index(min_ghost_dist)] < min_ghost_dist:
        if min_ghost_dist < 4:
            return -(100/(min_ghost_dist + 1))
    if newScaredTimes[ghostLocs.index(min_ghost_dist)] > min_ghost_dist:
        ghostScore += (10/(min_ghost_dist + 1)) * 10
        
    return nextScore + foodScore + ghostScore

# Abbreviation
better = betterEvaluationFunction
