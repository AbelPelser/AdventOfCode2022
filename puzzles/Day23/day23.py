from util import *

NORTH, SOUTH, WEST, EAST = 0, 1, 2, 3

DIRECTIONS = [NORTH, SOUTH, WEST, EAST]


class Elf:
    def __init__(self, position):
        self.position = position
        # self.direction = 3


class Map:
    def __init__(self):
        self.elves = {}  # coord -> Elf
        self.direction_start_i = 0
        self.direction_check_map = {
            NORTH: self.elf_can_move_north,
            WEST: self.elf_can_move_west,
            SOUTH: self.elf_can_move_south,
            EAST: self.elf_can_move_east
        }
        self.direction_deltas = {
            EAST: (1, 0), SOUTH: (0, 1), WEST: (-1, 0), NORTH: (0, -1)
        }
        self.n_directions = len(self.direction_deltas)

    def add_elf(self, position):
        self.elves[position] = Elf(position)

    def elf_can_move_north(self, elf):
        x, y = elf.position
        return not ((x - 1, y - 1) in self.elves or (x, y - 1) in self.elves or (x + 1, y - 1) in self.elves)

    def elf_can_move_east(self, elf):
        x, y = elf.position
        return not ((x + 1, y - 1) in self.elves or (x + 1, y) in self.elves or (x + 1, y + 1) in self.elves)

    def elf_can_move_south(self, elf):
        x, y = elf.position
        return not ((x - 1, y + 1) in self.elves or (x, y + 1) in self.elves or (x + 1, y + 1) in self.elves)

    def elf_can_move_west(self, elf):
        x, y = elf.position
        return not ((x - 1, y - 1) in self.elves or (x - 1, y) in self.elves or (x - 1, y + 1) in self.elves)

    def elf_can_stay_in_place(self, elf):
        x, y = elf.position
        surroundings = {
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y), (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
        }
        return len(surroundings.intersection(self.elves.keys())) == 0

    def move(self):
        conflicting_moves = set()
        proposed_moves = {}  # coord -> elf
        for elf in self.elves.values():
            if self.elf_can_stay_in_place(elf):
                continue
            proposed_move = self.get_first_valid_move_for_elf(elf)
            if proposed_move is None or proposed_move in conflicting_moves:
                continue
            if proposed_move in proposed_moves.keys():
                del proposed_moves[proposed_move]
                conflicting_moves.add(proposed_move)
                continue
            proposed_moves[proposed_move] = elf
        self.direction_start_i = (self.direction_start_i + 1) % self.n_directions
        if len(proposed_moves) == 0:
            # self.dump()
            return False
        for new_coords, elf in proposed_moves.items():
            del self.elves[elf.position]
            self.elves[new_coords] = elf
            elf.position = new_coords
        # self.dump()
        return True

    def get_first_valid_move_for_elf(self, elf):
        for i in range(len(DIRECTIONS)):
            direction_i = (self.direction_start_i + i) % self.n_directions
            if self.direction_check_map[direction_i](elf):
                dx, dy = self.direction_deltas[direction_i]
                return elf.position[0] + dx, elf.position[1] + dy

    def dump(self):
        max_x = get_rightmost_point(self.elves.keys())
        max_y = get_upmost_point(self.elves.keys())
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                coord = (x, y)
                if coord in self.elves:
                    print('#', end='')
                else:
                    print('.', end='')
            print('')
        print('\n')


def part1():
    grid = read_input_as_string_grid()
    map = Map()
    for y in range(len(grid)):
        for x, c in enumerate(grid[y]):
            if c == '#':
                map.add_elf((x, y))
    for _ in range(10):
        map.move()
    positions = map.elves.keys()
    min_x = get_leftmost_point(positions)
    max_x = get_rightmost_point(positions)
    min_y = get_downmost_point(positions)
    max_y = get_upmost_point(positions)
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(map.elves)

def part2():
    grid = read_input_as_string_grid()
    map = Map()
    for y in range(len(grid)):
        for x, c in enumerate(grid[y]):
            if c == '#':
                map.add_elf((x, y))
    i = 1
    while map.move():
        i += 1
    return i


if __name__ == '__main__':
    print(part1())
    print(part2())
