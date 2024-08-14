import matplotlib.pyplot as plt
import networkx as nx

# Define the family tree relationships
family_tree = {
    "Babur": ["Humayun"],
    "Humayun": ["Akbar I", "Kamran Mirza"],
    "Akbar I": ["Jahangir", "Murad", "Daniyal", "Shahzadi Khanum", "Arjumand Banu Begum", "Hassan"],
    "Jahangir": ["Shah Jahan", "Parviz", "Khusrau", "Jahanara Begum", "Parhez Banu Begum"],
    "Shah Jahan": ["Dara Shikoh", "Jahanara Begum", "Shah Shuja", "Roshanara Begum", "Aurangzeb", "Murad Bakhsh", "Gauhar-un-Nissa Begum", "Muhammad Sultan"],
    "Aurangzeb": ["Muhammad Azam Shah", "Muazzam", "Zeb-un-Nissa", "Zinat-un-Nissa", "Sultan Muhammad Akbar", "Sultan Muhammad Azam", "Sultan Muhammad Akbar", "Sultan Muhammad Ahmad Shah Bahadur"],
    "Muhammad Azam Shah": ["Bhim Chand", "Umaid Singh", "Chhattar Singh"]
}

# Create a directed graph
G = nx.DiGraph()

# Add edges to the graph based on family tree
for parent, children in family_tree.items():
    for child in children:
        G.add_edge(parent, child)

# Define colors for different generations
colors = {
    0: 'lightblue',   # Babur
    1: 'lightgreen',  # Humayun
    2: 'lightcoral',  # Akbar I, Jahangir
    3: 'lightskyblue',  # Shah Jahan, Aurangzeb, Muhammad Azam Shah
    4: 'lightpink'   # Descendants of Shah Jahan, Aurangzeb, Muhammad Azam Shah
}

# Function to assign colors to nodes based on generation
def get_node_color(node):
    for generation, emperors in enumerate([["Babur"], ["Humayun"], ["Akbar I", "Jahangir"], ["Shah Jahan", "Aurangzeb", "Muhammad Azam Shah"], ["Descendants of Shah Jahan, Aurangzeb, Muhammad Azam Shah"]]):
        if node in emperors:
            return colors[generation]
    return 'white'  # Default color

# Position nodes using graphviz layout
pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='dot')

# Draw nodes and edges with colors
nx.draw_networkx_nodes(G, pos, node_color=[get_node_color(node) for node in G.nodes()], node_size=500)
nx.draw_networkx_edges(G, pos, arrows=True, width=1.0, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

# Display the plot
plt.title("Mughal Family Tree")
plt.axis('off')
plt.show()

