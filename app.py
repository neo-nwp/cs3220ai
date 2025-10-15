import streamlit as st
import random
from pyvis.network import Network
import streamlit.components.v1 as components
import sys
import os

# Add the parent directory to the Python path to allow imports from `src`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graphClass import Graph
from src.maze_data import get_maze_graph, get_treasures
from src.treasure_maze import TreasureMazeEnvironment, TreasureMazeAgent

def visualize_maze(maze_graph, start_node, end_node, treasure_locs, agent_path=None):
    """Generates and displays a PyVis graph of the maze."""
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white", notebook=True, directed=False)
    
    nodes = maze_graph.nodes()
    net.add_nodes(nodes)

    for node in net.nodes:
        if node["id"] == start_node:
            node["color"] = "#FF4136" # Red for Start
            node["size"] = 20
        elif node["id"] == end_node:
            node["color"] = "#2ECC40" # Green for End
            node["size"] = 20
        elif node["id"] in treasure_locs:
            node["color"] = "#FFDC00" # Yellow for Treasure
            node["label"] = f"{node['id']}\n({treasure_locs[node['id']]})"
            node["shape"] = "star"
            node["size"] = 25

    for source, targets in maze_graph.graph_dict.items():
        for target, weight in targets.items():
            net.add_edge(source, target, value=weight)

    if agent_path:
        # Highlight the agent's path in blue
        for i in range(len(agent_path) - 1):
            net.add_edge(agent_path[i], agent_path[i+1], color="#0074D9", width=5)

    try:
        net.save_graph("maze_graph.html")
        with open("maze_graph.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except Exception as e:
        st.error(f"Error generating graph visualization: {e}")
        return ""

# --- Streamlit App UI ---
st.set_page_config(layout="wide")
st.title(" solvable Task 2: Treasure Maze 🗺️💎")

# --- Maze Setup ---
maze_data = get_maze_graph()
maze_graph = Graph(maze_data)
nodes_list = sorted(maze_graph.nodes())
treasures_list = get_treasures()

# --- Session State Initialization ---
if 'simulation_run' not in st.session_state:
    st.session_state.simulation_run = False
    st.session_state.start_node = nodes_list[0]
    st.session_state.end_node = nodes_list[-1]
    st.session_state.env = None
    st.session_state.agent = None
    st.session_state.log = []
    st.session_state.final_path = []

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Configuration")
    start_node_select = st.selectbox("Start Node", nodes_list, index=nodes_list.index(st.session_state.start_node))
    end_node_select = st.selectbox("End Node", nodes_list, index=nodes_list.index(st.session_state.end_node))

    if start_node_select == end_node_select:
        st.warning("Start and End nodes cannot be the same.")
    else:
        if st.button("Initialize & Solve Maze"):
            st.session_state.start_node = start_node_select
            st.session_state.end_node = end_node_select
            
            # Create environment and agent
            env = TreasureMazeEnvironment(maze_graph, treasures_list, st.session_state.start_node, st.session_state.end_node)
            agent = TreasureMazeAgent(
                initial_state=st.session_state.start_node,
                maze_graph=maze_graph,
                treasure_locs=env.treasure_locations,
                exit_goal=st.session_state.end_node
            )
            
            # The agent's __call__ method does all the planning
            agent(agent.state)
            
            st.session_state.final_path = agent.seq
            st.session_state.log = agent.log
            
            # Simulate the steps for performance calculation
            if agent.alive and agent.seq:
                for step in agent.seq:
                    if not agent.alive:
                        break
                    env.execute_action(agent, step)

            # Store the final state of the environment and agent
            st.session_state.env = env
            st.session_state.agent = agent
            st.session_state.simulation_run = True
            st.success("Simulation Complete!")

# --- Main Display ---
if not st.session_state.simulation_run:
    st.info("Configure the maze in the sidebar and click 'Initialize & Solve Maze' to begin.")
else:
    col1, col2 = st.columns([2, 1])
    agent = st.session_state.agent
    
    with col1:
        st.subheader("Maze Visualization")
        graph_html = visualize_maze(
            maze_graph,
            st.session_state.start_node,
            st.session_state.end_node,
            st.session_state.env.treasure_locations,
            st.session_state.final_path
        )
        if graph_html:
            components.html(graph_html, height=620)
        
    with col2:
        st.subheader("Agent Control & Log")
        
        st.text_area("Log", value="\n".join(st.session_state.log), height=250)

        st.markdown("---")

        if agent.found_treasure_info:
            st.success(f"**Treasure Found:** {agent.found_treasure_info[1]}")
        else:
            st.warning("No treasure was found on the path.")

        if agent.state == st.session_state.end_node:
            st.success(f"**Exit Reached** at node '{st.session_state.end_node}'!")
        else:
            st.error("Agent did not reach the exit.")
        
        st.metric(label="Final Performance", value=f"{agent.performance:.1f}")

        st.info(f"Path Taken: {' → '.join(st.session_state.final_path)}")

        st.markdown("---")
        st.markdown("**Legend:**")
        st.markdown("- <span style='color:#FF4136'>**Red Node**</span>: Start Point", unsafe_allow_html=True)
        st.markdown("- <span style='color:#2ECC40'>**Green Node**</span>: End Point (Exit)", unsafe_allow_html=True)
        st.markdown("- <span style='color:#FFDC00'>**Yellow Star**</span>: Treasure", unsafe_allow_html=True)
        st.markdown("- <span style='color:#0074D9'>**Blue Path**</span>: Agent's Final Path", unsafe_allow_html=True)

