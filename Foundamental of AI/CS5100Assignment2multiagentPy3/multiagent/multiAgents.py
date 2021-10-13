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
        ghostPositions = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        from util import manhattanDistance

        score = 0

        food = newFood.asList()
        foodDistances = []
        ghostDistances = []

        for item in food:
            foodDistances.append(manhattanDistance(newPos, item))

        for item in ghostPositions:
            ghostDistances.append(manhattanDistance(newPos, item))

        for i in foodDistances:
            if i <= 2:
                score += 1
            if 2 < i < 6:
                score += 0.5
            else:
                score += 0.15

        for i in ghostDistances:
            if i <= 2:
                score -= 5
            else:
                score -= 1

        if len(foodDistances) == 0:
            return 0

        if action == 'Stop':
            score -= 50

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore() + score

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
        # result = [score, action]
        action = self.get_value(gameState, 0, 0)

        return action[1]

    def get_value(self, gameState, index, depth):

        # Terminal states:
        if len(gameState.getLegalActions(index)) == 0 or depth == self.depth:
            return gameState.getScore(), ""

        # Max-agent: Pacman has index = 0
        if index == 0:
            return self.max_value(gameState, index, depth)

        # Min-agent: Ghost has index > 0
        else:
            return self.min_value(gameState, index, depth)

    def max_value(self, gameState, index, depth):

        legal_actions = gameState.getLegalActions(index)
        max_value = float("-inf")
        max_action = ""

        for action in legal_actions:
            successor = gameState.generateSuccessor(index, action)
            successor_index = index + 1
            successor_depth = depth

            # If there is only 1 agent left, that must be pacman
            if successor_index == gameState.getNumAgents():
                successor_index = 0
                successor_depth += 1

            current_value = self.get_value(successor, successor_index, successor_depth)[0]

            if current_value > max_value:
                max_value = current_value
                max_action = action

        return max_value, max_action

    def min_value(self, gameState, index, depth):
        # similar as the max_value(), but we keep track of the minimum value
        legal_actions = gameState.getLegalActions(index)
        min_value = float("inf")
        min_action = ""

        for action in legal_actions:
            successor = gameState.generateSuccessor(index, action)
            successor_index = index + 1
            successor_depth = depth

            # If there is only 1 agent left, that must be pacman
            if successor_index == gameState.getNumAgents():
                successor_index = 0
                successor_depth += 1

            current_value = self.get_value(successor, successor_index, successor_depth)[0]

            if current_value < min_value:
                min_value = current_value
                min_action = action

        return min_value, min_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # result = [score, action]
        action = self.get_value(gameState, 0, 0, float("-inf"), float("inf"))

        return action[1]


    def get_value(self, gameState, index, depth, alpha, beta):

        # Terminal states:
        if len(gameState.getLegalActions(index)) == 0 or depth == self.depth:
            return gameState.getScore(), ""

        # Max-agent: Pacman has index = 0
        if index == 0:
            return self.max_value(gameState, index, depth, alpha, beta)

        # Min-agent: Ghost has index > 0
        else:
            return self.min_value(gameState, index, depth, alpha, beta)

    def max_value(self, gameState, index, depth, alpha, beta):

        legal_actions = gameState.getLegalActions(index)
        max_value = float("-inf")
        max_action = ""

        for action in legal_actions:
            successor = gameState.generateSuccessor(index, action)
            successor_index = index + 1
            successor_depth = depth

            # If there is only 1 agent left, that must be pacman
            if successor_index == gameState.getNumAgents():
                successor_index = 0
                successor_depth += 1

            current_value = self.get_value(successor, successor_index, successor_depth, alpha, beta)[0]

            if current_value > max_value:
                max_value = current_value
                max_action = action

            alpha = max(max_value, alpha)

            if max_value > beta:
                return max_value, max_action

        return max_value, max_action

    def min_value(self, gameState, index, depth, alpha, beta):
        # similar as the max_value(), but we keep track of the minimum value
        legal_actions = gameState.getLegalActions(index)
        min_value = float("inf")
        min_action = ""

        for action in legal_actions:
            successor = gameState.generateSuccessor(index, action)
            successor_index = index + 1
            successor_depth = depth

            # If there is only 1 agent left, that must be pacman
            if successor_index == gameState.getNumAgents():
                successor_index = 0
                successor_depth += 1

            current_value = self.get_value(successor, successor_index, successor_depth, alpha, beta)[0]

            if current_value < min_value:
                min_value = current_value
                min_action = action

            beta = min(min_value, beta)

            if min_value < alpha:
                return min_value, min_action

        return min_value, min_action

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
        # result = [score, action]
        action = self.get_value(gameState, 0, 0)

        return action[1]

    def get_value(self, gameState, index, depth):

        # Terminal states:
        if len(gameState.getLegalActions(index)) == 0 or depth == self.depth:
            return gameState.getScore(), ""

        # Max-agent: Pacman has index = 0
        if index == 0:
            return self.max_value(gameState, index, depth)

        # Min-agent: Ghost has index > 0
        else:
            return self.expect_value(gameState, index, depth)

    def max_value(self, gameState, index, depth):

        legal_actions = gameState.getLegalActions(index)
        max_value = float("-inf")
        max_action = ""

        for action in legal_actions:
            successor = gameState.generateSuccessor(index, action)
            successor_index = index + 1
            successor_depth = depth

            # If there is only 1 agent left, that must be pacman
            if successor_index == gameState.getNumAgents():
                successor_index = 0
                successor_depth += 1

            current_value = self.get_value(successor, successor_index, successor_depth)[0]

            if current_value > max_value:
                max_value = current_value
                max_action = action

        return max_value, max_action

    def expect_value(self, gameState, index, depth):
        # similar as the max_value(), but we keep track of the minimum value
        legal_actions = gameState.getLegalActions(index)
        expected_value = 0
        expected_action = ""

        probability = 1.0 / len(legal_actions)

        for action in legal_actions:
            successor = gameState.generateSuccessor(index, action)
            successor_index = index + 1
            successor_depth = depth

            # If there is only 1 agent left, that must be pacman
            if successor_index == gameState.getNumAgents():
                successor_index = 0
                successor_depth += 1

            current_value = self.get_value(successor, successor_index, successor_depth)[0]

            expected_value += probability * current_value

        return expected_value, expected_action

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    cur_pos = currentGameState.getPacmanPosition()
    cur_food = currentGameState.getFood()
    cur_ghost_states = currentGameState.getGhostStates()
    ghost_positions = currentGameState.getGhostPositions()
    new_scared_times = [ghostState.scaredTimer for ghostState in cur_ghost_states]

    active_ghost = []
    scared_ghosts = []
    from util import manhattanDistance

    # Instantiate score with current state's value
    # The score will be incremented/decreased
    # by other weighted factors mentioned below.
    score = currentGameState.getScore()

    for ghost in cur_ghost_states:
        if ghost.scaredTimer:
            scared_ghosts.append(ghost)
        else:
            active_ghost.append(ghost)

    # Food weight: -20
    # Since eat all food in the state is our ultimate goal,
    # it will lower the evaluation score if there are a lot of food left.
    score += -20 * len(cur_food)

    # Capsules weight: -10
    # Since eat we will get a huge amount of points if pacman eat a ghost,
    # eat a capsules means it has a higher probability to eat ghost.
    # As a capsules coule be far away from the pacman's current location,
    # a lower weight was assigned than the food weight.

    total_Capsules = len(currentGameState.getCapsules())
    score += -10 * total_Capsules

    food = cur_food.asList()
    food_distances = []
    active_ghost_distances = []
    scared_ghost_distances = []

    for item in food:
        food_distances.append(-1 * manhattanDistance(cur_pos, item))

    for item in active_ghost:
        active_ghost_distances.append(manhattanDistance(cur_pos, item))

    for item in scared_ghosts:
        scared_ghost_distances.append(manhattanDistance(cur_pos, item))

    if not food_distances:
        food_distances.append(0)


    # It is prioritized to eat all food close to the pacman.
    # The weight for this factor is categorized by distance.
    for i in food_distances:
        if i <= 4:
            score += -1 * item
        if 4 < i < 16:
            score += -0.5 * item
        else:
            score += -0.1 * item


    # Hi scared ghoast, here I am!!
    # Weight 20 is assigt to the nearby scared ghost.
    for i in scared_ghost_distances:
        if i <= 4:
            score += -20 * item
        else:
            score += -10 * item

    # Lastly, we should not forget, there are also active ghoast.
    # It better to keep as far as we can.
    # Similarly, the weight for this factor is categorized by distance.
    for i in active_ghost_distances:
        if i <= 4:
            score += 2 * item
        if 4 < i < 16:
            score += 4 * item
        else:
            score += 6 * item


    "*** YOUR CODE HERE ***"
    return  score

# Abbreviation
better = betterEvaluationFunction
