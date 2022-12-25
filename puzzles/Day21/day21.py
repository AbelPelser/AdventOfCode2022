from typing import Optional

from util import read_input_as_lines

HOLDERS = {}


class Monkey:
    def __init__(self, left: Optional[str], right: Optional[str]):
        self.left_name = left
        self.right_name = right
        self.left: Optional[Monkey] = None
        self.right: Optional[Monkey] = None
        self.parent: Optional[Monkey] = None
        self.in_path_to_human = False

    def get_children(self, monkey_dict):
        if self.left_name is not None:
            self.left = monkey_dict[self.left_name]
        if self.right_name is not None:
            self.right = monkey_dict[self.right_name]

    def find_value_for_human(self, intended_result):
        raise Exception('Not implemented')

    def touch_children(self):
        if self.left:
            self.left.parent = self
            self.left.touch_children()
        if self.right:
            self.right.parent = self
            self.right.touch_children()

    def propagate_path_to_human(self):
        if self.in_path_to_human and self.parent is not None:
            self.parent.in_path_to_human = True
            self.parent.propagate_path_to_human()

    def evaluate(self):
        raise Exception('Not implemented')


class Literal(Monkey):
    def __init__(self, value):
        super().__init__(None, None)
        self.value = value

    def find_value_for_human(self, intended_result):
        # We are the human!
        return intended_result

    def evaluate(self):
        return self.value


class Div(Monkey):
    def __init__(self, left: str, right: str):
        super().__init__(left, right)

    def find_value_for_human(self, intended_result):
        if self.left.in_path_to_human:
            return self.left.find_value_for_human(intended_result * self.right.evaluate())
        return self.right.find_value_for_human(self.left.evaluate() / intended_result)

    def evaluate(self):
        return self.left.evaluate() / self.right.evaluate()


class Add(Monkey):
    def __init__(self, left: str, right: str):
        super().__init__(left, right)

    def find_value_for_human(self, intended_result):
        if self.left.in_path_to_human:
            return self.left.find_value_for_human(intended_result - self.right.evaluate())
        return self.right.find_value_for_human(intended_result - self.left.evaluate())

    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()


class Sub(Monkey):
    def __init__(self, left: str, right: str):
        super().__init__(left, right)

    def find_value_for_human(self, intended_result):
        if self.left.in_path_to_human:
            return self.left.find_value_for_human(intended_result + self.right.evaluate())
        return self.right.find_value_for_human(self.left.evaluate() - intended_result)

    def evaluate(self):
        return self.left.evaluate() - self.right.evaluate()


class Mult(Monkey):
    def __init__(self, left: str, right: str):
        super().__init__(left, right)

    def find_value_for_human(self, intended_result):
        if self.left.in_path_to_human:
            return self.left.find_value_for_human(intended_result / self.right.evaluate())
        return self.right.find_value_for_human(intended_result / self.left.evaluate())

    def evaluate(self):
        return self.left.evaluate() * self.right.evaluate()


class Equals(Monkey):
    def __init__(self, left: str, right: str):
        super().__init__(left, right)

    def evaluate(self):
        return self.left.evaluate() == self.right.evaluate()

    def find_value_for_human(self, intended_value=None):
        variable, given = (self.left, self.right) if self.left.in_path_to_human else (self.right, self.left)
        return variable.find_value_for_human(given.evaluate())


OP_DICT = {'+': Add, '-': Sub, '*': Mult, '/': Div}


def parse(root_is_equals_check=False):
    lines = read_input_as_lines()
    monkey_dict = {}
    for line in lines:
        name, rest = line.split(': ')
        if name == 'root' and root_is_equals_check:
            left, right = rest.split(' ')[0], rest.split(' ')[-1]
            monkey_dict[name] = Equals(left, right)
        elif rest.isdigit():
            monkey_dict[name] = Literal(int(rest))
        else:
            for op, clazz in OP_DICT.items():
                if op in rest:
                    left, right = rest.split(f' {op} ')
                    monkey_dict[name] = clazz(left, right)
                    break
    for holder in monkey_dict.values():
        holder.get_children(monkey_dict)
    return monkey_dict


def part1():
    return round(parse()['root'].evaluate())


def part2():
    monkey_dict = parse(root_is_equals_check=True)
    root = monkey_dict['root']
    root.touch_children()
    human = monkey_dict['humn']
    human.in_path_to_human = True
    human.propagate_path_to_human()
    return round(root.find_value_for_human())


if __name__ == '__main__':
    print(part1())
    print(part2())
