# from puzzles.Day19.blueprint3 import BlueprintNew
# from puzzles.Day19.blueprint2 import Blueprint
from puzzles.Day19.blueprint4 import BlueprintBruteForceNew
from util import read_input_as_lines, mult


def part1():
    lines = read_input_as_lines()
    result = 0
    for i, line in enumerate(lines):
        blueprint = BlueprintBruteForceNew.parse(line)
        n_geodes, path = blueprint.run()
        quality = n_geodes * blueprint.blueprint_nr
        result += quality
        print(f'Blueprint {blueprint.blueprint_nr} can open {n_geodes} geodes and has quality {quality} via {path}')
    return result


def part2():
    lines = read_input_as_lines()
    results = []
    for line in lines[:3]:
        # This works for my input but not for test data
        blueprint = BlueprintBruteForceNew.parse(line, max_n_minutes=32)
        n_geodes, path = blueprint.run()
        print(f'Blueprint {blueprint.blueprint_nr} can open {n_geodes} geodes via {path}')
        results.append(n_geodes)
    return mult(results)


if __name__ == '__main__':
    print(part1())
    print(part2())
