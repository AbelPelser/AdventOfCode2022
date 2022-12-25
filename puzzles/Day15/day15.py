from typing import Tuple, List

from util import read_input_as_lines


def parse():
    beacons = set()
    sensors = {}
    for line in read_input_as_lines():
        sensor_x = int(line.split('Sensor at x=')[-1].split(', ')[0])
        sensor_y = int(line.split('y=')[1].split(': closest')[0])
        beacon_x = int(line.split('beacon is at x=')[-1].split(', ')[0])
        beacon_y = int(line.split('y=')[-1])
        beacons.add((beacon_x, beacon_y))
        sensors[(sensor_x, sensor_y)] = (beacon_x, beacon_y)
    return beacons, sensors


def part1():
    beacons, sensors = parse()
    goal_y = 2000_000
    res = 0
    sensors_on_goal = {(sx, sy) for sx, sy in sensors.keys() if sy == goal_y}
    beacons_on_goal = {(bx, by) for bx, by in beacons if by == goal_y}
    objects_on_goal = sensors_on_goal.union(beacons_on_goal)
    for f, t in filter(None, get_range_for_y_col(goal_y, sensors)):
        res += t - f
        res -= len([_ for sx, _ in objects_on_goal if f <= sx < t])
    return res


def get_range_for_y_col(goal_y, sensors):
    ranges: List[Tuple[int, int]] = []
    for (sx, sy), (bx, by) in sensors.items():
        manhattan = abs(sx - bx) + abs(sy - by)
        distance_y = abs(sy - goal_y)
        if distance_y > manhattan:
            continue
        max_distance_x_at_col = manhattan - distance_y
        ranges.append((sx - max_distance_x_at_col, sx + max_distance_x_at_col + 1))
    return merge_ranges(ranges)


def merge_ranges(ranges):
    ranges = sorted(ranges, key=lambda t: t[0])
    for i in range(1, len(ranges)):
        prev_i = i - 1
        while prev_i >= 0 and ranges[prev_i] is None:
            prev_i -= 1
        prev_range = ranges[prev_i]
        if prev_range is None:
            continue
        prev_f, prev_t = prev_range
        current_f, current_t = ranges[i]
        if current_f > prev_t:
            continue
        ranges[i] = None
        ranges[prev_i] = prev_f, max(current_t, prev_t)
    return ranges


def part2():
    beacons, sensors = parse()
    for y in range(4000_001):
        ranges = list(filter(None, get_range_for_y_col(y, sensors)))
        if len(ranges) > 1:
            x = ranges[0][1]
            return x * 4_000_000 + y


if __name__ == '__main__':
    print(part1())
    print(part2())
