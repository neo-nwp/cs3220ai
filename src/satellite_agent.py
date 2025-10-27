import math

class SatelliteAgent:
    """Agent navigating through the asteroid maze."""
    def __init__(self, start, performance):
        self.position = start
        self.performance = performance
        self.alive = True
        self.path = [start]

    def move(self, new_pos):
        self.position = new_pos
        self.path.append(new_pos)

    def encounter_enemy(self, enemy):
        """Handle enemy encounter rules."""
        if enemy.power >= 2 * self.performance:
            self.alive = False
        else:
            self.performance *= 0.9  # defense mode (lose 10%)
        return self.alive
