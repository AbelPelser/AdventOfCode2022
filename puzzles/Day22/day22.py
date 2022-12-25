import re

from puzzles.Day22.cubemapping import *
from util import *

CUBE_MAPPING_RULES = [
    CubeMapping(facing=DOWN, source_range=[(100, 49), (149, 49)], target_range=[(99, 50), (99, 99)], turn_needed='R'),
    CubeMapping(facing=RIGHT, source_range=[(99, 50), (99, 99)], target_range=[(100, 49), (149, 49)], turn_needed='L'),

    CubeMapping(facing=LEFT, source_range=[(50, 50), (50, 99)], target_range=[(0, 100), (49, 100)], turn_needed='L'),
    CubeMapping(facing=UP, source_range=[(0, 100), (49, 100)], target_range=[(50, 50), (50, 99)], turn_needed='R'),

    CubeMapping(facing=RIGHT, source_range=[(149, 0), (149, 49)], target_range=[(99, 149), (99, 100)],
                turn_needed='RR'),
    CubeMapping(facing=RIGHT, source_range=[(99, 100), (99, 149)], target_range=[(149, 49), (149, 0)],
                turn_needed='RR'),

    CubeMapping(facing=DOWN, source_range=[(50, 149), (99, 149)], target_range=[(49, 150), (49, 199)], turn_needed='R'),
    CubeMapping(facing=RIGHT, source_range=[(49, 150), (49, 199)], target_range=[(50, 149), (99, 149)],
                turn_needed='L'),

    CubeMapping(facing=LEFT, source_range=[(50, 0), (50, 49)], target_range=[(0, 149), (0, 100)], turn_needed='RR'),
    CubeMapping(facing=LEFT, source_range=[(0, 100), (0, 149)], target_range=[(50, 49), (50, 0)], turn_needed='RR'),

    CubeMapping(facing=UP, source_range=[(100, 0), (149, 0)], target_range=[(0, 199), (49, 199)], turn_needed=''),
    CubeMapping(facing=DOWN, source_range=[(0, 199), (49, 199)], target_range=[(100, 0), (149, 0)], turn_needed=''),

    CubeMapping(facing=UP, source_range=[(50, 0), (99, 0)], target_range=[(0, 150), (0, 199)], turn_needed='R'),
    CubeMapping(facing=LEFT, source_range=[(0, 150), (0, 199)], target_range=[(50, 0), (99, 0)], turn_needed='L'),
]

CUBE_MAPPING_RULES2 = [
    CubeMapping(facing=LEFT, source_range=[(8, 0), (8, 3)], target_range=[(4, 4), (7, 4)], turn_needed='L'),
    CubeMapping(facing=UP, source_range=[(4, 4), (7, 4)], target_range=[(8, 0), (8, 3)], turn_needed='R'),

    CubeMapping(facing=RIGHT, source_range=[(11, 4), (11, 7)], target_range=[(15, 8), (12, 8)], turn_needed='R'),
    CubeMapping(facing=UP, source_range=[(12, 8), (15, 8)], target_range=[(11, 7), (11, 4)], turn_needed='L'),

    CubeMapping(facing=DOWN, source_range=[(4, 7), (7, 7)], target_range=[(8, 11), (8, 8)], turn_needed='L'),
    CubeMapping(facing=LEFT, source_range=[(8, 8), (8, 11)], target_range=[(7, 7), (4, 7)], turn_needed='R'),

    CubeMapping(facing=RIGHT, source_range=[(7, 0), (7, 3)], target_range=[(15, 11), (15, 8)], turn_needed='RR'),
    CubeMapping(facing=RIGHT, source_range=[(15, 8), (15, 11)], target_range=[(7, 3), (7, 0)], turn_needed='RR'),

    CubeMapping(facing=DOWN, source_range=[(0, 7), (3, 7)], target_range=[(11, 11), (8, 11)], turn_needed='RR'),
    CubeMapping(facing=DOWN, source_range=[(8, 11), (11, 11)], target_range=[(3, 7), (0, 7)], turn_needed='RR'),

    CubeMapping(facing=UP, source_range=[(8, 0), (11, 0)], target_range=[(3, 4), (0, 4)], turn_needed='RR'),
    CubeMapping(facing=UP, source_range=[(0, 4), (3, 4)], target_range=[(11, 0), (8, 0)], turn_needed='RR'),

    CubeMapping(facing=LEFT, source_range=[(0, 4), (0, 7)], target_range=[(15, 11), (12, 11)], turn_needed='R'),
    CubeMapping(facing=DOWN, source_range=[(12, 11), (15, 11)], target_range=[(0, 7), (0, 4)], turn_needed='L'),
]


