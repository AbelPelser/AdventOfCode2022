from util import read_input_as_lines, get_extremes

SOURCE = 500, 0


def add_points(blocked_points, x1, y1, x2, y2):
    d_x = -1 if x2 < x1 else 1 if x2 > x1 else 0
    d_y = -1 if y2 < y1 else 1 if y2 > y1 else 0
    while not (x1 == x2 and y1 == y2):
        blocked_points.add((x1, y1))
        x1 += d_x
        y1 += d_y
    blocked_points.add((x1, y1))
    return blocked_points


def dump(blocked_points, sand):
    [min_x, min_y], [max_x, max_y] = get_extremes(blocked_points.intersection(sand))
    for y in range(min_y - 5, max_y + 6):
        for x in range(min_x - 5, max_x + 6):
            if (x, y) in sand:
                print('o', end='')
            elif (x, y) in blocked_points:
                print('#', end='')
            else:
                print('.', end='')
        print('')
    print('')


def move_sand_if_possible(blocked_points, sand_x, sand_y, bottom=None):
    if bottom is not None and sand_y + 1 == bottom:
        return sand_x, sand_y
    if (sand_x, sand_y + 1) not in blocked_points:
        return sand_x, sand_y + 1
    if (sand_x - 1, sand_y + 1) not in blocked_points:
        return sand_x - 1, sand_y + 1
    if (sand_x + 1, sand_y + 1) not in blocked_points:
        return sand_x + 1, sand_y + 1
    return sand_x, sand_y


def parse():
    lines = read_input_as_lines()
    blocked_points = set()
    for line in lines:
        point_strings = line.split(' -> ')
        prev_x = prev_y = None
        for point_string in point_strings:
            x, y = map(int, point_string.split(','))
            if prev_x is not None:
                add_points(blocked_points, prev_x, prev_y, x, y)
            prev_x, prev_y = x, y
    return blocked_points


def part1():
    blocked_points = parse()
    lowest_y = max(blocked_points, key=lambda t: t[1])[1]
    sand = set()
    while True:
        sand_coord = SOURCE
        while True:
            if sand_coord[1] >= lowest_y:
                return len(sand)
            sand_coord_after_move = move_sand_if_possible(blocked_points, *sand_coord)
            if sand_coord == sand_coord_after_move:
                blocked_points.add(sand_coord)
                sand.add(sand_coord)
                break
            sand_coord = sand_coord_after_move


def part2():
    blocked_points = parse()
    lowest_y = max(blocked_points, key=lambda t: t[1])[1]
    sand = set()
    while True:
        sand_coord = SOURCE
        while True:
            sand_coord_after_move = move_sand_if_possible(blocked_points, *sand_coord, bottom=lowest_y + 2)
            if sand_coord == sand_coord_after_move:
                blocked_points.add(sand_coord)
                sand.add(sand_coord)
                if sand_coord == SOURCE:
                    return len(sand)
                break
            sand_coord = sand_coord_after_move


if __name__ == '__main__':
    print(part1())
    print(part2())
