from collections import defaultdict
from copy import copy

from puzzles.Day24.state import State
from puzzles.Day24.storm import Storm
from util import get_neighbour_coords

MAX_VOLUNTARY_WAIT = 2


class DoThinger:
    def __init__(self, initial_state: 'State', walls: set[tuple[int, int]], width, height):
        self.states: list['State'] = [initial_state]
        self.walls = walls
        self.height = height
        self.width = width
        self.modulo = (width - 2) * (height - 2)

    def get_state(self, minute):
        n_known_states = len(self.states)
        if n_known_states > minute:
            return self.states[minute]
        latest_state = self.states[-1]
        for i in range(n_known_states, minute + 1):
            new_state = copy(latest_state)
            new_state.round()
            self.states.append(new_state)
            latest_state = new_state
            print(f'Made state {i}')
            # self.dump(new_state)
        return self.states[minute]

    def dump(self, state):
        for y in range(self.height + 1):
            for x in range(self.width + 1):
                coord = (x, y)
                if coord in self.walls:
                    print('#', end='')
                elif coord not in state.blocked_by_storms:
                    print('.', end='')
                else:
                    matching = [s for s in state.storms if s.position == coord]
                    assert len(matching) > 0
                    if len(matching) > 1:
                        print(len(matching), end='')
                    else:
                        print(matching[0].c, end='')
            print('')
        print('\n')

    def do2(self, start: tuple[int, int], target: tuple[int, int], storms: list['Storm'], stage=-1):
        reachable_in_current_minute = {start}
        result_minute = 0
        while target not in reachable_in_current_minute:
            reachable_in_next_minute = set()
            blocked_by_storms = {s.move_to_next_position() for s in storms}
            for coord in reachable_in_current_minute:
                for neighbour in get_neighbour_coords(coord):
                    if neighbour in self.walls or neighbour in blocked_by_storms:
                        continue
                    reachable_in_next_minute.add(neighbour)
                if coord not in blocked_by_storms:
                    reachable_in_next_minute.add(coord)
            reachable_in_current_minute = reachable_in_next_minute
            result_minute += 1
        print(f'Finished stage {stage}: {result_minute}')
        if stage in (-1, 2):
            return result_minute
        next_doer = DoThinger(None, self.walls, self.width, self.height)
        return result_minute + next_doer.do2(target, start, storms, stage + 1)


    def do(self, start: tuple[int, int], target: tuple[int, int], stage=-1):
        to_visit = [(start, 0, [(start, 0)])]  # (coord, minute, path)
        distances = {}  # coord: (minute, path)
        visited = set()

        waited = defaultdict(int)
        while len(to_visit) > 0:
            (current_coord, minute, path), *to_visit = to_visit
            if (current_coord, minute % self.modulo) in visited:
                continue
            visited.add((current_coord, minute % self.modulo))
            if current_coord not in distances.keys():
                distances[current_coord] = (minute, path)
            else:
                known_minute, known_path = distances[current_coord]
                if minute < known_minute:
                    distances[current_coord] = (minute, path[:])
            if current_coord == target:
                continue

            next_minute = minute + 1
            next_state: State = self.get_state(next_minute % self.modulo)
            new_to_visit = []
            for neighbour_coord in get_neighbour_coords(current_coord):
                if neighbour_coord in self.walls or \
                        neighbour_coord in next_state.blocked_by_storms or \
                        (neighbour_coord, next_minute) in visited:
                    continue
                new_to_visit.append((neighbour_coord, next_minute, path + [(neighbour_coord, next_minute)]))
            # Waiting option
            if current_coord not in next_state.blocked_by_storms:
                if len(new_to_visit) == 0 or waited[current_coord] < MAX_VOLUNTARY_WAIT:
                    waited[current_coord] += 1
                    new_to_visit.append((current_coord, next_minute, path))
            to_visit += new_to_visit
            to_visit = [(current_coord, minute, path)
                        for (current_coord, minute, path) in sorted(to_visit, key=lambda t: t[1])
                        if (current_coord, minute) not in visited]

        result_minute, result_path = distances[target]
        print(f'Finished stage {stage}: {result_minute} ({result_path})')
        if stage == -1:
            return result_minute
        if stage == 2:
            return result_minute
        next_doer = DoThinger(copy(self.states[result_minute]), self.walls, self.width, self.height)
        next_doer.states = self.states[result_minute:]
        # 221, 258, 260
        return result_minute + next_doer.do(target, start, stage + 1)
