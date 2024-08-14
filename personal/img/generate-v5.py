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
    "Kamran Mirza": (1, 4),  # Adding Kamran Mirza to positions
    "Murad": (2, 2),         # Adding Murad to positions
    "Daniyal": (2, 3),       # Adding Daniyal to positions
    "Shahzadi Khanum": (2, 4), # Adding Shahzadi Khanum to positions
    "Arjumand Banu Begum": (2, 5), # Adding Arjumand Banu Begum to positions
    "Hassan": (2, 6),        # Adding Hassan to positions
    "Parviz": (2, 0),        # Adding Parviz to positions
    "Khusrau": (2, -1),      # Adding Khusrau to positions
    "Parhez Banu Begum": (2, -2), # Adding Parhez Banu Begum to positions
    "Dara Shikoh": (4, 5),   # Adding Dara Shikoh to positions
    "Roshanara Begum": (4, 4), # Adding Roshanara Begum to positions
    "Murad Bakhsh": (4, 3),  # Adding Murad Bakhsh to positions
    "Gauhar-un-Nissa Begum": (4, 2), # Adding Gauhar-un-Nissa Begum to positions
    "Muhammad Sultan": (4, 1), # Adding Muhammad Sultan to positions
    "Muhammad Azam": (4, 0), # Adding Muhammad Azam to positions
    "Zeb-un-Nissa": (4, -1), # Adding Zeb-un-Nissa to positions
    "Zinat-un-Nissa": (4, -2), # Adding Zinat-un-Nissa to positions
    "Sultan Muhammad Akbar": (4, -3), # Adding Sultan Muhammad Akbar to positions
    "Sultan Muhammad Azam": (4, -4), # Adding Sultan Muhammad Azam to positions
    "Sultan Muhammad Ahmad Shah Bahadur": (4, -5), # Adding Sultan Muhammad Ahmad Shah Bahadur to positions
    "Bhim Chand": (6, 1),    # Adding Bhim Chand to positions
    "Umaid Singh": (6, 0),   # Adding Umaid Singh to positions
    "Chhattar Singh": (6, -1) # Adding Chhattar Singh to positions
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
ax.set_xlim(0, 8)
ax.set_ylim(-6, 8)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect('equal')
ax.set_title("Mughal Family Tree")

# Display the plot
plt.show()

