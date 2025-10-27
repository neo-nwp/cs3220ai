import heapq
from src.nodeClass import Node

def _manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_manhattan(problem):
    """A* search returning (goal_node, expanded_count)."""
    start = problem.initial
    goal = problem.goal

    start_node = Node(start, None, None, 0)
    frontier = []
    heapq.heappush(frontier, (_manhattan(start, goal), 0, start_node))

    reached = {start: start_node}
    expanded = 0

    while frontier:
        f, g, node = heapq.heappop(frontier)
        expanded += 1

        if node.state == goal:
            return node, expanded  

        for action in problem.actions(node.state):
            s2 = problem.result(node.state, action)
            g2 = node.path_cost + 1
            child = Node(s2, node, action, g2)

            if s2 not in reached or g2 < reached[s2].path_cost:
                reached[s2] = child
                f2 = g2 + _manhattan(s2, goal)
                heapq.heappush(frontier, (f2, g2, child))

    return None, expanded


# ===================== IDA* Manhattan ===================== #

def ida_star_manhattan(problem):
    start, goal = problem.initial, problem.goal
    bound = _manhattan(start, goal)

    start_node = Node(start, None, None, 0)
    expanded = 0

    def search(node, g, bound, visited):
        nonlocal expanded
        expanded += 1

        f = g + _manhattan(node.state, goal)
        if f > bound:
            return f, None
        if node.state == goal:
            node.path_cost = g
            return True, node

        minimum = float('inf')

        for action in problem.actions(node.state):
            s2 = problem.result(node.state, action)
            if s2 in visited:
                continue
            child = Node(s2, node, action, g + 1)
            visited.add(s2)
            t, res = search(child, g + 1, bound, visited)
            if t is True:
                return True, res
            if t < minimum:
                minimum = t
            visited.remove(s2)

        return minimum, None

    while True:
        visited = {start}
        t, res = search(start_node, 0, bound, visited)
        if t is True:
            return res, expanded
        if t == float('inf'):
            return None, expanded
        bound = t

