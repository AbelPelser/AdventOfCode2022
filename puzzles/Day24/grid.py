from puzzles.Day24.storm import Storm
from util import enumerate_matrix, get_neighbour_coords


class Grid:
    def __init__(self, grid):
        self.height = len(grid)
        self.width = len(grid[0])
        self.walls = set()
        self.storms = []
        for (y, x), c in enumerate_matrix(grid):
            if c == '#':
                self.walls.add((x, y))
            elif y == self.height - 1:
                # No wall, still so low? target
                self.target = (x, y)
            elif y == 0:
                # No wall, still so high? start
                self.start = (x, y)
        for (y, x), c in enumerate_matrix(grid):
            if c in ('<', '>', 'v', '^'):
                self.storms.append(Storm.make(c, (x, y), self.width, self.height))
        self.walls.add((self.start[0], self.start[1] - 1))  # Block square above start
        self.walls.add((self.target[0], self.target[1] + 1))  # Block square under target

    def run(self, stage=-1):
        reachable_in_current_minute = {self.start}
        minute = 0
        while self.target not in reachable_in_current_minute:
            reachable_in_next_minute = set()
            blocked_by_storms = {s.move_to_next_position() for s in self.storms}
            for coord in reachable_in_current_minute:
                for neighbour in get_neighbour_coords(coord):
                    if neighbour in self.walls or neighbour in blocked_by_storms:
                        continue
                    reachable_in_next_minute.add(neighbour)
                if coord not in blocked_by_storms:
                    reachable_in_next_minute.add(coord)
            reachable_in_current_minute = reachable_in_next_minute
            minute += 1
        if stage in (-1, 2):
            return minute
        self.start, self.target = self.target, self.start
        return minute + self.run(stage + 1)
