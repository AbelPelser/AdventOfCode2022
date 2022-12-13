from util import read_input_as_string_grid, enumerate_matrix, get_neighbour_coords_in_matrix


class Vertex:
    def __init__(self, node):
        self.id = node
        self.outgoing_edges = {}
        self.incoming_edges = {}
        self.distance = 1_000_000
        self.visited = False
        self.previous = None

    def reset(self):
        self.distance = 1_000_000
        self.visited = False
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.outgoing_edges[neighbor] = weight
        neighbor.incoming_edges[self] = weight

    def __str__(self):
        return f'{self.id} outgoing edges: {[x.id for x in self.outgoing_edges]}'


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def reset(self):
        for v in self.vert_dict.values():
            v.reset()

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices += 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)
        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)


def shortest(vertex):
    current = vertex
    path = [vertex.id]
    while current.previous:
        current = current.previous
        path.append(current.id)
    return path


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
    node_map = {}
    for (y, x), node in enumerate_matrix(grid):
        node_str = f'{node}({x},{y})'
        g.add_vertex(node_str)
        node_map[(y, x)] = node_str
    for (y, x), node in enumerate_matrix(grid):
        node_str = node_map[(y, x)]
        for (y_n, x_n) in get_neighbour_coords_in_matrix(grid, (y, x)):
            neighbour_str = node_map[(y_n, x_n)]
            if can_go_from_node_to_node(node_str, neighbour_str):
                g.add_edge(node_str, neighbour_str, 1)
            if can_go_from_node_to_node(neighbour_str, node_str):
                g.add_edge(neighbour_str, node_str, 1)
    return g


def part1():
    g = parse()
    start = list({k: v for k, v in g.vert_dict.items() if 'S' in k}.values())[0]
    dijkstra(g, start)
    target = list({k: v for k, v in g.vert_dict.items() if 'E' in k}.values())[0]
    path = shortest(target)
    return len(path) - 1


def part2():
    g = parse()
    start = list({k: v for k, v in g.vert_dict.items() if 'E' in k}.values())[0]
    dijkstra(g, start, reverse=True)
    targets = list({k: v for k, v in g.vert_dict.items() if 'a' in k or 'S' in k}.values())
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
    print(part1())
    print(part2())
