# Defines the structure of the maze as a graph and lists the treasures.

def get_maze_graph():
    """Returns the maze structure as a dictionary."""
    return {
        'A': {'B': 1, 'E': 1},
        'B': {'A': 1, 'C': 1, 'F': 1},
        'C': {'B': 1, 'D': 1},
        'D': {'C': 1, 'H': 1, 'L': 1},
        'E': {'A': 1, 'I': 1},
        'F': {'B': 1, 'G': 1, 'J': 1},
        'G': {'F': 1, 'K': 1},
        'H': {'D': 1, 'L': 1},
        'I': {'E': 1, 'J': 1},
        'J': {'F': 1, 'I': 1, 'N': 1},
        'K': {'G': 1, 'O': 1},
        'L': {'D': 1, 'H': 1, 'P': 1},
        'M': {'N': 1},
        'N': {'J': 1, 'M': 1, 'O': 1},
        'O': {'K': 1, 'N': 1},
        'P': {'L': 1}
    }

def get_treasures():
    """Returns a list of available treasures."""
    return [
        "Pile of Gold",
        "Diamond",
        "Flyer for 100 Free Pizzas",
        "20 Extra Points for CS3220 Final Exam"
    ]

