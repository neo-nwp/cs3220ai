import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
from src.sudoku import AsteriskSudoku
from src.algorithms import backtracking_search

# --- Constants ---
AST_COLOR = "#ff4d4d"
FILLED  = "#ffd93d"
EMPTY   = "#ffffff"

st.set_page_config(page_title="Lab-7 Asterisk-Sudoku", layout="wide")
st.title("Lab-7 Task-2 – Asterisk Sudoku")

# --- Puzzles ---
puzzles = {
    "Valid Asterisk Sudoku": 
        "000000000"
        "000000000"
        "000000000"
        "000100000"
        "000020000"
        "000003000"
        "000000400"
        "000000050"
        "000000006",
    "Hard (Original)":
        "000000000"
        "003600000"
        "070090200"
        "050007000"
        "000045700"
        "000100030"
        "001000068"
        "008500010"
        "090000400",
    "Impossible (Standard Sudoku)":
        "530070000"
        "600195000"
        "098000060"
        "800060003"
        "400803001"
        "700020006"
        "060000280"
        "000419005"
        "000080079",
}

grid_name = st.sidebar.selectbox("Puzzle", list(puzzles.keys()))
grid81 = puzzles[grid_name]

# --- Solver ---
@st.cache_data(show_spinner=False)
def solve(g):
    csp = AsteriskSudoku(g)
    sol, history = backtracking_search(csp)
    return csp, sol, history

csp, sol, history = solve(grid81)

# --- Visuals (HTML Table) ---
def show_grid_html(title):
    st.subheader(title)
    html = '<table style="border-collapse: collapse; margin-bottom: 20px;">'
    for r in range(9):
        html += '<tr>'
        for c in range(9):
            idx = r * 9 + c
            val = sol[idx] if (sol and idx in sol) else ""
            is_fixed = len(csp.domains[idx]) == 1
            bg_color = FILLED if is_fixed else EMPTY
            
            # Border Logic
            is_ast = idx in csp.asterisk
            border_color = AST_COLOR if is_ast else "#888"
            
            # Thick borders for 3x3 boxes
            border_top = "3px solid black" if r % 3 == 0 else f"1px solid {border_color}"
            border_left = "3px solid black" if c % 3 == 0 else f"1px solid {border_color}"
            border_right = "3px solid black" if c == 8 else f"1px solid {border_color}"
            border_bottom = "3px solid black" if r == 8 else f"1px solid {border_color}"

            style = (f"width: 40px; height: 40px; text-align: center; color: black; "
                     f"background-color: {bg_color}; font-weight: bold; font-family: sans-serif; "
                     f"border-top: {border_top}; border-left: {border_left}; "
                     f"border-right: {border_right}; border-bottom: {border_bottom};")
            
            if is_ast: 
                style += f"border: 3px solid {AST_COLOR};"
            
            html += f'<td style="{style}">{val}</td>'
        html += '</tr>'
    html += '</table>'  # <--- FIXED: Table closes here, outside the loop
    st.markdown(html, unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    show_grid_html("Solved Grid" if sol else "No Solution Found")

    # --- Algorithm Steps Log ---
    st.subheader("Algorithm Steps")
    if history:
        with st.expander(f"View all {len(history)} steps"):
            for i, step in enumerate(history):
                r, c = divmod(step['var'], 9)
                action = step['action']
                val = step['val']
                icon = "🟢" if action == "Assign" else "🔴"
                st.write(f"{icon} **Step {i+1}:** {action} value **{val}** to Cell ({r}, {c})")
    else:
        st.write("No steps recorded.")

with col2:
    # --- Graph ---
    st.subheader("Constraint Graph")
    def vis_graph():
        net = Network(height="500px", width="100%", bgcolor="#222", font_color="white")
        g = nx.Graph()
        for v in range(81):
            is_ast = v in csp.asterisk
            label = str(sol[v]) if (sol and v in sol) else str(v)
            g.add_node(v, label=label, shape="square", size=20,
                       color=FILLED if len(csp.domains[v]) == 1 else EMPTY,
                       borderWidth=3, colorBorder=AST_COLOR if is_ast else "#000")
        for v in csp.vars:
            for u in csp.neighbours[v]:
                if v < u: 
                    g.add_edge(v, u, color="#555", width=0.5)
        net.from_nx(g)
        net.toggle_physics(False)
        path = "ast.html"
        net.save_graph(path)
        return path

    if sol:
        html_path = vis_graph()
        components.html(open(html_path).read(), height=550)
    else:
        st.error("No solution found.")

# --- Sidebar Metrics ---
st.sidebar.metric("Total Steps", len(history) if history else 0)
st.sidebar.metric("Assignments Attempted", csp.nassigns)
st.sidebar.metric("Solution Found", str(sol is not None))