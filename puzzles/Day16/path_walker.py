from functools import cache

import networkx as nx

from puzzles.Day16.valve import Valve


class PathWalker:
    def __init__(self, tunnel_graph, max_time=26):
        self.tunnel_graph = tunnel_graph
        self.max_time = max_time
        self.shortest_paths = {}

    # @cache
    def get_shortest_path(self, f, t):
        if (f, t) in self.shortest_paths.keys():
            return self.shortest_paths[(f, t)]
        result = len(nx.shortest_path(self.tunnel_graph, f, t)) - 1
        self.shortest_paths[(f, t)] = result
        return result

    def make_paths(self, current_path, current_valve, time_spent, valves_to_open, current_flow_rate=0,
                   pressure_released=0):
        yield current_path, pressure_released + (self.max_time - time_spent) * current_flow_rate

        for next_valve in valves_to_open:
            travel_cost_in_minutes = self.get_shortest_path(current_valve.name, next_valve.name)
            minutes_needed = travel_cost_in_minutes + 1
            if minutes_needed > (self.max_time - time_spent):
                continue

            yield from self.make_paths(
                current_path + [next_valve],
                next_valve,
                time_spent + minutes_needed,
                {v for v in valves_to_open if v != next_valve},
                current_flow_rate=current_flow_rate + next_valve.flow_rate,
                pressure_released=pressure_released + minutes_needed * current_flow_rate
            )

    def calculate_best_gain_per_set_of_nodes(self, start, valves_to_open: set['Valve']):
        result = {}
        for path, gain in self.make_paths([], start, 0, valves_to_open):
            valve_set = frozenset(path)
            if valve_set not in result or result[valve_set] < gain:
                result[valve_set] = gain
        return result