class DoThing:
    def __init__(self, map_open, map_blocked, off_map):
        self.map_open = map_open
        self.map_blocked = map_blocked
        self.map = map_open.union(map_blocked)
        self.off_map = off_map
        top_y = get_downmost_point(self.map_open.union(self.map_blocked))
        top_left = min({(x, y) for (x, y) in self.map_open.union(self.map_blocked) if y == top_y}, key=lambda t: t[0])
        self.position = top_left
        self.facing = 0
        self.turn_map = {'L': self.turn_left, 'R': self.turn_right}

    def turn_right(self):
        self.facing = (self.facing + 1) % 4

    def turn_left(self):
        self.facing = (self.facing - 1) % 4

    def get_movement_delta(self):
        return {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}[self.facing]

    def get_movement_step(self, amount):
        dx, dy = self.get_movement_delta()
        return amount * dx, amount * dy

    def apply_cube_rules(self, x, y):
        applicable = [rule for rule in CUBE_MAPPING_RULES if rule.is_applicable((x, y), self.facing)]
        f = 6
        assert len(applicable) == 1, str(self.position)
        rule = applicable[0]
        new_coord, turn_needed = rule.apply((x, y), self.facing)
        for letter in list(turn_needed):
            self.turn_map[letter]()
        return new_coord

    def get_in_between_steps(self, amount, part2=False):
        x, y = self.position
        for _ in range(amount):
            prev_x, prev_y = x, y
            # dx, dy can change during apply_cube_rules
            dx, dy = self.get_movement_delta()
            x, y = x + dx, y + dy
            if (x, y) not in self.map:
                if part2:
                    x, y = self.apply_cube_rules(prev_x, prev_y)
                else:
                    x, y = self.get_opposite_point_on_map(x, y)
            yield x, y

    def get_opposite_point_on_map(self, current_x, current_y):
        current_col = {(x, y) for (x, y) in self.map if x == current_x}
        current_row = {(x, y) for (x, y) in self.map if y == current_y}
        if self.facing == 0:
            current_x = get_leftmost_point(current_row)
        elif self.facing == 1:
            current_y = get_downmost_point(current_col)
        elif self.facing == 2:
            current_x = get_rightmost_point(current_row)
        elif self.facing == 3:
            current_y = get_upmost_point(current_col)
        else:
            assert False
        return current_x, current_y

    def dump(self):
        all_points = self.map.union(self.off_map)
        max_x = get_rightmost_point(all_points)
        max_y = get_upmost_point(all_points)
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                coord = (x, y)
                if coord == self.position:
                    print('O', end='')
                elif coord in self.map_blocked:
                    print('#', end='')
                elif coord in self.map_open:
                    print('.', end='')
                elif coord in self.off_map:
                    print(' ', end='')
            print('')
        print('\n\n')

    def run(self, instructions, part2=False):
        self.dump()
        for inst in re.findall('(L|R|[0-9]+)', instructions):
            if inst in ('L', 'R'):
                self.turn_map[inst]()
            else:
                amount = int(inst)
                prev_facing = self.facing
                for step in self.get_in_between_steps(amount, part2=part2):
                    if step in self.map_blocked:
                        if prev_facing != self.facing:
                            # Since the previous step, our facing has changed (cube rules), but we're blocked so we never enter the new cube square
                            self.facing = prev_facing
                        break
                    prev_facing = self.facing
                    self.position = step
                    # self.dump()
        return 1000 * (self.position[1] + 1) + 4 * (self.position[0] + 1) + self.facing


def part1():
    blocks = read_input_as_blocks()
    assert len(blocks) == 2
    grid = blocks[0]
    instructions = blocks[1]
    map_blocked = set()
    map_open = set()
    off_map = set()
    for y, line in enumerate(safe_split(grid, '\n')):
        for x, thing in enumerate(list(line)):
            coord = (x, y)
            if thing == ' ':
                off_map.add(coord)
            elif thing == '#':
                map_blocked.add(coord)
            elif thing == '.':
                map_open.add(coord)
            else:
                assert False, thing
    map = DoThing(map_open, map_blocked, off_map)
    return map.run(instructions)


def part2():
    blocks = read_input_as_blocks()
    assert len(blocks) == 2
    grid = blocks[0]
    instructions = blocks[1]
    map_blocked = set()
    map_open = set()
    off_map = set()
    for y, line in enumerate(safe_split(grid, '\n')):
        for x, thing in enumerate(list(line)):
            coord = (x, y)
            if thing == ' ':
                off_map.add(coord)
            elif thing == '#':
                map_blocked.add(coord)
            elif thing == '.':
                map_open.add(coord)
            else:
                assert False, thing
    map = DoThing(map_open, map_blocked, off_map)
    return map.run(instructions, part2=True)


if __name__ == '__main__':
    # print(part1())
    print(part2())
