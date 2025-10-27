DOWN, UP, RIGHT, LEFT = 1, 2, 3, 4

class PacmanMazeProblem:
    def __init__(self, environment, initial, goal):
        self.env = environment
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        r, c = state
        acts = []
        if self.env.is_free(r+1, c): acts.append(DOWN)
        if self.env.is_free(r-1, c): acts.append(UP)
        if self.env.is_free(r, c+1): acts.append(RIGHT)
        if self.env.is_free(r, c-1): acts.append(LEFT)
        return acts

    def result(self, state, action):
        r, c = state
        if action == DOWN: return (r+1, c)
        if action == UP: return (r-1, c)
        if action == RIGHT: return (r, c+1)
        if action == LEFT: return (r, c-1)
        return state

    def goal_test(self, state):
        return state == self.goal
