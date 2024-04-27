import random
import time
import math
import matplotlib.pyplot as plt

def read_tsp_file(file_path):
    coordinates = {}
    tsp_name = ""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    node_coord_section = False
    for line in lines:
        if line.startswith('NAME'):
            tsp_name = line.split(':')[1].strip()
        elif line.startswith('NODE_COORD_SECTION'):
            node_coord_section = True
            continue
        elif line.startswith('EOF'):
            break
        elif node_coord_section:
            node_info = line.strip().split()
            node_id = int(node_info[0])
            x = float(node_info[1])
            y = float(node_info[2])
            coordinates[node_id] = (x, y)

    return tsp_name, coordinates

def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def generate_complete_graph(coordinates):
    G = {}
    for u in coordinates:
        G[u] = {}
        for v in coordinates:
            if u != v:
                distance = euclidean_distance(coordinates[u], coordinates[v])
                G[u][v] = distance
    return G

def plot_graph(coordinates, tour):
    for i in range(len(tour) - 1):
        x1, y1 = coordinates[tour[i]]
        x2, y2 = coordinates[tour[i + 1]]
        plt.plot([x1, x2], [y1, y2], 'bo-')
    plt.show()

def calculate_tour_cost(G, tour):
    tour_cost = sum(G[tour[i]][tour[i+1]] for i in range(len(tour) - 1))
    return tour_cost

def nearest_neighbor_tsp(G, start_node=None):
    start_time = time.time()
    unvisited = set(G.keys())
    if start_node is None:
        current_node = random.choice(list(G.keys()))
    else:
        current_node = start_node
        unvisited.remove(current_node)
    tour = [current_node]

    while unvisited:
        nearest_neighbor = min(unvisited, key=lambda node: G[current_node][node])
        tour.append(nearest_neighbor)
        unvisited.remove(nearest_neighbor)
        current_node = nearest_neighbor

    tour_cost = calculate_tour_cost(G, tour)
    end_time = time.time()
    execution_time = end_time - start_time

    return tour, tour_cost, execution_time

if __name__ == '__main__':
    tsp_file = 'files/pr1002.tsp'
    tsp_name, coordinates = read_tsp_file(tsp_file)
    G = generate_complete_graph(coordinates)

    start_node = 1
    tour, tour_cost, execution_time = nearest_neighbor_tsp(G, start_node)

    print(f'TSP Name: {tsp_name}')
    print(f'Optimal tour: {tour}')
    print(f'Tour cost: {tour_cost}')
    print(f'Execution time: {execution_time} seconds')

    plot_graph(coordinates, tour)