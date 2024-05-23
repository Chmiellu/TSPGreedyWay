import time
import numpy as np
import os
import matplotlib.pyplot as plt

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

def chebyshev_distance(coord1, coord2):
    return max(abs(coord1[0] - coord2[0]), abs(coord1[1] - coord2[1]))

def generate_distance_matrix_for_partition(partition_nodes, coordinates):
    num_nodes = len(partition_nodes)
    distance_matrix = np.zeros((num_nodes, num_nodes))
    node_to_index = {node_id: idx for idx, node_id in enumerate(partition_nodes)}

    for i, node_id1 in enumerate(partition_nodes):
        for j, node_id2 in enumerate(partition_nodes):
            if i != j:
                distance_matrix[i][j] = chebyshev_distance(coordinates[node_id1], coordinates[node_id2])
            else:
                distance_matrix[i][j] = float('inf')

    return distance_matrix, node_to_index

def partition_space(coordinates):
    min_x = min(coord[0] for coord in coordinates.values())
    max_x = max(coord[0] for coord in coordinates.values())
    min_y = min(coord[1] for coord in coordinates.values())
    max_y = max(coord[1] for coord in coordinates.values())

    partitions = []
    x_step = (max_x - min_x) / 4
    y_step = (max_y - min_y) / 4

    for i in range(4):
        for j in range(4):
            min_x_part = min_x + i * x_step
            max_x_part = min_x + (i + 1) * x_step
            min_y_part = min_y + j * y_step
            max_y_part = min_y + (j + 1) * y_step
            partitions.append((min_x_part, max_x_part, min_y_part, max_y_part))

    return partitions

def nearest_neighbor_partitioned_tsp(file_path):
    start_time = time.time()

    tsp_name, coordinates = read_tsp_file(file_path)
    partitions = partition_space(coordinates)

    full_tour = []
    total_cost = 0
    global_node_to_index = {node_id: idx for idx, node_id in enumerate(coordinates.keys())}

    for part in partitions:
        min_x, max_x, min_y, max_y = part

        cities_in_partition = [
            node_id
            for node_id, coord in coordinates.items()
            if min_x <= coord[0] <= max_x and min_y <= coord[1] <= max_y
        ]

        if not cities_in_partition:
            continue

        distance_matrix, node_to_index = generate_distance_matrix_for_partition(cities_in_partition, coordinates)

        start_node = cities_in_partition[0]
        tour = [start_node]
        unvisited = set(cities_in_partition)
        unvisited.remove(start_node)

        while unvisited:
            current_node = tour[-1]
            idx_current_node = node_to_index[current_node]
            nearest_neighbor = min(
                unvisited,
                key=lambda node_id: distance_matrix[idx_current_node][node_to_index[node_id]],
            )
            tour.append(nearest_neighbor)
            unvisited.remove(nearest_neighbor)
            total_cost += distance_matrix[idx_current_node][node_to_index[nearest_neighbor]]

        full_tour.extend(tour)

    if full_tour:
        total_cost += chebyshev_distance(coordinates[full_tour[-1]], coordinates[full_tour[0]])
        full_tour.append(full_tour[0])

    end_time = time.time()
    execution_time = end_time - start_time

    return tsp_name, coordinates, full_tour, total_cost, execution_time

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

def plot_tour(tsp_name, coordinates, tour, output_dir):
    x_coords = [coordinates[node][0] for node in tour]
    y_coords = [coordinates[node][1] for node in tour]

    plt.figure(figsize=(10, 10))
    plt.plot(x_coords, y_coords, 'o-', markersize=5, label='Tour Path')
    plt.title(f'Tour for {tsp_name}')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.grid(True)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plot_path = os.path.join(output_dir, f"{tsp_name}_tour.png")
    plt.savefig(plot_path)
    plt.close()

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
        tsp_name, coordinates, full_tour, tour_cost, execution_time = nearest_neighbor_partitioned_tsp(
            file_path
        )
        total_execution_time += execution_time
        diff_result = get_diff_result(os.path.basename(file_path), tour_cost)
        print(f"TSP Name: {tsp_name}")
        print(f"Tour cost: {tour_cost}")
        print(f"Difference from optimal: {diff_result}")
        print(f"Execution time: {execution_time} seconds")

        plot_tour(tsp_name, coordinates, full_tour, 'plots')

    print(f"Total Execution Time: {total_execution_time} seconds")
