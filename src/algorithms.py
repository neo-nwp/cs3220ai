from src.utils import first

# ------------- Heuristics -------------
def mrv(assignment, csp):
    """Minimum Remaining Values heuristic."""
    def count_legal_values(var):
        return sum(1 for val in csp.choices(var) 
                   if csp.nconflicts(var, val, assignment) == 0)

    unassigned = [v for v in csp.vars if v not in assignment]
    return min(unassigned, key=count_legal_values)

def order_domain(var, assignment, csp):
    return csp.choices(var)

# ------------- Backtracking Search (With History) -------------
def backtracking_search(csp,
                        select=mrv,
                        order=order_domain):
    
    # List to record every step: {'action': 'Assign', 'var': 0, 'val': 1}
    history = []

    def backtrack(assignment):
        if len(assignment) == len(csp.vars):
            return assignment
        
        var = select(assignment, csp)
        
        for val in order(var, assignment, csp):
            if csp.nconflicts(var, val, assignment) == 0:
                csp.assign(var, val, assignment)
                
                # LOG THE STEP
                history.append({"action": "Assign", "var": var, "val": val})
                
                result = backtrack(assignment)
                if result is not None:
                    return result
                
                csp.unassign(var, assignment)
                
                # LOG THE BACKTRACK
                history.append({"action": "Backtrack", "var": var, "val": val})
                
        return None

    solution = backtrack({})
    return solution, history  # Return both