class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.vars = variables
        self.domains = domains
        self.neighbours = neighbours  # British spelling
        self.constraints = constraints
        self.nassigns = 0
        self._curr = None          # lazy init

    # ---- pruning support ----
    def _support_prune(self):
        if self._curr is None:
            self._curr = {v: list(self.domains[v]) for v in self.vars}

    def prune(self, var, val):
        self._support_prune()
        if val in self._curr[var]:
            self._curr[var].remove(val)

    # ---- basic interface ----
    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        assignment.pop(var, None)

    def nconflicts(self, var, val, assignment):
        def conf(v2):
            # Check if neighbor v2 is assigned and conflicts with var=val
            return v2 in assignment and not self.constraints(var, val, v2, assignment[v2])
        
        return sum(conf(v2) for v2 in self.neighbours[var])

    def choices(self, var):
        self._support_prune()
        return self._curr[var]