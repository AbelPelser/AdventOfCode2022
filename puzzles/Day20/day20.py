from puzzles.Day20.linkedlist import LinkedList
from util import read_input_as_lines


def parse(key=None):
    lines = list(map(int, read_input_as_lines()))
    linked_list = LinkedList()
    for i, value in enumerate(lines):
        linked_list.add_node(i, value * key if key is not None else value)
    linked_list.make_circular()
    return linked_list

def part1():
    linked_list = parse()
    length = linked_list.n_nodes
    for index in range(length):
        linked_list.move_by_value(index)
    index_of_0 = linked_list.node_by_value_dict[0].current_index
    return sum(linked_list.get_node_by_current_index(index_of_0 + i).value for i in (1000, 2000, 3000))



def part2():
    linked_list = parse(key=811589153)
    for i in range(10):
        print(f'Mix {i}')
        for index in range(linked_list.n_nodes):
            linked_list.move_by_value(index)
    index_of_0 = linked_list.node_by_value_dict[0].current_index
    return sum(linked_list.get_node_by_current_index(index_of_0 + i).value for i in (1000, 2000, 3000))


if __name__ == '__main__':
    print(part1())
    print(part2())
