from copy import copy

from util import *


MOVEMENT_DELTAS = {
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1),
    '^': (0, -1)
}

class Storm:
    def __init__(self, location, start_position, position, movement_delta, max_position_exclusive):
        self.location = location
        self.start_position = start_position
        self.position = position
        self.movement_delta = movement_delta
        self.max_position_exclusive = max_position_exclusive

    def move_to_next_position(self, minutes=1):
        x, y = self.position
        dx, dy = self.movement_delta
        for _ in range(minutes):
            x += dx
            y += dy
            if (x, y) == self.max_position_exclusive:
                x, y = self.start_position
        self.position = x, y
        return x, y

    def __copy__(self):
        return Storm(self.location, self.start_position, self.position, self.movement_delta, self.max_position_exclusive)


class State:
    def __init__(self, minute, storms):
        self.minute: int = minute
        self.storms: list['Storm'] = storms
        self.blocked_by_storms: set[tuple] = {s.position for s in storms}

    def round(self):
        self.minute += 1
        new_blocked_by_storms = set()
        for storm in self.storms:
            x, y = storm.move_to_next_position()
            new_blocked_by_storms.add((x, y))
        self.blocked_by_storms = new_blocked_by_storms

    def __copy__(self):
        return State(self.minute, copy(self.storms))


class DoThinger:
    def __init__(self, grid, target, initial_state):
        self.grid = grid
        self.target = target
        self.states = [initial_state]

    def get_state(self, minute):
        n_known_states = len(self.states)
        if n_known_states > minute:
            return self.states[minute]
        latest_state = self.states[-1]
        for _ in range(n_known_states, minute + 1):
            new_state = copy(latest_state)
            new_state.round()
            self.states.append(new_state)
            latest_state = new_state
        return self.states[minute]

    def do(self, start: tuple[int, int]):
        to_visit = [(start, 0)]  # (coord, minute
        while True:
            ((current_x, current_y), minute), *to_visit = to_visit
            to_visit.append(())


def part1():
    grid = read_input_as_string_grid()
    wall = set()
    start = None
    target = None
    storms = []  #
    height = len(grid)
    width = len(grid[0])
    for (y, x), c in enumerate_matrix(grid):
        if c == 'E':
            start = (x, y)
        elif c == '#':
            wall.add((x, y))
        elif y == height - 1:
            target = (x, y)




def part2():
    pass


if __name__ == '__main__':
    print(part1())
    print(part2())
