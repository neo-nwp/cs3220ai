import collections
from .problemSolvingAgentProgramClass import SimpleProblemSolvingAgentProgram
from .fwgcproblemClass import FWGCProblem

class FWGCProblemSolvingAgent(SimpleProblemSolvingAgentProgram):
    """
    A specific problem-solving agent for the Farmer, Wolf, Goat, Cabbage problem.
    """
    def __init__(self, initial_state=None, goal=None, program=None):
        super().__init__(initial_state)
        self.goal = goal
        
        if program is None or not isinstance(program, collections.abc.Callable):
            raise ValueError("A valid search program (e.g., BestFirstSearchAgentProgram) is required.")
        
        self.program = program

    def update_state(self, state, percept):
        """For this simple agent, the state doesn't change based on percepts."""
        return state

    def formulate_goal(self, state):
        """Returns the predefined goal."""
        return self.goal

    def formulate_problem(self, state, goal):
        """Creates an instance of the FWGCProblem."""
        return FWGCProblem(initial=state, goal=goal)

    def search(self, problem):
        """
        Uses the assigned search program to find a solution node.
        """
        return self.program(problem)
