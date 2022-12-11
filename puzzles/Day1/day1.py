from util import read_input_as_blocks, safe_split


def part1():
    return max(calculate_calory_sum_per_elf())


def part2():
    return sum(sorted(calculate_calory_sum_per_elf())[-3:])


def calculate_calory_sum_per_elf():
    return [sum(map(int, safe_split(l))) for l in read_input_as_blocks()]


if __name__ == '__main__':
    print(part1())
    print(part2())
