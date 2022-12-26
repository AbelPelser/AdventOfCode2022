class Storm:
    def __init__(self, start_position, position, movement_delta, max_position_exclusive, c):
        self.start_position = start_position
        self.position = position
        self.movement_delta = movement_delta
        self.max_position_exclusive = max_position_exclusive
        self.c = c

    def move_to_next_position(self, minutes=1):
        x, y = self.position
        dx, dy = self.movement_delta
        for _ in range(minutes):
            x += dx
            y += dy
            if (x, y) == self.max_position_exclusive:
                x, y = self.start_position
        self.position = x, y
        return x, y

    def __copy__(self):
        return Storm(self.start_position, self.position, self.movement_delta, self.max_position_exclusive, self.c)
