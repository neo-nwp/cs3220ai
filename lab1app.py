# Import dependencies
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code
import pandas as pd
import networkx as nx
from pyvis.network import Network

def data_load():
    flights_df = pd.read_csv("data/flights.csv", usecols = ["ORIGIN_AIRPORT", "DESTINATION_AIRPORT","YEAR"])
    print(f"Original dataset size: {flights_df.size}") #this dataset is quite big 
    flights_df1=flights_df[(flights_df.DESTINATION_AIRPORT.str.len()<=3)&(flights_df.ORIGIN_AIRPORT.str.len()<=3)]
    print(f"Working dataset size: {flights_df1.size}") #this dataset is quite big
    return flights_df1


def data_proc(df):
    df_between_airports = df.groupby(by=["ORIGIN_AIRPORT", "DESTINATION_AIRPORT"]).count().reset_index()
    df_between_airports.rename(columns={"YEAR":"N_fligths"}, inplace=True)
    df_between_airports.sort_values(by="N_fligths", ascending=False, inplace=True)
    df_between_airports['Perc']=df_between_airports["N_fligths"]/df_between_airports.shape[0] #the Nflights has been normalized 
    return df_between_airports

def makeEdgeTitle(x):
    return "N_flights: "+str(x)

def setGraphData(df):
    node_sizes=df.groupby("ORIGIN_AIRPORT").count()["N_fligths"]
    # get all the nodes from the two columns
    nodes = list(set([*df['ORIGIN_AIRPORT'], 
                  *df['DESTINATION_AIRPORT']
                 ]))
    # extract the size of each airport
    values = [int(node_sizes[node]) for node in nodes]
    df["edge_titles"]=df["N_fligths"].apply(makeEdgeTitle)
    # extract the edges between airports
    edges = df.loc[:,["ORIGIN_AIRPORT", "DESTINATION_AIRPORT", "edge_titles"]].values.tolist()
    edges_width=df.Perc.values.tolist()
    
    return nodes,values,edges,edges_width
    
    

def buildGraph(nodes,values,edges,edges_width):
    netFlights = Network(heading="Lab1. Building Interactive Network of flights",
                bgcolor ="#242020",
                font_color = "white",
                height = "1000px",
                width = "100%",
                directed = True,
                filter_menu=True)
    # add the nodes, the value is to set the size of the nodes
    netFlights.add_nodes(nodes, value = values)
    # add the edges
    netFlights.add_edges(edges)
    netFlights.show("L1_Network_of_flights.html", notebook=False)
    

def main():
    flights_df=data_load()
    df_between_airports=data_proc(flights_df)
    nodes,values,edges,edges_width=setGraphData(df_between_airports)
    
    # Set header title
    st.title('Network Graph Visualization - lab1. Example')
    origin_airports=df_between_airports['ORIGIN_AIRPORT'].unique().tolist()
    origin_airports.sort()
    # Implement multiselect dropdown menu for option selection
    selected_origin_airports = st.multiselect('Select origin airports to visualize', origin_airports)
    # Set info message on initial site load
    if len(selected_origin_airports) == 0:
        st.text('Please choose at least 1 origin airport to get started')
        # Create network graph when user selects >= 1 item
    else:
        df_select = flights_df.loc[flights_df['ORIGIN_AIRPORT'].isin(selected_origin_airports)]
        df_select = df_select.reset_index(drop=True)
        st.dataframe(df_select, hide_index=True)
        
if __name__ == '__main__':
    main()
    
    
    
    
    
    

    
    
