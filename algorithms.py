def dijkstra(start_node, get_neighbours_of_node, get_cost_of_node):
    visited = set()
    to_visit = set()
    distances = {start_node: 0}
    paths = {start_node: []}
    node = start_node
    while True:
        current_distance = distances[node]
        current_path = paths[node]
        neighbours = set(get_neighbours_of_node(node))
        for neighbour in neighbours:
            known_distance = distances.get(neighbour)
            distance_via_current = current_distance + get_cost_of_node(neighbour)
            if known_distance is None or distance_via_current < known_distance:
                distances[neighbour] = distance_via_current
                paths[neighbour] = current_path + [neighbour]
        visited.add(node)
        to_visit = to_visit.union(neighbours).difference(visited)
        if len(to_visit) == 0:
            return distances, paths
        node = min(to_visit, key=lambda t: distances[t])


def dijkstra_distance(start_node, get_neighbours_of_node, get_cost_of_node):
    visited = set()
    to_visit = set()
    distances = {start_node: 0}
    node = start_node
    while True:
        current_distance = distances[node]
        neighbours = set(get_neighbours_of_node(node))
        for neighbour in neighbours:
            known_distance = distances.get(neighbour)
            distance_via_current = current_distance + get_cost_of_node(neighbour)
            if known_distance is None or distance_via_current < known_distance:
                distances[neighbour] = distance_via_current
        visited.add(node)
        to_visit = to_visit.union(neighbours).difference(visited)
        if len(to_visit) == 0:
            return distances
        node = min(to_visit, key=lambda t: distances[t])
