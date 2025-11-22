from src.problemClass import Problem
from src.utils import count


class CSPBasic(Problem):
    def __init__(self, variables, domains, neighbors, constraints):
        """
        Construct a CSP problem.

        variables: list of variable names
        domains: dict var -> list of possible values
        neighbors: dict var -> list of neighboring vars (those that share a constraint)
        constraints: function(Xi, x, Xj, y) -> bool
        """
        variables = variables or list(domains.keys())
        self.variables = list(variables)
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints

        # For search
        self.initial = ()
        self.curr_domains = None   # used when we start pruning (AC-3, FC, MAC)
        self.nassigns = 0          # count how many assigns done (for comparison)

    # ---------- Domain pruning support ----------

    def support_pruning(self):
        """Initialize curr_domains as a copy of domains (only once)."""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def prune(self, var, value):
        """Rule out var = value from current domain."""
        self.curr_domains[var].remove(value)

    def restore(self, removals):
        """
        Undo all prunings in 'removals'.
        removals is a list of (var, value) pairs that were pruned.
        """
        if self.curr_domains is None:
            return
        for var, val in removals:
            if val not in self.curr_domains[var]:
                self.curr_domains[var].append(val)


class CSP(CSPBasic):
    # ---------- Assignment handling ----------

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; overwrite old value if any."""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment."""
        if var in assignment:
            del assignment[var]

    # ---------- Conflict counting ----------

    def nconflicts(self, var, val, assignment):
        """
        Return the number of conflicts var = val has with other assigned variables.
        Uses self.constraints(Xi, x, Xj, y).
        """

        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

        return count(conflict(v) for v in self.neighbors[var])

    # ---------- Convenience methods ----------

    def display(self, assignment):
        """Show a human-readable representation of the CSP."""
        print(assignment)

    def choices(self, var):
        """Return all values for var that are not pruned."""
        return (self.curr_domains or self.domains)[var]