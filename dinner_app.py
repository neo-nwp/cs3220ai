# dinner_app.py

import streamlit as st
import streamlit.components.v1 as components

import networkx as nx
from pyvis.network import Network

from src.dinner_data import make_dinner_csp, SEATS
from src.algorithms_t1 import (
    first_unassigned_variable,
    unordered_domain_values,
    no_inference,
)


# -------------------------------------------------
# Helper: nice sorting for seat labels
# -------------------------------------------------
def seat_sort_key(seat):
    if isinstance(seat, int):
        return seat
    s = str(seat)
    digits = "".join(ch for ch in s if ch.isdigit())
    try:
        return int(digits)
    except ValueError:
        return 0


# -------------------------------------------------
# Build PyVis graph of the dinner CSP
# -------------------------------------------------
def build_dinner_graph(csp, assignment=None, html_name="dinner_csp_graph.html"):
    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="#000000")
    net.barnes_hut()

    # Nodes
    for seat in sorted(csp.variables, key=seat_sort_key):
        person = assignment.get(seat) if assignment else None

        if person:
            label = f"Seat {seat}: {person}"
            color = "#c4f5c4"  # light green if assigned
        else:
            label = f"Seat {seat}"
            color = "#f0f0f0"  # light gray

        net.add_node(seat, label=label, color=color, shape="circle")

    # Edges
    G = nx.Graph()
    for i in csp.variables:
        for j in csp.neighbors[i]:
            if i < j:
                G.add_edge(i, j)

    for (u, v) in G.edges():
        if abs(u - v) == 1:
            width = 4
            title = "Adjacent seats (special rules)"
        else:
            width = 1
            title = "All-different"

        net.add_edge(u, v, width=width, title=title)

    net.write_html(html_name)
    return html_name


# -------------------------------------------------
# Backtracking search with STEP TRACE (medium detail)
# -------------------------------------------------
def backtracking_search_with_trace(
    csp,
    select_unassigned_variable=first_unassigned_variable,
    order_domain_values=unordered_domain_values,
    inference=no_inference,
):
    """
    Same backtracking search as in algorithms.py,
    but records human-readable steps into a log list.
    """

    log = []

    def log_line(msg):
        log.append(msg)

    def backtrack(assignment, depth=0):
        indent = "  " * depth

        # If assignment is complete, return it
        if len(assignment) == len(csp.variables):
            log_line(f"{indent}✅ Assignment complete: {assignment}")
            return assignment

        # Choose variable
        var = select_unassigned_variable(assignment, csp)
        if var is None:
            log_line(f"{indent}⚠ No unassigned variables left, returning assignment.")
            return assignment

        log_line(f"{indent}▶ Selected variable: Seat {var}")

        # Try values in order
        for value in order_domain_values(var, assignment, csp):
            conflicts = csp.nconflicts(var, value, assignment)
            log_line(
                f"{indent}  Trying Seat {var} = {value} (conflicts = {conflicts})"
            )

            if conflicts == 0:
                # Assign
                csp.assign(var, value, assignment)
                log_line(f"{indent}  → Assign Seat {var} = {value}")

                removals = []
                csp.support_pruning()

                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment, depth + 1)
                    if result is not None:
                        return result

                # Undo and backtrack
                csp.restore(removals)
                csp.unassign(var, assignment)
                log_line(
                    f"{indent}  ↩ Backtracking from Seat {var} = {value} (dead end)"
                )
            else:
                log_line(
                    f"{indent}  ✖ Reject Seat {var} = {value} due to conflicts"
                )

        # No value worked → failure
        log_line(f"{indent}❌ No valid value for Seat {var}, backtracking higher...")
        return None

    result = backtrack({})
    return result, log


# -------------------------------------------------
# Streamlit UI (simple + step explanation)
# -------------------------------------------------
def main():
    st.set_page_config(page_title="Dinner CSP Visualization", layout="wide")

    st.title("🍽️ Dinner Seating CSP — Simple Visualization with Steps")
    st.write(
        """
        This tool solves the **Dinner Table Constraint Satisfaction Problem** using backtracking.

        **Rules**  
        - Each seat must have a **different person**  
        - Adjacent seats cannot seat the following pairs:
          - A next to B  
          - B next to C  
          - B next to E  
        """
    )

    st.write("---")

    if st.button("🔍 Solve CSP"):
        csp = make_dinner_csp()

        st.write("Solving CSP with backtracking...")

        solution, log = backtracking_search_with_trace(
            csp,
            select_unassigned_variable=first_unassigned_variable,
            order_domain_values=unordered_domain_values,
            inference=no_inference,  # no forward checking / MAC (keeps trace simple)
        )

        if solution is None:
            st.error("No solution found.")
            return

        st.success("Solution found! 🎉")

        # Show solution table
        st.subheader("Seating Arrangement")
        st.table([{"Seat": s, "Person": solution[s]} for s in sorted(SEATS)])

        # Show number of assignments
        st.write(f"Assignments tried: **{csp.nassigns}**")

        # Visualization
        st.subheader("CSP Graph")
        html_path = build_dinner_graph(csp, solution)
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        components.html(html, height=600, scrolling=True)

        # Algorithm steps
        st.subheader("🧠 Backtracking Steps (Medium Detail)")
        st.write(
            "These are the main steps of the backtracking algorithm: "
            "which seat is chosen, which value is tried, conflicts, and backtracks."
        )
        st.code("\n".join(log))

    else:
        st.info("Click **Solve CSP** to generate a valid seating arrangement and see the algorithm steps.")


if __name__ == "__main__":
    main()
