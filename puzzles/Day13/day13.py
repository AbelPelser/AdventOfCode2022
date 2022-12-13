from typing import List

from util import read_input_as_blocks, safe_split


class MyList:
    def __init__(self, contents: List):
        self.contents = contents

    def __lt__(self, other):
        for my_item, other_item in zip(self.contents, other.contents):
            if isinstance(my_item, int) and isinstance(other_item, int):
                if my_item == other_item:
                    continue
                return my_item < other_item
            my_item = [my_item] if isinstance(my_item, int) else my_item
            other_item = [other_item] if isinstance(other_item, int) else other_item
            my_list_mine, my_list_other = MyList(my_item), MyList(other_item)
            if my_list_mine == my_list_other:
                continue
            return my_list_mine < my_list_other
        return len(self.contents) < len(other.contents)

    def __eq__(self, other):
        if len(self.contents) != len(other.contents):
            return False
        for my_item, other_item in zip(self.contents, other.contents):
            if isinstance(my_item, int) and isinstance(other_item, int):
                if my_item != other_item:
                    return False
                continue
            my_item = [my_item] if isinstance(my_item, int) else my_item
            other_item = [other_item] if isinstance(other_item, int) else other_item
            if MyList(my_item) != MyList(other_item):
                return False
        return True

    def __len__(self):
        return len(self.contents)


def part1():
    blocks = read_input_as_blocks()
    indices_in_the_right_order = []
    for i, block in enumerate(blocks):
        list1, list2 = (eval(line) for line in safe_split(block))
        if MyList(list1) < MyList(list2):
            indices_in_the_right_order.append(i + 1)
    return sum(indices_in_the_right_order)


def part2():
    blocks = read_input_as_blocks()
    all_lists = [MyList(eval(line)) for block in blocks for line in safe_split(block)]
    p2 = MyList([[2]])
    p6 = MyList([[6]])
    all_lists += [p2, p6]
    sorted_lists = sorted(all_lists)
    return (sorted_lists.index(p2) + 1) * (sorted_lists.index(p6) + 1)


if __name__ == '__main__':
    print(part1())
    print(part2())
