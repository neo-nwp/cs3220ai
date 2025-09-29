# Import dependencies
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code

import networkx as nx #Networkx for creating graph data
from pyvis.network import Network #to create the graph as an interactive html object



from src.graphClass import Graph
from data.RomaniaMapData import romaniaData
from src.agents import ProblemSolvingNavAgentBFS
from src.naigationEnvironmentClass import NavigationEnvironment

# from src.trivialVacuumEnvironmentClass import TrivialVacuumEnvironment
# from src.agents import RandomVacuumAgent


def drawBtn(e,a):
    option= [e,a]
    st.button("Run One Agent's Step", on_click= AgentStep, args= [option])
    
def AgentStep(opt):
    st.session_state["clicked"] = True
    e,a= opt[0],opt[1]
    
    if e.is_agent_alive(a):
        stepActs=e.step()
        st.success(" Agent decided to do: {}.".format(",".join(stepActs)))
        st.success("RandomVacuumAgent is located at {} now.".format(a.location))
        st.info("Current Agent performance: {}.".format(a.performance))
        st.info("State of the Environment: {}.".format(e.status))
    else:
        st.error("Agent in location {} and it is dead.".format(a.location))
        
    image=getImg(a.location, e.status)
    st.image(image, caption="Agent is here", width="content")
        
def buildGraph(graphData, nodeColorsDict):
    netRomania = Network(
                bgcolor ="#242020",
                font_color = "white",
                height = "750px",
                width = "100%") 
    nodes=graphData.nodes()
    # initialize graph
    g = nx.Graph()
    
    # add the nodes
    g.add_nodes_from(nodes)
    for node in g:
        #node["color"]=nodeColorsDict[node]
        node['color']="white"
    # add the edges
    edges=[]
    for node_source in graphData.nodes():
        for node_target, dist in graphData.get(node_source).items():
            if set((node_source,node_target)) not in edges:
                edges.append(set((node_source,node_target)))                
    g.add_edges_from(edges)
    
    # generate the graph
    netRomania.from_nx(g)
    
    netRomania.save_graph('L3_RomaniaMap.html')
    HtmlFile = open(f'L3_RomaniaMap.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height = 1200,width=1000)
    
    
def makeDefaultColors(dictData):
    nodeColors=dict.fromkeys(dictData.keys(), "white")
    return nodeColors
        
    



def main():
    st.header("Problem Solving Agents: Romania Navigation Problem")
        
    if "clicked" not in st.session_state:
        st.session_state["clicked"] = False
        
    if not st.session_state["clicked"]:
        # Set header title
        st.header("_Initial Env._", divider=True)
        
        romaniaGraph = Graph(romaniaData)
        nodeColors=makeDefaultColors(romaniaGraph.graph_dict)
        
        initState="Arad"
        goalState="Bucharest"
        
        re=NavigationEnvironment(romaniaGraph)
        BFSnavAgent=ProblemSolvingNavAgentBFS(initState,romaniaGraph,goalState)        
                      
        re.add_thing(BFSnavAgent)
        st.header("State of the Environment", divider="red")
        nodeColors[BFSnavAgent.state]="red"
        buildGraph(romaniaGraph, nodeColors) 
        st.info(f"The Agent: {BFSnavAgent.state} with performance {BFSnavAgent}.")
        st.info(f"The Agent goal is: {BFSnavAgent.goal} .")
                
        #drawBtn(e1,a1)
    
            
        
    if st.session_state["clicked"]:
        st.warning("Agent Step Done!")
        
    
    
    
        
        
        
                
            
    
    
    
    
    
    
if __name__ == '__main__':
    main()
    
    

