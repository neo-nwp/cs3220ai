from src.navigation_search import astar_manhattan, ida_star_manhattan

class AStarManhattanSmartAgentProgram:
    def __call__(self, percept):
        problem = percept["problem"]
        start = percept["current"]
        goal = percept["target"]

        node, expanded = astar_manhattan(problem)
        if node is None:
            print("[SMART A*] No path found.")
            return None

        path = [n.state for n in node.path()]
        cost = node.path_cost
        print(f"[SMART A* Manhattan] Nodes expanded: {expanded} | Total cost: {cost}")
        return path


class IDAStarManhattanSmartAgentProgram:
    def __call__(self, percept):
        problem = percept["problem"]
        start = percept["current"]
        goal = percept["target"]

        node, expanded = ida_star_manhattan(problem)
        if node is None:
            print("[SMART IDA*] No path found.")
            return None

        path = [n.state for n in node.path()]     # ✅ convert Node → list of positions
        cost = node.path_cost
        print(f"[SMART IDA* Manhattan] Nodes expanded: {expanded} | Total cost: {cost}")
        return path
