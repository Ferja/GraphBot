import networkx as nx
import data
from haversine import haversine
from city import City


def distance_between_cities(node1, node2):
    city1 = (node1.lat, node1.lon)
    city2 = (node2.lat, node2.lon)
    return haversine(city1, city2)


def create_graph(max_distance, min_population):
    graph = nx.Graph()
    data_frame = data.get_cities_data(min_population)
    nodes = set(map(lambda x: City(x.Country, x.City, x.Population, x.Latitude, x.Longitude), data_frame.itertuples()))
    nodes_aux = nodes.copy()
    edges = set()
    for node in nodes:
        nodes_aux.remove(node)
        edges = edges | set(
            map(lambda x: (node, x, distance_between_cities(node, x)), filter(lambda x: distance_between_cities(node, x) <= max_distance, nodes_aux)))

    graph.add_nodes_from(nodes)
    graph.add_weighted_edges_from(edges)

    return graph
