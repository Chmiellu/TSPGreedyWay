import random
import time
import networkx as nx
import matplotlib.pyplot as plt

# pytania czy zaczynac od random, czy wyswietlac te wykresy, czemu jest róznica w execution time ,
# realnie dobry wynik to ile?
#kilka razy mozna kliknąć
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

def generate_complete_graph(coordinates):
    G = nx.Graph()
    for node_id, coord in coordinates.items():
        G.add_node(node_id, pos=coord)

    for u in G.nodes():
        for v in G.nodes():
            if u != v:
                distance = ((coordinates[u][0] - coordinates[v][0])**2 + (coordinates[u][1] - coordinates[v][1])**2)**0.5
                G.add_edge(u, v, weight=distance)

    return G

def plot_graph(G, tour):
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500)
    path_edges = [(tour[i], tour[i+1]) for i in range(len(tour) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    plt.show()

def calculate_tour_cost(G, tour):
    tour_cost = sum(G[tour[i]][tour[i+1]]['weight'] for i in range(len(tour) - 1))
    return tour_cost

def nearest_neighbor_tsp(G):
    start_time = time.time()
    unvisited = set(G.nodes)
    current_node = random.choice(list(G.nodes))
    unvisited.remove(current_node)
    tour = [current_node]

    while unvisited:
        nearest_neighbor = min(unvisited, key=lambda node: G[current_node][node]['weight'])
        tour.append(nearest_neighbor)
        unvisited.remove(nearest_neighbor)
        current_node = nearest_neighbor

    tour_cost = calculate_tour_cost(G, tour)
    end_time = time.time()
    execution_time = end_time - start_time

    return tour, tour_cost, execution_time

if __name__ == '__main__':
    tsp_file = 'files/lin105.tsp'
    tsp_name, coordinates = read_tsp_file(tsp_file)
    G = generate_complete_graph(coordinates)

    tour, tour_cost, execution_time = nearest_neighbor_tsp(G)

    print(f'TSP Name: {tsp_name}')
    print(f'Optimal tour: {tour}')
    print(f'Tour cost: {tour_cost}')
    print(f'Execution time: {execution_time} seconds')

    plot_graph(G, tour)