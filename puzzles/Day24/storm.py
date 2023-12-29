MOVEMENT_DELTAS = {
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1),
    '^': (0, -1)
}


class Storm:
    def __init__(self, start_position, position, movement_delta, max_position_exclusive):
        self.start_position = start_position
        self.position = position
        self.movement_delta = movement_delta
        self.max_position_exclusive = max_position_exclusive

    def move_to_next_position(self):
        x, y = self.position
        dx, dy = self.movement_delta
        x += dx
        y += dy
        if (x, y) == self.max_position_exclusive:
            x, y = self.start_position
        self.position = x, y
        return x, y

    @staticmethod
    def make(storm_type, position, grid_width, grid_height):
        x, y = position
        assert storm_type in ('<', '>', 'v', '^')
        movement_delta = MOVEMENT_DELTAS[storm_type]
        if storm_type == '<':
            start_x = grid_width - 2
            return Storm((start_x, y), (x, y), movement_delta, (0, y))
        elif storm_type == '>':
            end_x_excl = grid_width - 1  # walls
            return Storm((1, y), (x, y), movement_delta, (end_x_excl, y))
        elif storm_type == '^':
            start_y = grid_height - 2
            return Storm((x, start_y), (x, y), movement_delta, (x, 0))
        elif storm_type == 'v':
            end_y_excl = grid_height - 1  # wall
            return Storm((x, 1), (x, y), movement_delta, (x, end_y_excl))

    def __copy__(self):
        return Storm(self.start_position, self.position, self.movement_delta, self.max_position_exclusive)
