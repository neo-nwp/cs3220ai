import numpy as np
from src.nodeClass import Node

class AsteroidMazeProblem:
    """
    Defines the problem for the asteroid navigation:
    - environment: the grid world
    - initial: starting position (row, col)
    - goal: goal position (row, col)
    """
    def __init__(self, environment, initial, goal):
        self.environment = environment
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return all possible moves (1: down, 2: up, 3: right, 4: left)."""
        possible_actions = []
        rows, cols = self.environment.rows, self.environment.cols
        r, c = state

        # ↓ Move down
        if r + 1 < rows and self.environment.grid[r + 1][c] != 1:
            possible_actions.append(1)
        # ↑ Move up
        if r - 1 >= 0 and self.environment.grid[r - 1][c] != 1:
            possible_actions.append(2)
        # → Move right
        if c + 1 < cols and self.environment.grid[r][c + 1] != 1:
            possible_actions.append(3)
        # ← Move left
        if c - 1 >= 0 and self.environment.grid[r][c - 1] != 1:
            possible_actions.append(4)

        return possible_actions

    def result(self, state, action):
        """Return the new state after performing the action."""
        r, c = state
        if action == 1:  # down
            return (r + 1, c)
        elif action == 2:  # up
            return (r - 1, c)
        elif action == 3:  # right
            return (r, c + 1)
        elif action == 4:  # left
            return (r, c - 1)
        return state

    def goal_test(self, state):
        """Check if the current state is the goal."""
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Uniform cost (1 per move)."""
        return c + 1
