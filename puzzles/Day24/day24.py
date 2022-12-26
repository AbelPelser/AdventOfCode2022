from puzzles.Day24.dothinger import DoThinger
from puzzles.Day24.state import State
from puzzles.Day24.storm import Storm
from util import *

MOVEMENT_DELTAS = {
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1),
    '^': (0, -1)
}


def part1():
    grid = read_input_as_string_grid()
    wall = set()
    start = None
    target = None
    storms = []  #
    height = len(grid)
    width = len(grid[0])
    for (y, x), c in enumerate_matrix(grid):
        if c == '#':
            wall.add((x, y))
        elif y == height - 1:
            # No wall, still so low? target
            target = (x, y)
        elif y == 0:
            start = (x, y)
    for (y, x), c in enumerate_matrix(grid):
        if c == '<':
            start_x = len(grid[y]) - 2
            storms.append(Storm((start_x, y), (x, y), (-1, 0), (0, y), c))
        elif c == '>':
            end_x_excl = width - 1  # wall
            storms.append(Storm((1, y), (x, y), (1, 0), (end_x_excl, y), c))
        elif c == '^':
            start_y = height - 2
            storms.append(Storm((x, start_y), (x, y), (0, -1), (x, 0), c))
        elif c == 'v':
            end_y_excl = height - 1  # wall
            storms.append(Storm((x, 1), (x, y), (0, 1), (x, end_y_excl), c))
    wall.add((start[0], start[1] - 1))  # Block square above start

    initial_state = State(0, storms)

    # t = DoThinger(initial_state, wall, width, height)
    # res = t.do(start, target)
    # print(res)

    t2 = DoThinger(None, wall, width, height)
    return t2.do2(start, target, storms)


def part2():
    grid = read_input_as_string_grid()
    wall = set()
    start = None
    target = None
    storms = []  #
    height = len(grid)
    width = len(grid[0])
    for (y, x), c in enumerate_matrix(grid):
        if c == '#':
            wall.add((x, y))
        elif y == height - 1:
            # No wall, still so low? target
            target = (x, y)
        elif y == 0:
            start = (x, y)
    for (y, x), c in enumerate_matrix(grid):
        if c == '<':
            start_x = len(grid[y]) - 2
            storms.append(Storm((start_x, y), (x, y), (-1, 0), (0, y), c))
        elif c == '>':
            end_x_excl = width - 1  # wall
            storms.append(Storm((1, y), (x, y), (1, 0), (end_x_excl, y), c))
        elif c == '^':
            start_y = height - 2
            storms.append(Storm((x, start_y), (x, y), (0, -1), (x, 0), c))
        elif c == 'v':
            end_y_excl = height - 1  # wall
            storms.append(Storm((x, 1), (x, y), (0, 1), (x, end_y_excl), c))
    wall.add((start[0], start[1] - 1))  # Block square above start
    wall.add((target[0], target[1] + 1))  # Block square under target

    t2 = DoThinger(None, wall, width, height)
    return t2.do2(start, target, storms, stage=0)


if __name__ == '__main__':
    print(part1())
    print(part2())
