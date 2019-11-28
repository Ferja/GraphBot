import networkx as nx
import data
from haversine import haversine
from fuzzywuzzy import fuzz
from city import City


def distance_between_cities(node1, node2):
    city1 = node1.lat_lon()
    city2 = node2.lat_lon()
    return haversine(city1, city2)


def distance_between_city_lat_lon(node, lat, lon):
    return haversine(node.lat_lon(), (lat, lon))


def get_graph_dist_lat_lon(graph, dist, lat, lon):
    return_graph = graph.copy()
    return_graph.remove_nodes_from([n for n in graph if distance_between_city_lat_lon(n, lat, lon) > dist])
    return return_graph


def get_city_name_country_code(string):
    strings = string.split(",")
    return strings[0].lower(), strings[1].lower()


def get_graph_route(graph, src, dst):
    city_src, country_src = get_city_name_country_code(src)
    city_dst, country_dst = get_city_name_country_code(dst)
    max_ratio_src = 0
    max_ratio_dst = 0
    node_max_ratio_src = None
    node_max_ratio_dst = None
    for node in [n for n in graph if n.country in country_dst or n.country in country_src]:
        if node.country in country_src:
            ratio_aux = fuzz.partial_ratio(node.city, city_src)
            if ratio_aux > max_ratio_src:
                max_ratio_src = ratio_aux
                node_max_ratio_src = node
        if node.country in country_dst:
            ratio_aux = fuzz.partial_ratio(node.city, city_dst)
            if ratio_aux > max_ratio_dst:
                max_ratio_dst = ratio_aux
                node_max_ratio_dst = node
    if node_max_ratio_src is None:
        raise Exception('Bad src')
    if node_max_ratio_dst is None:
        raise Exception('Bad dst')

    return nx.dijkstra_path(graph, node_max_ratio_src, node_max_ratio_dst)


def create_graph(max_distance, min_population):
    graph = nx.Graph()
    data_frame = data.get_cities_data(min_population)
    nodes = set(map(lambda x: City(x.Country, x.City, x.Population, round(x.Latitude, 2), round(x.Longitude, 2)), data_frame.itertuples()))
    cuadrantes = []
    for i in range(36):
        cuadrantes.append([])
        for j in range(18):
            cuadrantes[i].append([])

    for node in nodes:
        x, y = node.cuadrante()
        cuadrantes[x][y].append(node)

    nodes_aux = nodes.copy()
    edges = set()
    for node in nodes:
        nodes_aux.remove(node)
        edges = edges | set(
            map(lambda x: (node, x, distance_between_cities(node, x)), filter(lambda x: distance_between_cities(node, x) <= max_distance, nodes_aux)))

    graph.add_nodes_from(nodes)
    graph.add_weighted_edges_from(edges)
    return graph
