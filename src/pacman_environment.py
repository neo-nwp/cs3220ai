import numpy as np
import random

WALL, PATH, FOOD, GOAL, START = 0, 1, 2, 3, 4

class Ghost:
    def __init__(self, loc):
        self.loc = loc
        self.alive = True

class PacmanEnvironment:
    def __init__(self, size=10, wall_ratio=0.25, food_ratio=0.10, seed=None):
        self.rows = self.cols = size
        self.seed = seed
        self.wall_ratio = wall_ratio
        self.food_ratio = food_ratio
        self.generate()

    def generate(self):
        if self.seed is not None:
            np.random.seed(self.seed)
            random.seed(self.seed)

        self.grid = np.ones((self.rows, self.cols), dtype=int)
        total = self.rows * self.cols

        # Walls
        for pos in random.sample(range(total), int(total * self.wall_ratio)):
            self.grid[pos // self.cols, pos % self.cols] = WALL

        # Start + Goal
        free = [(r, c) for r in range(self.rows) for c in range(self.cols) if self.grid[r, c] == PATH]
        self.start, self.goal = random.sample(free, 2)
        self.grid[self.start] = START
        self.grid[self.goal] = GOAL

        # Food
        count_food = max(1, int(total * self.food_ratio))
        self.food_cells = set(random.sample(free, count_food))
        for r, c in self.food_cells:
            if (r, c) != self.start and (r, c) != self.goal:
                self.grid[r, c] = FOOD

        # Ghosts
        spots = [p for p in free if p not in self.food_cells and p not in (self.start, self.goal)]
        self.ghosts = [Ghost(p) for p in random.sample(spots, 5)]

    def is_free(self, r, c):
        return (0 <= r < self.rows) and (0 <= c < self.cols) and self.grid[r, c] != WALL

    def consume_food(self, cell):
        self.food_cells.discard(cell)

    def select_next_food(self, current):
        if not self.food_cells:
            return None
        def manhattan(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])
        return min(self.food_cells, key=lambda f: manhattan(current, f))

    # ✅ NEW: Pretty grid visualization
    def display(self, agent_loc=None):
        for r in range(self.rows):
            row = ""
            for c in range(self.cols):
                cell = (r, c)

                if agent_loc == cell:
                    row += "🟡 "
                elif any(g.loc == cell and g.alive for g in self.ghosts):
                    row += "👻 "
                elif cell in self.food_cells:
                    row += "🍒 "
                elif cell == self.goal:
                    row += "🎯 "
                elif cell == self.start:
                    row += "🚪 "
                elif self.grid[r, c] == WALL:
                    row += "⬛ "
                else:
                    row += "◻️ "
            print(row)
        print()
