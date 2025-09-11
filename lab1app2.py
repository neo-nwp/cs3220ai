# Import dependencies
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import json
import streamlit.components.v1 as components #to display the HTML code
import networkx as nx #Networkx for creating graph data
from pyvis.network import Network #to create the graph as an interactive html object

from src.DynastyClass import Dynasty
from src.GameOfThronesGraphClass import GameOfThronesGraph

@st.cache_data
#Caching in Streamlit can significantly improve the performance of your app when working with large data

def data_load(file_name = "data/game-of-thrones-characters-groups.json"):
    #Read the json file using load() and put the json data into a variable.
    with open(file_name) as f:
        json_data = json.load(f)
    return json_data




def showHouses(GameOfThronesHousesObj):
    st.write("Game Of Thrones Houses:")
    markdown_list = ""
    visualisationData={}
    legendData=[]
    for house in GameOfThronesHousesObj:
        markdown_list += f"- {house}: Strength: {house.getStrength()}\n"
        visualisationData[house.name]=house.getStrength()
        legendData.append(house.name)
    st.markdown(markdown_list)
    
    #Configure your x and y values from the dictionary:
    x= list(visualisationData.keys())
    y=list(visualisationData.values())
    
    # Create a Matplotlib figure and axes
    fig, ax = plt.subplots()
    
    # Generate the Seaborn bar plot on the axes
    ax=sns.barplot(x=x,y=y)
    ax.legend(legendData)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1.05, 1))
    ax.set(xlabel='Houses',
        ylabel='Strength (N family members)',
        title='Strength of GameOfThronesHouses')

    plt.xticks(rotation=45)
    
    
    # Display the plot in Streamlit
    st.pyplot(fig)
    


def showHouseMembers(json_data):
    for data in json_data['groups']:
        house=Dynasty(data['name'])
        for character in data['characters']:
            house.append(character)
        st.write(f"{house}. Our members:")
        #print(house)
        #print("Our members:")
        markdown_list = ""
        for person in house:
            markdown_list += f"- {person}\n"
            #print(person)
        st.markdown(markdown_list)
        st.write(f"We have {house.getStrength()} family members!!!")
        #print(f"We have {house.getStrength()} family members!!!")
    


def buildGraphGraphData(GameOfThronesHousesObj):
    
    g = nx.Graph()
    
    N_houses=0
    colorKeys=[]
    
    for house in GameOfThronesHousesObj:
        if house.name!="Include":
            g.add_node(house.name, size=house.getStrength())
            N_houses+=1
            colorKeys.append(house.name)
            
    for house in GameOfThronesHousesObj:
        if house.name!="Include":
            for person in house:
                g.add_node(person)
                
    myEdges=[]
    
          
    for house in GameOfThronesHousesObj:
        if house.name!="Include":
            for person in house:
                if ((person, house.name) not in myEdges) and ((house.name, person) not in myEdges):
                            myEdges.append((person, house.name))                          
                            

                            
    g.add_edges_from(myEdges)   
    return g,N_houses,colorKeys

    
    
    
    

def buildGraph(GameOfThronesHousesObj,gData,N, colorKeys):
    nodeColors=dict(zip(colorKeys, [tuple(int(c*255) for c in cs) for cs in sns.color_palette("husl", N)]))

    # generate the graph
    GameOfThronesNet = Network(
                bgcolor ="#242020",
                font_color = "white",
                height = "1000px",
                width = "100%")
   
    
    GameOfThronesNet.from_nx(gData)
    
    for node in GameOfThronesNet.nodes:
        if node["id"] in GameOfThronesHousesObj:
            # Convert RGB to hexadecimal string
            node["color"] = '#%02x%02x%02x' % nodeColors[node["id"]]
        else:
            for house in GameOfThronesHousesObj: 
                if house.name !="Include":# apple the coloer of the House to this family member
                    if node["id"] in house:
                        node["color"] = '#%02x%02x%02x' % nodeColors[house.name]    
    
    GameOfThronesNet.save_graph('L1_Task2_GameOfThronesHouses.html')
    st.header(f'Lab1. Task2.')
    HtmlFile = open(f'L1_Task2_GameOfThronesHouses.html', 'r', encoding='utf-8')
    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height = 1200,width=1000)
    
    

def main():
    #print("Data loading...")
    json_data=data_load()
    corpusData=json_data['groups']
    GameOfThronesHouses=GameOfThronesGraph(corpusData)
    
    st.title('Task2: infographic of relationships between  characters in the Game of Thrones')
    
    tab1, tab2, tab3 = st.tabs(["Game Of Thrones Houses", "Mambers of Houses", "Graph for Game Of Throne Houses"])
    
    with tab1:
        showHouses(GameOfThronesHouses)
    
    with tab2:
        showHouseMembers(json_data)
        
    with tab3:
        g,N_houses,colorKeys=buildGraphGraphData(GameOfThronesHouses)
        buildGraph(GameOfThronesHouses,g,N_houses,colorKeys)
        
    


        
if __name__ == '__main__':
    main()
    
    
    
    
    
    

    
    
