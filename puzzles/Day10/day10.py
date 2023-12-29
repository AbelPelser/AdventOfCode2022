from util import read_input_as_lines


def part1():
    cycles = 0
    x = 1
    sum_part1 = 0
    for line in read_input_as_lines():
        delta_x = 0
        if line == 'noop':
            delta_cycles = 1
        else:
            delta_cycles = 2
            delta_x = int(line.split('addx ')[-1])
        cycles += delta_cycles
        for cycle_of_interest in (20, 60, 100, 140, 180, 220):
            if cycles == cycle_of_interest or \
                    (delta_cycles == 2 and cycles - 1 == cycle_of_interest):
                sum_part1 += cycle_of_interest * x
        x += delta_x
    return sum_part1


def dump(pixels):
    for j in range(6):
        for i in range(j * 40, (j + 1) * 40):
            print(pixels[i], end='')
        print('')


def part2():
    cycles = 0
    x = 1
    pixels = ['.'] * 240
    for line in read_input_as_lines():
        delta_x = 0
        if line == 'noop':
            delta_cycles = 1
        else:
            delta_cycles = 2
            delta_x = int(line.split('addx ')[-1])
        for cycle_to_draw in range(cycles, cycles + delta_cycles):
            if cycle_to_draw % 40 in (x - 1, x, x + 1):
                pixels[cycle_to_draw] = '#'
        cycles += delta_cycles
        x += delta_x
    dump(pixels)


if __name__ == '__main__':
    print(part1())
    print(part2())
