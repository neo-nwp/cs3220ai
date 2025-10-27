from src.navigation_search import astar_manhattan, ida_star_manhattan
from src.pacman_problem import PacmanMazeProblem


class PacmanProblemSolvingAgentSMART:

    def __init__(self, start, env, goal, use_ida=False):
        self.start = start
        self.location = start
        self.state = start
        self.goal = goal
        self.env = env
        self.plan = []
        self.alive = True
        self.performance = 0
        self.use_ida = use_ida   # ✅ REQUIRED TO SWITCH A* / IDA*

    def _search_to(self, start, target):
        problem = PacmanMazeProblem(self.env.pacman_env, start, target)

        if self.use_ida:
            node, expanded = ida_star_manhattan(problem)
            tag = "IDA*"
        else:
            node, expanded = astar_manhattan(problem)
            tag = "A*"

        if node is None:
            print(f"[{tag}] No path to {target}")
            return None, None

        path = [n.state for n in node.path()]
        print(f"[{tag}] to {target}: cost={node.path_cost}, expanded={expanded}")
        return path, node.path_cost