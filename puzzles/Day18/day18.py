from util import read_input_as_lines, get_neighbour_coords, get_extremes


class Point:
    def __init__(self, coords):
        self.coords = coords
        self.neighbours = {}

    def add_neighbour(self, neighbour: 'Point'):
        self.neighbours[neighbour.coords] = neighbour
        neighbour.neighbours[self.coords] = self


def parse():
    points = {}
    lines = read_input_as_lines()
    for line in lines:
        x, y, z = map(int, line.split(','))
        coord = (x, y, z)
        point = Point(coord)
        for neighbour_coord in get_neighbour_coords(coord):
            if neighbour_coord in points.keys():
                point.add_neighbour(points[neighbour_coord])
        points[coord] = point
    return points


def part1():
    points = parse()
    return sum(6 - len(point.neighbours) for point in points.values())


def fill_with_steam(start: tuple, point_coords, minimums: tuple, maximums: tuple):
    seen = set()
    to_visit = {start}
    filled_with_steam = set()
    while to_visit:
        to_visit_next = set()
        for coord in to_visit:
            seen.add(coord)
            for (xn, yn, zn) in get_neighbour_coords(coord):
                if not (minimums[0] <= xn <= maximums[0] and
                        minimums[1] <= yn <= maximums[1] and
                        minimums[2] <= zn <= maximums[2]):
                    continue
                neighbour_coord = (xn, yn, zn)
                if neighbour_coord in point_coords:
                    continue
                filled_with_steam.add(neighbour_coord)
                if neighbour_coord not in seen:
                    to_visit_next.add(neighbour_coord)
        to_visit = to_visit_next
    return filled_with_steam


def part2():
    points = parse()
    missing_neighbour_coords = set()
    for point in points.values():
        for neighbour_coord in get_neighbour_coords(point.coords):
            if neighbour_coord not in point.neighbours.keys():
                missing_neighbour_coords.add(neighbour_coord)
    minimums, maximums = get_extremes(missing_neighbour_coords)
    filled_with_steam = fill_with_steam(minimums, points.keys(), minimums, maximums)
    return len([neighbour
                for point_coords in points.keys()
                for neighbour in get_neighbour_coords(point_coords)
                if neighbour in filled_with_steam])


if __name__ == '__main__':
    print(part1())
    print(part2())
