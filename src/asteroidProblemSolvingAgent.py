from src.problemSolvingAgentProgramClass import SimpleProblemSolvingAgentProgram
from src.asteroid_problem import AsteroidMazeProblem

class AsteroidProblemSolvingAgent(SimpleProblemSolvingAgentProgram):
    def __init__(self, initial_state=None, environment=None, goal=None):
        super().__init__(initial_state)
        self.environment = environment      # 🟩 store the full environment, not just grid
        self.goal = goal

    def update_state(self, state, percept):
        return percept

    def formulate_goal(self, state):
        if self.goal is not None:
            return self.goal
        else:
            print("No goal! can't work!")
            return None

    def formulate_problem(self, state, goal):
        # 🟩 pass the environment object (it has .start and .goal)
        problem = AsteroidMazeProblem(self.environment)
        return problem

    def search(self, problem):
        seq = self.program(problem)
        return seq
