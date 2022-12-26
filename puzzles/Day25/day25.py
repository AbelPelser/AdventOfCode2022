from gmpy2 import digits

from util import read_input_as_lines


def to_snafu_replace(base5):
    return base5.replace('0', '=').replace('1', '-').replace('2', '0').replace('3', '1').replace('4', '2')


def from_snafu_replace(line):
    return line.replace('2', '4').replace('1', '3').replace('0', '2').replace('-', '1').replace('=', '0')


def snafu_to_normal(line):
    return int(from_snafu_replace(line), 5) - int('2' * len(line), 5)


def normal_to_snafu(number):
    base5 = digits(number, 5)
    n_digits_to_add = 0
    while len(base5) != n_digits_to_add:
        n_digits_to_add += 1
        base5 = digits(number + int('2' * n_digits_to_add, 5), 5)
    return to_snafu_replace(base5)


def part1():
    return normal_to_snafu(sum(snafu_to_normal(line) for line in read_input_as_lines()))


def part2():
    pass


if __name__ == '__main__':
    print(part1())
    print(part2())
