from util import read_input_as_lines


lines = read_input_as_lines()


def part1():
    count = 0
    for line in lines:
        first, second = line.split(',')
        f1, t1 = first.split('-')
        f1, t1 = int(f1), int(t1)
        f2, t2 = second.split('-')
        f2, t2 = int(f2), int(t2)
        if (f2 >= f1 and t2 <= t1) or (f1 >= f2 and t1 <= t2):
            count += 1
    return count


def part2():
    count = 0
    for line in lines:
        first, second = line.split(',')
        f1, t1 = first.split('-')
        f1, t1 = int(f1), int(t1)
        f2, t2 = second.split('-')
        f2, t2 = int(f2), int(t2)
        if len(set(range(f1, t1 + 1)).intersection(set(range(f2, t2 + 1)))) > 0:
            count += 1
    return count


if __name__ == '__main__':
    print(part1())
    print(part2())
