import time
import math
import numpy as np


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


def nearest_neighbor_partitioned_tsp(coordinates):
    start_time = time.time()

    # Generate distance matrix
    num_nodes = len(coordinates)
    node_to_index = {node_id: idx for idx, node_id in enumerate(coordinates.keys())}
    distance_matrix = np.zeros((num_nodes, num_nodes))
    for node_id1, coord1 in coordinates.items():
        for node_id2, coord2 in coordinates.items():
            idx1 = node_to_index[node_id1]
            idx2 = node_to_index[node_id2]
            distance_matrix[idx1][idx2] = euclidean_distance(coord1, coord2)

    # Partition the space
    min_x = min(coord[0] for coord in coordinates.values())
    max_x = max(coord[0] for coord in coordinates.values())
    min_y = min(coord[1] for coord in coordinates.values())
    max_y = max(coord[1] for coord in coordinates.values())

    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2

    partitions = []
    for i in range(2):
        for j in range(2):
            min_x_part = min_x if i == 0 else mid_x
            max_x_part = mid_x if i == 0 else max_x
            min_y_part = min_y if j == 0 else mid_y
            max_y_part = mid_y if j == 0 else max_y
            partitions.append((min_x_part, max_x_part, min_y_part, max_y_part))

    # Nearest Neighbor TSP for each partition
    full_tour = []
    total_cost = 0

    for part in partitions:
        min_x, max_x, min_y, max_y = part

        cities_in_partition = [
            node_id
            for node_id, coord in coordinates.items()
            if min_x <= coord[0] <= max_x and min_y <= coord[1] <= max_y
        ]

        start_node = cities_in_partition[0]
        tour = [start_node]
        unvisited = set(cities_in_partition)
        unvisited.remove(start_node)

        while unvisited:
            current_node = tour[-1]
            idx_current_node = node_to_index[current_node]
            nearest_neighbor = min(
                unvisited,
                key=lambda node_id: distance_matrix[idx_current_node][
                    node_to_index[node_id]
                ],
            )
            tour.append(nearest_neighbor)
            unvisited.remove(nearest_neighbor)
            total_cost += distance_matrix[idx_current_node][
                node_to_index[nearest_neighbor]
            ]

        full_tour.extend(tour)

    idx_last_node = node_to_index[full_tour[-1]]
    idx_first_node = node_to_index[full_tour[0]]
    total_cost += distance_matrix[idx_last_node][idx_first_node]
    full_tour.append(full_tour[0])

    end_time = time.time()
    execution_time = end_time - start_time

    return full_tour, total_cost, execution_time


def process_tsp_file(file_path):
    tsp_name, coordinates = read_tsp_file(file_path)
    full_tour, tour_cost, execution_time = nearest_neighbor_partitioned_tsp(coordinates)
    return tsp_name, tour_cost, execution_time


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
        tsp_name, tour_cost, execution_time = process_tsp_file(file_path)
        total_execution_time += execution_time
        print(f"TSP Name: {tsp_name}")
        print(f"Tour cost: {tour_cost}")
        print(f"Execution time: {execution_time} seconds")
    print(f"Total Execution Time: {total_execution_time} seconds")
