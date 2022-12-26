from puzzles.Day24.grid import Grid
from util import *


def parse():
    return Grid(read_input_as_string_grid())


def part1():
    return parse().run()


def part2():
    return parse().run(0)


if __name__ == '__main__':
    print(part1())
    print(part2())
