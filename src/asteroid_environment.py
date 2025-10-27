import numpy as np
import random

class Enemy:
    def __init__(self, power):
        self.power = power


class AsteroidEnvironment:
    """Square asteroid maze with start, goal, enemies, and obstacles."""
    def __init__(self, size=7, asteroid_ratio=0.25, enemy_ratio=0.1, seed=None):
        # ✅ Fix: handle both int and (rows, cols)
        if isinstance(size, int):
            self.rows = size
            self.cols = size
        elif isinstance(size, (tuple, list)) and len(size) == 2:
            self.rows, self.cols = size
        else:
            raise ValueError("size must be an int or a tuple (rows, cols)")

        self.asteroid_ratio = asteroid_ratio
        self.enemy_ratio = enemy_ratio
        self.seed = seed
        self.grid = None
        self.enemies = {}
        self.start = None
        self.goal = None
        self.generate()

    def generate(self):
        if self.seed is not None:
            np.random.seed(self.seed)
            random.seed(self.seed)

        total_cells = self.rows * self.cols
        asteroid_count = int(total_cells * self.asteroid_ratio)
        enemy_count = int(total_cells * self.enemy_ratio)

        grid = np.zeros((self.rows, self.cols), dtype=int)

        asteroid_positions = random.sample(range(total_cells), asteroid_count)
        for pos in asteroid_positions:
            r, c = divmod(pos, self.cols)
            grid[r, c] = 1

        free_positions = [i for i in range(total_cells) if i not in asteroid_positions]
        enemy_positions = random.sample(free_positions, enemy_count)
        for pos in enemy_positions:
            r, c = divmod(pos, self.cols)
            grid[r, c] = 2
            self.enemies[(r, c)] = Enemy(power=random.randint(5, 15))

        remaining_free = [i for i in free_positions if i not in enemy_positions]
        start_idx, goal_idx = random.sample(remaining_free, 2)
        sr, sc = divmod(start_idx, self.cols)
        gr, gc = divmod(goal_idx, self.cols)
        grid[sr, sc] = 4
        grid[gr, gc] = 3

        self.grid = grid
        self.start = (sr, sc)
        self.goal = (gr, gc)

    def is_free(self, r, c):
        return (0 <= r < self.rows) and (0 <= c < self.cols) and self.grid[r, c] != 1

