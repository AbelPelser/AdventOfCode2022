from typing import Dict, List, Tuple

from bisect import insort
from sortedcontainers import SortedSet
from util import read_input_as_string_grid, enumerate_matrix, get_neighbour_coords_in_matrix


class Vertex:
    def __init__(self, name):
        self.name = name
        self.outgoing_edges: Dict[Vertex, int] = {}
        self.incoming_edges: Dict[Vertex, int] = {}
        self.distance = 1_000_000
        self.distance_to_node: Dict[Vertex, int] = {self: 0}
        self.path_to_node: Dict[Vertex, List[Vertex]] = {self: [self]}
        self.visited = False
        self.previous = None

    def get_distance_to_node(self, node):
        return self.distance_to_node.get(node, 10_000_000)

    def add_neighbor(self, neighbor, weight=0):
        self.outgoing_edges[neighbor] = weight
        neighbor.incoming_edges[self] = weight

    def __lt__(self, other):
        return self.distance < other.distance

    def __repr__(self):
        return self.name

    def __str__(self):
        return f'{self.name} outgoing edges: {[x.name for x in self.outgoing_edges]}'


class Graph:
    def __init__(self):
        self.vertices = set()

    def __iter__(self):
        return iter(self.vertices)

    def add_vertex(self, name: str):
        new_vertex = Vertex(name)
        self.vertices.add(new_vertex)
        return new_vertex

    def add_edge(self, frm: Vertex, to: Vertex, cost=0):
        frm.add_neighbor(to, cost)

    def get_nodes_by_name(self, name):
        return [v for v in self.vertices if name in v.name]


def shortest(vertex):
    current = vertex
    path = [vertex.name]
    while current.previous:
        current = current.previous
        path.append(current.name)
    return path


def dijkstra(start: Vertex, reverse=False):
    start.distance = 0
    unvisited_queue: SortedSet = SortedSet(start.outgoing_edges.keys())
    while len(unvisited_queue) > 0:
        current_node = unvisited_queue.pop(0)
        current_node.visited = True
        edges_to_search = current_node.incoming_edges if reverse else current_node.outgoing_edges
        for next_node in edges_to_search.keys():
            if next_node.visited:
                continue
            unvisited_queue.add(next_node)
            new_dist = current_node.distance + edges_to_search[next_node]
            if new_dist < next_node.distance:
                next_node.distance = new_dist
                next_node.previous = current_node

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
    dijkstra(g.get_nodes_by_name('S')[0])
    path = shortest(g.get_nodes_by_name('E')[0])
    return len(path) - 1


def part2():
    g = parse()
    dijkstra(g.get_nodes_by_name('E')[0], reverse=True)
    min_distance = None
    for target in g.get_nodes_by_name('a') + g.get_nodes_by_name('S'):
        distance = len(shortest(target)) - 1
        if distance > 0 and (min_distance is None or distance < min_distance):
            min_distance = distance
    return min_distance


if __name__ == '__main__':
    # g = parse()
    # start = list({v for v in g.vertices if 'S' in v.name})[0]
    # dijkstra2(g, start)
    print(part1())
    print(part2())
