from .problemClass import Problem

class FWGCProblem(Problem):
    """
    The problem of the transporting a farmer, wolf, goar, and cabbage across a river.
    Stare is represented by frozenset of items on the West  bank.
    'F'(Farmer), 'W'(Wolf), 'G'(Goat), 'C'(Cabbage).
    """

    def __init__(self, initial=frozenset({'F', 'W', 'G', 'C'}), goal=frozenset()):
        """Define the initial and goal states."""
        super().__init__(initial, goal)
        self.all_items = frozenset({'F', 'W', 'G', 'C'})

    def is_unsafe(self, bank):
        """
        Return True if the bank is unsafe. A bank is unsafe if the farmer is not
        present and either the wolf and goat are together, or the goat and cabbage are together.
        """
        return 'F' not in bank and (('W' in bank and 'G' in bank) or ('G' in bank and 'C' in bank))

    def actions(self, state):
        """
        Return the valid actions that can be executed in the given state.
        An action is the set of items moving across the river. The farmer
        must always be in the set.
        """
        possible_actions = []
        
        # Determine which bank the farmer is on to generate valid moves
        if 'F' in state:  # Farmer is on the West bank, moving East
            # Farmer can take one item or go alone
            items_to_move = state - {'F'}
            
            # Action: Farmer crosses with one item from West to East
            for item in items_to_move:
                action = frozenset({'F', item})
                # Check if the resulting state is safe
                if not self.is_unsafe(state - action):
                    possible_actions.append(action)
            
            # Action: Farmer crosses alone from West to East
            action = frozenset({'F'})
            if not self.is_unsafe(state - action):
                possible_actions.append(action)
        
        else:  # Farmer is on the East bank, moving West
            items_on_east_bank = self.all_items - state
            items_to_move = items_on_east_bank - {'F'}

            # Action: Farmer crosses with one item from East to West
            for item in items_to_move:
                action = frozenset({'F', item})
                # Check if the resulting state is safe
                if not self.is_unsafe(items_on_east_bank - action):
                    possible_actions.append(action)

            # Action: Farmer crosses alone from East to West
            action = frozenset({'F'})
            if not self.is_unsafe(items_on_east_bank - action):
                 possible_actions.append(action)
        
        return possible_actions

    def result(self, state, action):
        """
        Return the state that results from executing a given action.
        The new state is the symmetric difference of the current state and the action.
        """
        return state.symmetric_difference(action)

    def goal_test(self, state):
        """Return True if the state is a goal state."""
        return state == self.goal
