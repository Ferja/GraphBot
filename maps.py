from staticmap import StaticMap, CircleMarker, Line
import random
import graphs


def draw_map_plotpop(graph, dist, lat, lon):
    fitxer = "%d.png" % random.randint(1000000, 9999999)
    reduced_graph = graphs.get_graph_dist_lat_lon(graph, dist, lat, lon)
    mapa = StaticMap(500, 500)
    for node in reduced_graph:
        mapa.add_marker(CircleMarker(node.lon_lat(), 'blue', node.population/1000000))
    imatge = mapa.render()
    imatge.save(fitxer)
    return fitxer


def draw_map_plotgraph(graph, dist, lat, lon):
    fitxer = "%d.png" % random.randint(1000000, 9999999)
    reduced_graph = graphs.get_graph_dist_lat_lon(graph, dist, lat, lon)
    mapa = StaticMap(500, 500)
    for node in reduced_graph:
        mapa.add_marker(CircleMarker(node.lon_lat(), 'blue', 5))
    for (u, v) in reduced_graph.edges():
        mapa.add_line(Line((u.lon_lat(), v.lon_lat()), 'blue', 1))
    imatge = mapa.render()
    imatge.save(fitxer)
    return fitxer


def draw_map_route(graph, src, dst):
    fitxer = "%d.png" % random.randint(1000000, 9999999)
    route_node_list = graphs.get_graph_route(graph, src, dst)
    mapa = StaticMap(500, 500)
    mapa.add_marker(CircleMarker(route_node_list[0].lon_lat(), 'blue', 5))
    for i in range(len(route_node_list) - 1):
        mapa.add_marker(CircleMarker(route_node_list[i+1].lon_lat(), 'blue', 5))
        mapa.add_line(Line((route_node_list[i].lon_lat(), route_node_list[i+1].lon_lat()), 'blue', 1))
    imatge = mapa.render()
    imatge.save(fitxer)
    return fitxer
