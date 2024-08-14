import matplotlib.pyplot as plt

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

# Initialize figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

# Define positions for each emperor
positions = {
    "Babur": (1, 7),
    "Humayun": (1, 5),
    "Akbar I": (1, 3),
    "Jahangir": (1, 1),
    "Shah Jahan": (3, 5),
    "Aurangzeb": (3, 1),
    "Muhammad Azam Shah": (5, 1),
    "Kamran Mirza": (1, 4)  # Adding Kamran Mirza to positions
}

# Draw rectangles for each emperor
for emperor, pos in positions.items():
    ax.add_patch(plt.Rectangle(pos, 1, 1, linewidth=2, edgecolor='black', facecolor='lightblue'))
    ax.text(pos[0] + 0.5, pos[1] + 0.5, emperor, ha='center', va='center', fontsize=12, fontweight='bold')

# Draw connecting lines for parent-child relationships
for parent, children in family_tree.items():
    parent_pos = positions[parent]
    for child in children:
        child_pos = positions[child]
        ax.plot([parent_pos[0] + 0.5, child_pos[0] + 0.5], [parent_pos[1], child_pos[1] + 1], 'k-', lw=1)

# Set limits, labels, and turn off axes
ax.set_xlim(0, 6)
ax.set_ylim(0, 8)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect('equal')
ax.set_title("Mughal Family Tree")

# Display the plot
plt.show()

