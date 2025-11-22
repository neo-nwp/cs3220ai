from queue import Queue
from collections import deque

from src.utils import first


# ============================================================
# AC-3 (same idea/style as your Lab 6 version)
# ============================================================

def AC3(csp):
    """
    Enforce arc-consistency on all arcs.
    Returns (True/False, checks) where checks is the number of constraint checks.
    """
    queue = Queue()

    print("Initial queue:")
    for Xi in csp.variables:
        for Xk in csp.neighbors[Xi]:
            queue.put((Xi, Xk))
            print((Xi, Xk), end=" ")
        print()

    csp.support_pruning()
    checks = 0

    while list(queue.queue):
        (Xi, Xj) = queue.get()
        revised, checks = revise(csp, Xi, Xj, checks)
        if revised:
            if not csp.curr_domains[Xi]:
                # Empty domain → inconsistency
                return False, checks
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.put((Xk, Xi))
        print(f"Queue: {list(queue.queue)}")

    return True, checks  # CSP is satisfiable


def revise(csp, Xi, Xj, checks=0):
    """Return (True, checks) if we removed some value from Xi's domain."""
    revised = False
    print(f'Arc {(Xi, Xj)} is checking')

    for x in csp.curr_domains[Xi][:]:  # iterate over a copy
        conflict = True
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(Xi, x)
            print(f'The val {x} was deleted from {Xi} domain')
            revised = True

    return revised, checks


# (Optional) older "back_revise" kept in case your teacher refers to it
def back_revise(csp, Xi, Xj, checks=0):
    """Return (True, checks) if we remove a value from Xj's domain (reverse direction)."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        conflict = False
        for y in csp.curr_domains[Xj]:
            conflict = False
            if not csp.constraints(Xi, x, Xj, y):
                conflict = True
            checks += 1
            if conflict:
                csp.prune(Xj, y)
                print(f'The val {y} was deleted from {Xj} domain')
                revised = True
    return revised, checks


# ============================================================
# Backtracking search + Heuristics
# ============================================================

# ----- Variable ordering -----

def first_unassigned_variable(assignment, csp):
    """Default variable order: first unassigned in the list."""
    return first([var for var in csp.variables if var not in assignment])


def mrv(assignment, csp):
    """
    Minimum Remaining Values (MRV) heuristic:
    choose the unassigned variable with the smallest domain.
    """
    unassigned = [v for v in csp.variables if v not in assignment]
    if not unassigned:
        return None

    if csp.curr_domains is not None:
        return min(unassigned, key=lambda var: len(csp.curr_domains[var]))
    else:
        return min(unassigned, key=lambda var: len(csp.domains[var]))


# ----- Value ordering -----

def unordered_domain_values(var, assignment, csp):
    """Default order: values in the domain as-is."""
    return csp.choices(var)


def lcv(var, assignment, csp):
    """
    Least Constraining Value heuristic:
    order values by how few domain values they rule out for neighbors.
    """

    def conflicts_count(val):
        count = 0
        for nb in csp.neighbors[var]:
            if nb not in assignment:
                for y in csp.choices(nb):
                    if not csp.constraints(var, val, nb, y):
                        count += 1
        return count

    return sorted(csp.choices(var), key=conflicts_count)


# ----- Inference (Forward Checking, MAC) -----

def no_inference(csp, var, value, assignment, removals):
    """Do nothing (used when we don't want extra inference)."""
    return True


def forward_checking(csp, var, value, assignment, removals):
    """
    Forward Checking:
    For each unassigned neighbor of var, remove values that conflict with (var=value).
    If any neighbor domain becomes empty → failure.
    """
    csp.support_pruning()

    for nb in csp.neighbors[var]:
        if nb not in assignment:
            for y in csp.curr_domains[nb][:]:
                if not csp.constraints(var, value, nb, y):
                    csp.prune(nb, y)
                    removals.append((nb, y))
            if not csp.curr_domains[nb]:
                return False
    return True


def mac(csp, var, value, assignment, removals):
    """
    MAC (Maintaining Arc Consistency):
    After assigning var=value, maintain arc consistency using AC-3,
    but only on arcs related to var and the current partial assignment.
    """
    csp.support_pruning()

    # Start with all arcs (Xk, Xi) where Xi is var and Xk is a neighbor
    queue = deque()
    for nb in csp.neighbors[var]:
        if nb not in assignment:
            queue.append((nb, var))

    return ac3_with_removals(csp, queue, removals)


def ac3_with_removals(csp, queue, removals):
    """AC-3 variant that records prunings into 'removals' for later restore()."""
    while queue:
        Xi, Xj = queue.popleft()
        if revise_with_removals(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True


def revise_with_removals(csp, Xi, Xj, removals):
    """Like revise(), but records pruned values into 'removals'."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        if not any(csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x)
            removals.append((Xi, x))
            revised = True
    return revised


# ============================================================
# Backtracking Search (general)
# ============================================================

def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    """
    General backtracking search with pluggable:
      - variable ordering (e.g., mrv)
      - value ordering (e.g., lcv)
      - inference (e.g., forward_checking, mac)
    """

    def backtrack(assignment):
        # If assignment is complete, return it
        if len(assignment) == len(csp.variables):
            return assignment

        var = select_unassigned_variable(assignment, csp)
        if var is None:
            return assignment

        for value in order_domain_values(var, assignment, csp):
            if csp.nconflicts(var, value, assignment) == 0:
                csp.assign(var, value, assignment)
                removals = []
                csp.support_pruning()

                # Keep value in the domain of var (optional, but useful)
                # Here we leave domains as-is; constraints use 'assignment'.

                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result

                # Undo prunings and unassign
                csp.restore(removals)
                csp.unassign(var, assignment)

        return None

    result = backtrack({})
    return result
