from util import read_input_as_lines


def part1():
    count = 0
    for line in read_input_as_lines():
        first, second = line.split(',')
        f1, t1 = map(int, first.split('-'))
        f2, t2 = map(int, second.split('-'))
        if (f2 >= f1 and t2 <= t1) or (f1 >= f2 and t1 <= t2):
            count += 1
    return count


def part2():
    count = 0
    for line in read_input_as_lines():
        first, second = line.split(',')
        f1, t1 = map(int, first.split('-'))
        f2, t2 = map(int, second.split('-'))
        if t1 >= f2 and t2 >= f1:
            count += 1
    return count


if __name__ == '__main__':
    print(part1())
    print(part2())
