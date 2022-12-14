from typing import Dict, List, Tuple

from util import read_input_as_string_grid, enumerate_matrix, get_neighbour_coords_in_matrix


class Vertex:
    def __init__(self, name):
        self.name = name
        self.outgoing_edges: Dict[Vertex, int] = {}
        self.incoming_edges: Dict[Vertex, int] = {}
        # self.distance = 1_000_000
        self.distance_to_node: Dict[Vertex, int] = {self: 0}
        self.path_to_node: Dict[Vertex, List[Vertex]] = {self: [self]}
        self.visited = False
        self.previous = None

    def get_distance_to_node(self, node):
        return self.distance_to_node.get(node, 10_000_000)

    def add_neighbor(self, neighbor, weight=0):
        self.outgoing_edges[neighbor] = weight
        neighbor.incoming_edges[self] = weight

    def __repr__(self):
        return self.name

    def __str__(self):
        return f'{self.name} outgoing edges: {[x.name for x in self.outgoing_edges]}'


class Graph:
    def __init__(self):
        self.vertices = set()
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vertices)

    def add_vertex(self, name: str):
        self.num_vertices += 1
        new_vertex = Vertex(name)
        self.vertices.add(new_vertex)
        return new_vertex

    def add_edge(self, frm: Vertex, to: Vertex, cost=0):
        frm.add_neighbor(to, cost)


def shortest(vertex):
    current = vertex
    path = [vertex.name]
    while current.previous:
        current = current.previous
        path.append(current.name)
    return path


def dijkstra2(graph: Graph, start: Vertex, reverse=False):
    current_node = start
    while True:
        current_node.visited = True
        edges_to_search = current_node.incoming_edges if reverse else current_node.outgoing_edges
        for next_node, edge_distance in edges_to_search.items():
            next_node: Vertex
            if next_node.visited:
                continue
            current_distance = start.get_distance_to_node(current_node)
            new_distance = current_distance + edge_distance
            if new_distance < start.get_distance_to_node(next_node):
                start.distance_to_node[next_node] = new_distance
                path = start.path_to_node[current_node] + [next_node]
                start.path_to_node[next_node] = path
                for i, node_in_path in enumerate(path):
                    node_in_path.path_to_node[next_node] = path[i:]
                    node_in_path.distance_to_node[next_node] = new_distance - start.distance_to_node[node_in_path]
        unvisited_queue = sorted([v for v in graph if not v.visited], key=lambda v: start.get_distance_to_node(v))
        if len(unvisited_queue) == 0:
            break
        current_node = unvisited_queue[0]


def dijkstra(graph, start, reverse=False):
    start.distance = 0
    unvisited_queue = sorted(list(graph), key=lambda v: v.distance)
    while len(unvisited_queue) > 0:
        current_node = unvisited_queue[0]
        current_node.visited = True
        edges_to_search = current_node.incoming_edges if reverse else current_node.outgoing_edges
        for next_node in edges_to_search.keys():
            if next_node.visited:
                continue
            new_dist = current_node.distance + edges_to_search[next_node]
            if new_dist < next_node.distance:
                next_node.distance = new_dist
                next_node.previous = current_node
        unvisited_queue = sorted([v for v in graph if not v.visited], key=lambda v: v.distance)


def get_height(value):
    letter = value[0]
    return ord({'S': 'a', 'E': 'z'}.get(letter, letter))


def get_height_diff(value1, value2):
    return get_height(value2) - get_height(value1)


def can_go_from_node_to_node(value1, value2):
    return get_height_diff(value1, value2) <= 1


def parse():
    g = Graph()
    grid = read_input_as_string_grid()
    node_map: Dict[Tuple[int, int], Vertex] = {}
    for (y, x), node in enumerate_matrix(grid):
        node_map[(y, x)] = g.add_vertex(f'{node}({x},{y})')
    for (y, x), node in enumerate_matrix(grid):
        vertex = node_map[(y, x)]
        for (y_n, x_n) in get_neighbour_coords_in_matrix(grid, (y, x)):
            neighbour_vertex = node_map[(y_n, x_n)]
            if can_go_from_node_to_node(vertex.name, neighbour_vertex.name):
                g.add_edge(vertex, neighbour_vertex, 1)
            if can_go_from_node_to_node(neighbour_vertex.name, vertex.name):
                g.add_edge(neighbour_vertex, vertex, 1)
    return g


def part1():
    g = parse()
    start = list({v for v in g.vertices if 'S' in v.name})[0]
    dijkstra(g, start)
    target = list({v for v in g.vertices if 'E' in v.name})[0]
    path = shortest(target)
    return len(path) - 1


def part2():
    g = parse()
    start = list({v for v in g.vertices if 'E' in v.name})[0]
    dijkstra(g, start, reverse=True)
    targets = list({v for v in g.vertices if 'a' in v.name or 'S' in v.name})
    min_distance = None
    for target in targets:
        path = shortest(target)
        distance = len(path) - 1
        if distance == 0:
            continue
        if min_distance is None or distance < min_distance:
            min_distance = distance
    return min_distance


if __name__ == '__main__':
    g = parse()
    start = list({v for v in g.vertices if 'S' in v.name})[0]
    dijkstra2(g, start)
    # print(part1())
    # print(part2())
