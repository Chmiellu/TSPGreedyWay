import random
import time
import math
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


def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)


def generate_complete_graph(coordinates):
    G = {}
    for u in coordinates:
        G[u] = {}
        for v in coordinates:
            if u != v:
                distance = euclidean_distance(coordinates[u], coordinates[v])
                G[u][v] = distance
    return G


def calculate_tour_cost(G, tour):
    tour_cost = sum(G[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
    return tour_cost


def nearest_neighbor_partitioned_tsp(G, partitions, coordinates):
    start_time = time.time()
    full_tour = []
    total_cost = 0

    for part in partitions:
        min_x, max_x, min_y, max_y = part

        cities_in_partition = [
            node
            for node, coord in coordinates.items()
            if min_x <= coord[0] <= max_x and min_y <= coord[1] <= max_y
        ]
        start_node = cities_in_partition[0]
        tour = [start_node]
        unvisited = cities_in_partition.copy()
        unvisited.remove(start_node)

        while unvisited:
            current_node = tour[-1]
            nearest_neighbor = min(
                unvisited,
                key=lambda node: (
                    G[current_node][node] if node != current_node else float("inf")
                ),
            )
            tour.append(nearest_neighbor)
            unvisited.remove(nearest_neighbor)
            total_cost += G[current_node][nearest_neighbor]

        # Dodaj trasę z aktualnej partycji do całkowitej trasy
        full_tour.extend(tour)

    # Dodaj powrót do punktu startowego
    full_tour.append(start_node)

    end_time = time.time()
    execution_time = end_time - start_time

    return full_tour, total_cost, execution_time


def partition_space(coordinates):

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

    return partitions


def plot_graph(coordinates, tour, tsp_name):
    x_coords = [coord[0] for coord in coordinates.values()]
    y_coords = [coord[1] for coord in coordinates.values()]
    plt.scatter(x_coords, y_coords, color="blue", zorder=2)
    for i in range(len(tour) - 1):
        x1, y1 = coordinates[tour[i]]
        x2, y2 = coordinates[tour[i + 1]]
        plt.plot([x1, x2], [y1, y2], "ro-", zorder=1)
    plt.title(tsp_name)
    plt.show()
    # plt.savefig(os.path.join('plots', f'{tsp_name}.png'))
    # plt.close()


def get_diff_result(problem, total_distance):
    if problem == "lin105.tsp":
        diff = ((total_distance / 14379) - 1) * 100
        return f"{diff:.2f}%"

    elif problem == "tsp225.tsp":
        diff = ((total_distance / 3919) - 1) * 100
        return f"{diff:.2f}%"

    elif problem == "pr1002.tsp":
        diff = ((total_distance / 259045) - 1) * 100
        return f"{diff:.2f}%"

    elif problem == "pr2392.tsp":
        diff = ((total_distance / 378032) - 1) * 100
        return f"{diff:.2f}%"

    elif problem == "rl5934.tsp":
        diff = ((total_distance / 556045) - 1) * 100
        return f"{diff:.2f}%"


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
        tsp_name, coordinates = read_tsp_file(file_path)
        G = generate_complete_graph(coordinates)

        partitions = partition_space(coordinates)

        full_tour, tour_cost, execution_time = nearest_neighbor_partitioned_tsp(
            G, partitions, coordinates
        )
        total_execution_time += execution_time
        diff_result = get_diff_result(os.path.basename(file_path), tour_cost)
        print(f"TSP Name: {tsp_name}")
        print(f"Optimal tour: {full_tour}")
        print(f"Tour cost: {tour_cost}")
        print(f"Difference from optimal: {diff_result}")
        print(f"Execution time: {execution_time} seconds")
        plot_graph(coordinates, full_tour, tsp_name)
    print(f"Total Execution Time: {total_execution_time} seconds")
