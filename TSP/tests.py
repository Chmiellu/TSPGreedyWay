import time
import math
import numpy as np
import os

def read_tsp_file(file_path):
    coordinates = {}
    tsp_name = ""
    with open(file_path, "r") as file:
        lines = file.readlines()

    node_coord_section = False
    for line in lines:
        if line.startswith("NAME"):
            tsp_name = line.split(":")[1].strip()
        elif line.startswith("NODE_COORD_SECTION"):
            node_coord_section = True
            continue
        elif line.startswith("EOF"):
            break
        elif node_coord_section:
            node_info = line.strip().split()
            node_id = int(node_info[0])
            x = float(node_info[1])
            y = float(node_info[2])
            coordinates[node_id] = (x, y)

    return tsp_name, coordinates

def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

def calculate_tour_cost(tour, distance_matrix):
    total_cost = 0
    num_nodes = len(tour)
    for i in range(num_nodes - 1):
        total_cost += distance_matrix[tour[i]][tour[i + 1]]
    total_cost += distance_matrix[tour[-1]][tour[0]]
    return total_cost

def two_opt(tour, distance_matrix, max_time=50):
    best = tour
    improved = True
    start_time = time.time()
    while improved and time.time() - start_time < max_time:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour)):
                if j - i == 1:
                    continue
                new_tour = tour[:i] + tour[i:j][::-1] + tour[j:]
                if calculate_tour_cost(new_tour, distance_matrix) < calculate_tour_cost(best, distance_matrix):
                    best = new_tour
                    improved = True
        tour = best
    return best

def greedy_tsp(coordinates, max_time=60):
    start_time = time.time()

    num_nodes = len(coordinates)
    node_to_index = {node_id: idx for idx, node_id in enumerate(coordinates.keys())}
    index_to_node = {idx: node_id for node_id, idx in node_to_index.items()}
    distance_matrix = np.zeros((num_nodes, num_nodes))
    for node_id1, coord1 in coordinates.items():
        for node_id2, coord2 in coordinates.items():
            idx1 = node_to_index[node_id1]
            idx2 = node_to_index[node_id2]
            distance_matrix[idx1][idx2] = euclidean_distance(coord1, coord2)

    tour = []
    unvisited = set(range(num_nodes))

    while unvisited and time.time() - start_time < max_time:
        current_node = unvisited.pop()
        group_tour = [current_node]
        group_distance_matrix = distance_matrix[group_tour]
        while unvisited and time.time() - start_time < max_time:
            nearest_neighbor = min(
                unvisited, key=lambda idx: group_distance_matrix[0][idx]
            )
            group_tour.append(nearest_neighbor)
            unvisited.remove(nearest_neighbor)
            group_distance_matrix = distance_matrix[group_tour]
        tour.extend(group_tour)

    # Apply 2-opt optimization with limited time
    tour = two_opt(tour, distance_matrix, max_time=60)

    total_cost = calculate_tour_cost(tour, distance_matrix)

    end_time = time.time()
    execution_time = end_time - start_time

    return [index_to_node[idx] for idx in tour], total_cost, execution_time

def get_diff_result(problem, total_distance):
    optimal_distances = {
        "lin105.tsp": 14379,
        "tsp225.tsp": 3919,
        "pr1002.tsp": 259045,
        "pr2392.tsp": 378032,
        "rl5934.tsp": 556045
    }

    if problem in optimal_distances:
        optimal_distance = optimal_distances[problem]
        diff = ((total_distance / optimal_distance) - 1) * 100
        return f"{diff:.2f}%"
    else:
        return "Unknown problem"

def process_tsp_file(file_path):
    tsp_name, coordinates = read_tsp_file(file_path)
    tour, tour_cost, execution_time = greedy_tsp(coordinates)
    return tsp_name, tour, tour_cost, execution_time

if __name__ == "__main__":
    total_execution_time = 0
    files = [
        "files/lin105.tsp",
        "files/tsp225.tsp",
        "files/pr1002.tsp",
        "files/pr2392.tsp",
        "files/rl5934.tsp",
    ]
    for file_path in files:
        tsp_name, tour, tour_cost, execution_time = process_tsp_file(file_path)
        total_execution_time += execution_time
        diff_result = get_diff_result(os.path.basename(file_path), tour_cost)
        print(f"TSP Name: {tsp_name}")
        print(f"Tour: {tour}")
        print(f"Tour cost: {tour_cost}")
        print(f"Difference from optimal: {diff_result}")
        print(f"Execution time: {execution_time} seconds")
    print(f"Total Execution Time: {total_execution_time} seconds")
