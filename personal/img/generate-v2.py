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

# Position nodes using graphviz layout
pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='dot')

# Define colors for different generations
colors = {
    "Babur": "#ffc0cb",            # Light Pink
    "Humayun": "#ff7f50",          # Coral
    "Akbar I": "#ffff99",          # Light Yellow
    "Jahangir": "#ff6347",         # Tomato
    "Shah Jahan": "#87ceeb",       # Sky Blue
    "Aurangzeb": "#00bfff",        # Deep Sky Blue
    "Muhammad Azam Shah": "#9370db" # Medium Purple
}

# Draw nodes with filled rectangular blocks
nodes = nx.draw_networkx_nodes(G, pos, node_color=[colors.get(node, '#ffffff') for node in G.nodes()], node_size=2000, node_shape='s', linewidths=0.5, edgecolors='black')

# Draw edges
nx.draw_networkx_edges(G, pos, arrows=True, width=1.0, alpha=0.5)

# Draw labels with adjusted font size and weight
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

# Adjust plot limits and turn off axis
plt.xlim([-1.5, 1.5])
plt.ylim([-1.5, 1.5])
plt.axis('off')

# Display the plot
plt.title("Mughal Family Tree")
plt.show()

