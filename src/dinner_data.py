# src/dinner_data.py

from src.CSPclass import CSP

# People
PEOPLE = ["A", "B", "C", "D", "E"]

# Seats (variables)
SEATS = [1, 2, 3, 4, 5]


def make_neighbors():
    """
    We want a GLOBAL 'all-different' constraint:
    -> any pair of seats must not have the same person.

    So we make a COMPLETE graph: every seat is a neighbor of every other.
    """
    neighbors = {}
    for i in SEATS:
        neighbors[i] = [j for j in SEATS if j != i]
    return neighbors


def dinner_constraint(Xi, vi, Xj, vj):
    """
    Constraint between two seats Xi and Xj (could be neighbors or not).

    vi, vj are the people sitting at those seats.

    1. GLOBAL all-different:
       No person can sit in two seats => vi != vj for ALL pairs.

    2. EXTRA rules only for ADJACENT seats (|Xi - Xj| == 1):
       - A cannot sit next to B
       - B cannot sit next to E
       - B cannot sit next to C
    """

    # 1) Global all-different: same person in two seats is forbidden
    if vi == vj:
        return False

    # 2) Adjacency-based rules (only apply to neighboring seats)
    if abs(Xi - Xj) == 1:
        bad_pairs = {
            ("A", "B"), ("B", "A"),
            ("B", "E"), ("E", "B"),
            ("B", "C"), ("C", "B"),
        }
        if (vi, vj) in bad_pairs:
            return False

    # Otherwise it's fine
    return True


def make_dinner_csp():
    """
    Build the CSP object for the dinner seating problem.
    Variables  : seats 1..5
    Domains    : each seat can be any of A, B, C, D, E initially
    Neighbors  : all seats pairwise (complete graph)
    Constraints: dinner_constraint (global all-different + local conflict rules)
    """
    neighbors = make_neighbors()
    domains = {seat: PEOPLE[:] for seat in SEATS}

    def constraints(Xi, vi, Xj, vj):
        return dinner_constraint(Xi, vi, Xj, vj)

    return CSP(SEATS, domains, neighbors, constraints)
