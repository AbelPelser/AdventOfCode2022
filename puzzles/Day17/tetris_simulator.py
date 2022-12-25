from util import get_leftmost_point, get_rightmost_point, get_downmost_point, get_upmost_point

WIDTH = 7
ROCKS = [
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
    {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    {(0, 0), (0, 1), (0, 2), (0, 3)},
    {(0, 0), (1, 0), (0, 1), (1, 1)}
]
JET_DELTAS = {'>': (1, 0), '<': (-1, 0)}


def make_rock(rock, offset_y, offset_x=2):
    # offset_x always 2, only the height differs
    return move_rock(rock, offset_x, offset_y)


def move_rock(rock, delta_x, delta_y):
    return {(x + delta_x, y + delta_y) for (x, y) in rock}


class TetrisSimulator:
    def __init__(self, jets, goal=2022):
        self.jets = jets
        self.goal = goal
        self.jet_i = 0
        self.rock_i = 0
        self.coords_blocked = set()
        self.highest_y_blocked_relative = self.highest_y_blocked_absolute = -1
        self.situation_cache = {}
        self.rock = None
        self.i = 0

    def get_next_rock(self):
        self.rock = make_rock(ROCKS[self.rock_i], self.highest_y_blocked_relative + 4)
        self.rock_i = (self.rock_i + 1) % len(ROCKS)

    def get_next_jet_delta(self):
        jet_delta = JET_DELTAS[self.jets[self.jet_i]]
        self.jet_i = (self.jet_i + 1) % len(self.jets)
        return jet_delta

    def move_rock_if_possible(self, delta_x, delta_y):
        new_coords = move_rock(self.rock, delta_x, delta_y)
        can_move = get_leftmost_point(new_coords) >= 0 and \
                   get_rightmost_point(new_coords) < WIDTH and \
                   get_downmost_point(new_coords) >= 0 and \
                   not any(filter(lambda t: t in self.coords_blocked, new_coords))
        if can_move:
            self.rock = new_coords
        return can_move

    def run(self):
        while self.i < self.goal:
            self.get_next_rock()
            while True:
                jet_delta = self.get_next_jet_delta()
                self.move_rock_if_possible(*jet_delta)

                moved = self.move_rock_if_possible(0, -1)
                if not moved:
                    self.lay_rock_to_rest()
                    break
            self.i += 1
        return self.highest_y_blocked_absolute + 1

    def lay_rock_to_rest(self):
        self.coords_blocked = self.coords_blocked.union(self.rock)
        top = get_upmost_point(self.rock)
        if top > self.highest_y_blocked_relative:
            diff = top - self.highest_y_blocked_relative
            self.highest_y_blocked_relative += diff
            self.highest_y_blocked_absolute += diff
        if self.reduce_stored_surroundings():
            self.detect_repetition()

    def y_is_fully_blocked(self, y):
        # Return True if for all x, (x, y) or (x, y + 1) is blocked.
        # This means no rock can ever descend below this row, so we don't need to store anything below this row
        for x in range(WIDTH):
            if (x, y) not in self.coords_blocked and (x, y + 1) not in self.coords_blocked:
                return False
        return True

    def reduce_stored_surroundings(self):
        # Trim bottom rows from coords_blocked
        y_in_rock = {y for _, y in self.rock}
        lowest_y_to_store = 0
        for y in y_in_rock:
            if y <= lowest_y_to_store:
                continue
            if self.y_is_fully_blocked(y):
                lowest_y_to_store = y
        if lowest_y_to_store <= 0:
            # Nothing can be trimmed
            return False
        # Remove all coords that are below lowest_y_to_store, and normalize the rest
        self.coords_blocked = {(x, y - lowest_y_to_store) for (x, y) in self.coords_blocked if
                               y >= lowest_y_to_store}
        self.highest_y_blocked_relative -= lowest_y_to_store
        return True

    def get_current_situation(self):
        return frozenset(self.coords_blocked), self.jet_i, self.rock_i

    def detect_repetition(self):
        # If this situation has occurred before, use it to fast-forward the simulation
        situation = self.get_current_situation()
        current_score = self.highest_y_blocked_absolute + 1
        if situation in self.situation_cache.keys():
            prev_score, prev_i = self.situation_cache[situation]
            score_delta = current_score - prev_score
            i_delta = self.i - prev_i
            n_times = (self.goal - self.i) // i_delta
            self.i += n_times * i_delta
            new_score = current_score + (n_times * score_delta)
            self.highest_y_blocked_absolute = new_score - 1
        else:
            self.situation_cache[situation] = (current_score, self.i)
