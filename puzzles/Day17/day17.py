from puzzles.Day17.tetris_simulator import TetrisSimulator
from util import read_input


def part1():
    return TetrisSimulator(read_input(), goal=2022).run()


def part2():
    return TetrisSimulator(read_input(), goal=1_000_000_000_000).run()


if __name__ == '__main__':
    print(part1())
    print(part2())
