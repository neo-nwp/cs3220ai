import streamlit as st
from src.fwgcproblemClass import FWGCProblem
from src.fwgcproblemsolvingagent import FWGCProblemSolvingAgent
from src.PS_agentPrograms import BestFirstSearchAgentProgram

# --- Page and Emoji Configuration ---
st.set_page_config(page_title="FWGC Solver", page_icon="🌊")
ITEM_EMOJIS = {'F': '🧑‍🌾', 'W': '🐺', 'G': '🐐', 'C': '🥬'}
ITEM_NAMES = {'F': 'Farmer', 'W': 'Wolf', 'G': 'Goat', 'C': 'Cabbage'}


# --- Session State Initialization ---
# This is crucial to remember the solution and our place in it.
if 'solution_path' not in st.session_state:
    st.session_state.solution_path = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'problem_instance' not in st.session_state:
    st.session_state.problem_instance = None


# --- Helper Functions ---
def solve_puzzle():
    """Finds the solution and stores it in the session state."""
    with st.spinner("Agent is thinking..."):
        problem = FWGCProblem()
        agent = FWGCProblemSolvingAgent(
            initial_state=problem.initial,
            goal=problem.goal,
            program=BestFirstSearchAgentProgram()
        )
        goal_node = agent.search(problem)
        if goal_node:
            st.session_state.problem_instance = problem
            st.session_state.solution_path = goal_node.path()
            st.session_state.current_step = 0
        else:
            st.error("Could not find a solution.")

def format_bank(bank_items):
    """Creates a string with emojis for the items on a bank."""
    if not bank_items:
        return "_(empty)_"
    return " ".join([ITEM_EMOJIS[item] for item in sorted(list(bank_items))])

def reset_app():
    """Resets the session state to start over."""
    st.session_state.solution_path = None
    st.session_state.problem_instance = None
    st.session_state.current_step = 0
    st.rerun()


# --- Main App UI ---
st.title("FWGC Puzzle Solver 🧑‍🌾🐺🐐🥬")

# --- View 1: Before Solving ---
if st.session_state.solution_path is None:
    if st.button("🔍 Find Solution", type="primary", use_container_width=True):
        solve_puzzle()
        st.rerun()

# --- View 2: After Solving ---
else:
    path = st.session_state.solution_path
    step = st.session_state.current_step
    problem = st.session_state.problem_instance
    current_node = path[step]

    st.header(f"Step {step} / {len(path) - 1}")

    # Display the current state of the river banks with emojis
    west_bank_items = current_node.state
    east_bank_items = problem.all_items - west_bank_items
    
    st.markdown(f"**West Bank:** {format_bank(west_bank_items)}")
    st.markdown("---")
    st.markdown(f"**East Bank:** {format_bank(east_bank_items)}")

    # Display the action that led to this state
    if current_node.action:
        action_emojis = format_bank(current_node.action)
        action_names = " and ".join([ITEM_NAMES[item] for item in current_node.action])
        st.info(f"**Action:** The {action_names} cross the river {action_emojis}")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Previous", use_container_width=True, disabled=(step == 0)):
            st.session_state.current_step -= 1
            st.rerun()

    with col2:
        if st.button("Next ➡️", use_container_width=True, disabled=(step >= len(path) - 1)):
            st.session_state.current_step += 1
            st.rerun()

    # Show a success message on the final step
    if st.session_state.current_step == len(path) - 1:
        st.balloons()
        st.success("🎉 Puzzle Solved!")

    # Add a button to reset and start over
    if st.button("🔄 Reset"):
        reset_app()
