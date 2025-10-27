from src.pacman_problem import PacmanMazeProblem
from src.navigation_search import astar_manhattan, ida_star_manhattan

class Environment:

    def __init__(self, pacman_env, use_ida=False, max_steps=600):
        self.agents = []
        self.pacman_env = pacman_env
        self.use_ida = use_ida
        self.max_steps = max_steps
        self.step_count = 0

        self.rows = pacman_env.rows
        self.cols = pacman_env.cols
        self.total_cells = self.rows * self.cols

    def add_thing(self, agent, location=None):
        agent.location = agent.start
        agent.state = agent.location
        agent.alive = True
        agent.performance = int(0.30 * self.total_cells)
        print(f"✅ Added {agent.__class__.__name__} at {agent.location} | Initial Performance = {agent.performance}")
        self.agents.append(agent)

        # ✅ Show initial map
        self.pacman_env.display(agent.location)

    def percept(self, agent):
        return agent.location

    def execute_action(self, agent, action):
        if action is None:
            return False

        agent.location = action
        agent.state = action
        print(f"➡️ Pac-Man moved to {agent.location}")

        # Food
        if agent.location in self.pacman_env.food_cells:
            self.pacman_env.consume_food(agent.location)
            agent.performance *= 2
            print(f"🍒 Ate FOOD at {agent.location} | Performance doubled!")

        # Ghost
        for g in self.pacman_env.ghosts:
            if g.alive and g.loc == agent.location:
                if agent.performance > int(0.30 * self.total_cells):
                    g.alive = False
                    agent.performance = int(agent.performance * 0.9)
                    print("👻 Fought ghost & WON (Performance -10%)")
                else:
                    print("💀 Pac-Man was killed by ghost!")
                    agent.alive = False
                    self.pacman_env.display(agent.location)
                    return False

        # ✅ Display map after move
        self.pacman_env.display(agent.location)
        return True

    def _search_to(self, start, target):
        problem = PacmanMazeProblem(self.pacman_env, start, target)
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
        cost = node.path_cost
        print(f"[{tag}] to {target}: cost={cost}, expanded={expanded}")
        return path, cost

    def step(self, agent):
        if not agent.plan:
            return False
        next_move = agent.plan.pop(0)
        return self.execute_action(agent, next_move)

    def run(self):
        agent = self.agents[0]
        print("\n🍽 Starting MULTI-GOAL search...\n")

        while agent.alive and self.pacman_env.food_cells:
            current = agent.location
            best_food, best_path, best_cost = None, None, None

            for food in self.pacman_env.food_cells:
                path, cost = self._search_to(current, food)
                if path and (best_cost is None or cost < best_cost):
                    best_food, best_path, best_cost = food, path, cost

            if not best_food:
                print("❌ No reachable food left.")
                break

            print(f"🎯 Next target food: {best_food} (cost={best_cost})")

            agent.plan = best_path[1:]
            while agent.alive and agent.location != best_food:
                if not self.step(agent):
                    break

        if agent.alive:
            print("\n🎯 All food collected. Going to final GOAL...")
            path, cost = self._search_to(agent.location, self.pacman_env.goal)
            if path:
                agent.plan = path[1:]
                while agent.alive and agent.location != self.pacman_env.goal:
                    if not self.step(agent):
                        break

        if agent.location == self.pacman_env.goal:
            print("🏁 Goal reached — agent stops.")
        else:
            print("⚠️ Agent stopped before goal.")
