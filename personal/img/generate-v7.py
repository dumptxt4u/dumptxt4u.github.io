import matplotlib.pyplot as plt

# Define the family tree relationships
family_tree = {
    "Babur": ["Humayun"],
    "Humayun": ["Akbar I", "Kamran Mirza"],
    "Akbar I": ["Jahangir", "Murad", "Daniyal", "Shahzadi Khanum", "Arjumand Banu Begum", "Hassan"],
    "Jahangir": ["Shah Jahan", "Parviz", "Khusrau", "Jahanara Begum", "Parhez Banu Begum"]
}

# Initialize figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Define positions for each emperor
positions = {
    "Babur": (1, 5),
    "Humayun": (1, 3),
    "Akbar I": (1, 1),
    "Jahangir": (1, -1),
    "Kamran Mirza": (3, 3),
    "Murad": (3, 1),
    "Daniyal": (3, -1),
    "Shahzadi Khanum": (3, -3),
    "Arjumand Banu Begum": (3, -5),
    "Hassan": (3, -7),
    "Shah Jahan": (5, 1),
    "Parviz": (5, -1),
    "Khusrau": (5, -3),
    "Jahanara Begum": (5, -5),
    "Parhez Banu Begum": (5, -7)
}

# Draw rectangles for each emperor
for emperor, pos in positions.items():
    ax.add_patch(plt.Rectangle(pos, 2, 1.5, linewidth=2, edgecolor='black', facecolor='lightblue'))
    ax.text(pos[0] + 1, pos[1] + 0.75, emperor, ha='center', va='center', fontsize=12, fontweight='bold')

# Draw connecting lines for parent-child relationships
for parent, children in family_tree.items():
    parent_pos = positions[parent]
    for child in children:
        child_pos = positions[child]
        ax.plot([parent_pos[0] + 2, child_pos[0]], [parent_pos[1] + 0.75, child_pos[1] + 0.75], 'k-', lw=1)

# Set limits, labels, and turn off axes
ax.set_xlim(0, 8)
ax.set_ylim(-8, 6)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect('equal')
ax.set_title("Subset of Mughal Family Tree")

# Display the plot
plt.show()

