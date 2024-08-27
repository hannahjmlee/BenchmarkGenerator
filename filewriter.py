import numpy as np
import networkx as nx
import random


def generate_text_file(environment, filename):
    with open(filename, 'w') as f:
        # Write the headers
        f.write(f"type octile\n")
        f.write(f"height {environment.shape[0]}\n")
        f.write(f"width {environment.shape[1]}\n")
        f.write(f"map\n")

        # Convert the NumPy array to the specified format and write each row to the file
        for row in environment:
            line = ''.join(['.' if cell else '@' for cell in row])
            f.write(f"{line}\n")


def create_graph_from_array(environment):
    G = nx.grid_2d_graph(environment.shape[0], environment.shape[1])
    
    # Remove edges that connect to obstacles
    for row in range(environment.shape[0]):
        for col in range(environment.shape[1]):
            if not environment[row, col]:  # If it's an obstacle
                G.remove_node((row, col))
    
    return G

def generate_scenario_file(environment, mapname, filename):
    G = create_graph_from_array(environment)
    # Get all valid (free space) points
    free_points = [(r, c) for r in range(environment.shape[0]) for c in range(environment.shape[1]) if environment[r, c]]

    # Randomly shuffle and pair points for start and goal
    random.shuffle(free_points)
    pairs = [(free_points[i], free_points[i+1]) for i in range(0, len(free_points) - 1, 2)]
    
    # Ensure each pair is feasible
    tasks = []
    for start, goal in pairs:
        if nx.has_path(G, start, goal):
            tasks.append((start, goal))
    
    # Write to scenario file
    with open(filename, 'w') as f:
        f.write("version 1\n")
        for i, (start, goal) in enumerate(tasks):
            f.write(f"1 {mapname} {environment.shape[0]} {environment.shape[1]} {start[1]} {start[0]} {goal[1]} {goal[0]} 1.000\n")
