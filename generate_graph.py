import networkx as nx
from pyvis.network import Network
import seaborn as sns
import json
import os

# --- OOP Classes ---
class Dynasty:
    def __init__(self, name):
        self._name = name
        self.characters = []
    @property
    def name(self): return self._name
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip(): raise ValueError("Name cannot be an empty string.")
        self._name = value
    def append(self, ch):
        if not isinstance(ch, str): raise TypeError("Character must be a string.")
        self.characters.append(ch)
    def __iter__(self):
        for person in self.characters: yield person
    def __contains__(self, ch): return ch in self.characters
    def __str__(self): return f"This is a House of {self.name}!"
    def getStrength(self): return len(self.characters)

class GameOfThronesGraph:
    def __init__(self, corpus):
        self.houses = {}
        for data_item in corpus:
            house_name = data_item['name']
            house_obj = Dynasty(house_name)
            for character in data_item['characters']: house_obj.append(character)
            self.houses[house_name] = house_obj
    def __iter__(self):
        for house in self.houses.values(): yield house
    def __contains__(self, h): return h in self.houses

# --- Main script to generate graph ---
def create_interactive_graph():
    """Loads data, processes it with classes, and generates an HTML graph."""
    
    # Updated file path to match your folder structure
    json_path = "data/game-of-thrones-characters-groups.json"
    if not os.path.exists(json_path):
        print(f"Error: Data file not found at {json_path}")
        return

    with open(json_path) as f:
        json_data = json.load(f)
    
    corpusData = json_data['groups']
    GameOfThronesHouses = GameOfThronesGraph(corpusData)

    g = nx.Graph()
    for house in GameOfThronesHouses:
        if house.name != "Include":
            g.add_node(house.name, size=house.getStrength(), color='grey')
            for person in house:
                g.add_node(person, size=10)

    myEdges = [(person, house.name) for house in GameOfThronesHouses if house.name != "Include" for person in house]
    g.add_edges_from(myEdges)

    GameOfThronesNet = Network(
        bgcolor="#242020",
        font_color="white",
        height="1000px",
        width="100%",
        notebook=False,
        cdn_resources="remote"
    )
    GameOfThronesNet.from_nx(g)
    
    colorKeys = [h.name for h in GameOfThronesHouses if h.name != "Include"]
    palette = sns.color_palette("husl", len(colorKeys))
    nodeColors = dict(zip(colorKeys, ['#%02x%02x%02x' % tuple(int(c * 255) for c in cs) for cs in palette]))

    for node in GameOfThronesNet.nodes:
        node_id = node["id"]
        if node_id in GameOfThronesHouses:
            node["color"] = nodeColors.get(node_id, 'grey')
        else:
            for house in GameOfThronesHouses:
                if node_id in house:
                    node["color"] = nodeColors.get(house.name, 'grey')
                    break

    output_filename = "L1_Task2_GameOfThronesHouses.html"
    GameOfThronesNet.show(output_filename, notebook=False)
    print(f"Successfully generated {output_filename}")

if __name__ == "__main__":
    create_interactive_graph()