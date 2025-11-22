# run_dinner.py

from src.dinner_data import make_dinner_csp, SEATS
from src.algorithms_t1 import backtracking_search

if __name__ == "__main__":
    csp = make_dinner_csp()
    solution = backtracking_search(csp)

    print("=== Dinner Seating Solution ===")
    if solution is None:
        print("No valid seating arangement found.")
    else:
        for seat in sorted(SEATS):
            print(f"Seat {seat}: {solution[seat]}")
