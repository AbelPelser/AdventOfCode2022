import re
from functools import reduce

from util import read_input_as_blocks


class Item:
    def __init__(self, value, _):
        self.value = value

    def process_operator(self, op):
        self.value = op(self.value) // 3


class ItemPart2(Item):
    def __init__(self, value, monkeys):
        super().__init__(value, monkeys)
        self.value_mod_monkey = {
            m_: value % m_.test_divisible_by
            for m_ in monkeys
        }

    def process_operator(self, op):
        self.value_mod_monkey = {
            m_: op(value) % m_.test_divisible_by
            for m_, value in self.value_mod_monkey.items()
        }


class Monkey:
    def __init__(self, items, test_divisible_by, to_if_true, to_if_false, op_string):
        self.items = items
        self.op = lambda old: eval(op_string)
        self.test_divisible_by = test_divisible_by
        self.to_if_true = to_if_true
        self.to_if_false = to_if_false
        self.n_inspected = 0
        self.item_class = Item

    def inspect_all(self):
        for item in self.items:
            self.n_inspected += 1
            item.process_operator(self.op)
            self.find_target(item).items.append(item)
        self.items = []

    def find_target(self, item: Item):
        return self.to_if_true if item.value % self.test_divisible_by == 0 else self.to_if_false

    def convert_to_objects(self, monkeys):
        self.items = [self.item_class(i, monkeys) for i in self.items]
        self.to_if_true = monkeys[self.to_if_true]
        self.to_if_false = monkeys[self.to_if_false]


class MonkeyPart2(Monkey):
    def __init__(self, items, test_divisible_by, to_if_true, to_if_false, op_string):
        super().__init__(items, test_divisible_by, to_if_true, to_if_false, op_string)
        self.item_class = ItemPart2

    def find_target(self, item: ItemPart2):
        return self.to_if_true if item.value_mod_monkey[self] == 0 else self.to_if_false


MONKEY_REGEX = """Monkey (\d+):
 {2}Starting items: (\d+(?:, \d+)*)?
 {2}Operation: new = ([a-z0-9 *+/%]+)
 {2}Test: divisible by (\d+)
 {4}If true: throw to monkey (\d+)
 {4}If false: throw to monkey (\d+)"""


def parse(is_part2=False):
    monkeys = []
    monkey_strings = read_input_as_blocks()
    for monkey_string in monkey_strings:
        i, starting_items, op_string, test_divisible_by, to_if_true, to_if_false = re.match(MONKEY_REGEX,
                                                                                            monkey_string).groups()
        starting_items = list(map(int, starting_items.split(', ')))
        monkey_class = MonkeyPart2 if is_part2 else Monkey
        monkey = monkey_class(starting_items, int(test_divisible_by), int(to_if_true), int(to_if_false), op_string)
        monkeys.append(monkey)
    for monkey in monkeys:
        monkey.convert_to_objects(monkeys)
    return monkeys


def calculate_monkey_business(monkeys):
    monkeys = sorted(monkeys, key=lambda monkey: monkey.n_inspected)
    return reduce(lambda a, b: a.n_inspected * b.n_inspected, monkeys[-2:])


def part1():
    monkeys = parse()
    for _ in range(20):
        for monkey in monkeys:
            monkey.inspect_all()
    return calculate_monkey_business(monkeys)


def part2():
    monkeys = parse(is_part2=True)
    for _ in range(10000):
        for monkey in monkeys:
            monkey.inspect_all()
    return calculate_monkey_business(monkeys)


if __name__ == '__main__':
    print(part1())
    print(part2())
