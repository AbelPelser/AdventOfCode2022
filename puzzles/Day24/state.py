from copy import *

from puzzles.Day24.storm import Storm


class State:
    def __init__(self, minute, storms):
        self.minute: int = minute
        self.storms: list['Storm'] = storms
        self.blocked_by_storms: set[tuple] = {s.position for s in storms}

    def round(self):
        self.minute += 1
        new_blocked_by_storms = set()
        for storm in self.storms:
            x, y = storm.move_to_next_position()
            new_blocked_by_storms.add((x, y))
        self.blocked_by_storms = new_blocked_by_storms

    def __copy__(self):
        return State(self.minute, deepcopy(self.storms))
