import random
import collections
from src.environmentClass import Environment
from src.graphProblemClass import GraphProblem
from src.PS_agentPrograms import BestFirstSearchAgentProgram

class TreasureMazeEnvironment(Environment):
    """
    An environment for the Treasure Maze problem.
    It manages the maze layout, treasure locations, and agent interactions.
    """
    def __init__(self, maze_graph, treasures, start_node, end_node):
        super().__init__()
        self.maze_graph = maze_graph
        self.treasures_list = treasures
        self.start_node = start_node
        self.end_node = end_node
        self.treasure_locations = {}
        self.place_treasures()

    def place_treasures(self):
        """Randomly places treasures on valid maze nodes."""
        nodes = list(self.maze_graph.nodes())
        valid_nodes = [node for node in nodes if node not in [self.start_node, self.end_node]]
        
        if len(valid_nodes) < len(self.treasures_list):
            raise ValueError("Not enough valid nodes in the maze to place all treasures.")
            
        random.shuffle(valid_nodes)
        
        for i, treasure in enumerate(self.treasures_list):
            self.treasure_locations[valid_nodes[i]] = treasure

    def execute_action(self, agent, action):
        """Updates the agent's state and performance based on an action."""
        if agent.alive:
            agent.state = action
            agent.performance -= 1
            if agent.performance <= 0:
                agent.alive = False

    def is_done(self):
        """The environment is done if no agents are alive."""
        return not any(agent.alive for agent in self.agents)


class TreasureMazeAgent(collections.abc.Callable):
    """
    A problem-solving agent for the Treasure Maze.
    The agent first seeks a treasure and then seeks the exit.
    """
    def __init__(self, initial_state, maze_graph, treasure_locs, exit_goal, program=None):
        self.state = initial_state
        self.maze_graph = maze_graph
        self.treasure_locations = treasure_locs
        self.exit_goal = exit_goal
        
        self.performance = len(maze_graph.nodes()) * 0.5
        self.alive = True
        
        self.seq = [] # The final sequence of actions
        self.found_treasure_info = None
        self.log = []

        if program is None:
            self.program = BestFirstSearchAgentProgram()
        else:
            self.program = program

    def __call__(self, percept):
        """Main logic for the agent's decision-making process."""
        self.state = percept
        if not self.seq:
            self.log.append("Agent starts at '{}'. Performance: {}".format(self.state, self.performance))
            # 1. Search for a treasure
            treasure_problem = GraphProblem(self.state, list(self.treasure_locations.keys()), self.maze_graph)
            treasure_path_node = self.program(treasure_problem)
            
            if not treasure_path_node:
                self.log.append("Agent could not find a path to any treasure.")
                self.alive = False
                return

            treasure_path = self.actions_from_path(treasure_path_node.path())
            treasure_location = treasure_path[-1] if treasure_path else self.state
            self.found_treasure_info = (treasure_location, self.treasure_locations[treasure_location])
            self.log.append("Agent found a path to the treasure '{}' at '{}'.".format(self.found_treasure_info[1], self.found_treasure_info[0]))

            # 2. Search for the exit from the treasure's location
            self.log.append("Agent is now searching for the exit '{}'.".format(self.exit_goal))
            exit_problem = GraphProblem(treasure_location, self.exit_goal, self.maze_graph)
            exit_path_node = self.program(exit_problem)
            
            if not exit_path_node:
                self.log.append("Agent found a treasure but could not find a path to the exit.")
                self.alive = False
                return

            exit_path = self.actions_from_path(exit_path_node.path())
            
            # Combine paths. The first element of exit_path is the treasure location itself.
            self.seq = treasure_path + exit_path[1:]
            self.log.append("Full path calculated: {}".format(self.seq))


    def actions_from_path(self, path_nodes):
        """Utility to convert a node path to a sequence of state actions."""
        return [node.state for node in path_nodes]

