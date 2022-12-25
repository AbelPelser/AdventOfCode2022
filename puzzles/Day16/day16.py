import networkx as nx

from puzzles.Day16.path_walker import PathWalker
from puzzles.Day16.valve import Valve
from util import read_input_as_lines, get_2_subsets_without_overlap


def parse():
    # lines = read_input_as_lines(filename='testInput')
    valves = {}
    lines = read_input_as_lines()
    for line in lines:
        name = line.split('Valve ')[1].split(' has ')[0]
        flow_rate = int(line.split('flow rate=')[-1].split(';')[0])
        valve_noun = 'valves' if 'valves' in line else 'valve'
        target_valve_names = line.split(valve_noun + ' ')[-1].split(', ')
        valves[name] = Valve(name, flow_rate, target_valve_names)
    tunnel_graph = nx.Graph()
    for valve in valves.values():
        for target in valve.target_valve_names:
            tunnel_graph.add_edge(valve.name, target)
    return valves, tunnel_graph


def part1():
    valves, tunnel_graph = parse()
    path_walker = PathWalker(tunnel_graph, max_time=30)
    valves_to_open = {v for v in valves.values() if v.flow_rate > 0}
    gains_per_set_of_nodes = path_walker.calculate_best_gain_per_set_of_nodes(valves['AA'], valves_to_open)
    return max(gains_per_set_of_nodes.values())


def part2():
    valves, tunnel_graph = parse()
    path_walker = PathWalker(tunnel_graph)
    valves_to_open = {v for v in valves.values() if v.flow_rate > 0}
    gains_per_set_of_nodes = path_walker.calculate_best_gain_per_set_of_nodes(valves['AA'], valves_to_open)
    best_res = 0
    for set_you, set_elephant in get_2_subsets_without_overlap(valves_to_open):
        set_you, set_elephant = frozenset(set_you), frozenset(set_elephant)
        if set_you not in gains_per_set_of_nodes.keys() or set_elephant not in gains_per_set_of_nodes.keys():
            continue
        best_res = max(best_res, gains_per_set_of_nodes[set_you] + gains_per_set_of_nodes[set_elephant])
    return best_res


if __name__ == '__main__':
    print(part1())
    print(part2())
