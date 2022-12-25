RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3

class CubeMapping:
    def __init__(self, facing: int, source_range, target_range, turn_needed=''):
        self.facing = facing
        self.source_range = source_range
        self.target_range = target_range
        self.turn_needed = turn_needed
        self.validate()

    def validate(self):
        [(source_from_x, source_from_y), (source_to_x, source_to_y)] = self.source_range
        [(target_from_x, target_from_y), (target_to_x, target_to_y)] = self.target_range
        if self.facing in (UP, DOWN):
            assert source_from_y == source_to_y
            if len(self.turn_needed) == 1:
                assert target_from_x == target_to_x
            else:
                assert target_from_y == target_to_y
        else:
            assert source_from_x == source_to_x
            if len(self.turn_needed) == 1:
                assert target_from_y == target_to_y
            else:
                assert target_from_x == target_to_x

    def is_applicable(self, coord, facing):
        if facing != self.facing:
            return False
        x, y = coord
        [(source_from_x, source_from_y), (source_to_x, source_to_y)] = self.source_range
        if facing in (UP, DOWN) and y == source_from_y and source_from_x <= x <= source_to_x:
            return True
        if facing in (LEFT, RIGHT) and x == source_from_x and source_from_y <= y <= source_to_y:
            return True
        return False

    def apply(self, coord, facing):
        assert self.is_applicable(coord, facing)
        x, y = coord
        [(source_from_x, source_from_y), (source_to_x, source_to_y)] = self.source_range
        [(target_from_x, target_from_y), (target_to_x, target_to_y)] = self.target_range
        assert source_to_x >= source_from_x and source_to_y >= source_from_y
        offset = (y - source_from_y) if source_from_x == source_to_x else (x - source_from_x)
        if target_from_x == target_to_x:
            if target_to_y > target_from_y:
                res = (target_from_x, target_from_y + offset), self.turn_needed
            else:
                res = (target_from_x, target_from_y - offset), self.turn_needed
        else:
            if target_to_x > target_from_x:
                res = (target_from_x + offset, target_from_y), self.turn_needed
            else:
                res = (target_from_x - offset, target_from_y), self.turn_needed
        return res