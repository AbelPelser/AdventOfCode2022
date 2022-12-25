class LinkedList:
    def __init__(self):
        self.tail = None
        self.head = None
        self.original_order_dict = {}
        self.current_order_dict = {}
        self.node_by_value_dict = {}
        self.n_nodes = 0

    def add_node(self, index, value):
        new = Node(value, index)
        self.n_nodes += 1
        self.original_order_dict[index] = new
        self.current_order_dict[index] = new
        self.node_by_value_dict[value] = new
        if self.head:
            self.head.next = new
        new.prev = self.head
        self.head = new
        if not self.tail:
            self.tail = new

    def get_node_by_current_index(self, index):
        return self.current_order_dict[index % len(self.current_order_dict)]

    def make_circular(self):
        self.head.next = self.tail
        self.tail.prev = self.head

    def set_current_index_for_node(self, node, current_index):
        node.current_index = current_index
        self.current_order_dict[current_index] = node

    def rotate_node_left(self, node, amount):
        self.set_current_index_for_node(node, (node.current_index - amount) % self.n_nodes)

    def rotate_node_right(self, node, amount):
        self.set_current_index_for_node(node, (node.current_index + amount) % self.n_nodes)

    def rotate_all_left(self, amount):
        if amount < 0:
            self.rotate_all_right(-amount)
            return
        for node in list(self.current_order_dict.values()):
            self.rotate_node_left(node, amount)

    def rotate_all_right(self, amount):
        if amount < 0:
            self.rotate_all_left(-amount)
            return
        for node in list(self.current_order_dict.values()):
            self.rotate_node_left(node, amount)

    def rotate_left(self, amount, frm=0, to=0):
        frm %= self.n_nodes
        to %= self.n_nodes
        node = self.current_order_dict[frm]
        while True:
            original_current_index = node.current_index
            if original_current_index == to:
                break
            self.rotate_node_left(node, amount)
            node = node.next

    def rotate_right(self, amount, frm=0, to=0):
        node = self.current_order_dict[frm]
        while True:
            original_current_index = node.current_index
            self.rotate_node_right(node, amount)
            if original_current_index == to:
                break
            node = node.prev

    def move_by_value(self, original_index):
        node = self.original_order_dict[original_index]
        amount = node.value % (self.n_nodes * (self.n_nodes - 1))
        original_current_index = node.current_index
        n_left = (original_current_index + amount) // self.n_nodes
        target_index = (original_current_index + amount) % self.n_nodes
        self.rotate_all_left(n_left)
        had_extra_shift = False
        if original_current_index < target_index and original_current_index < node.current_index:
            self.rotate_all_left(1)
            had_extra_shift = True
        new_current_index = node.current_index
        if target_index > new_current_index:
            self.rotate_left(1, frm=new_current_index + 1, to=target_index + 1)
            LinkedList.unlink_node(node)
            self.set_current_index_for_node(node, target_index)
            LinkedList.insert_node(node, self.current_order_dict[(target_index - 1) % self.n_nodes])
        elif target_index < new_current_index:
            if new_current_index >= original_current_index and not had_extra_shift:
                self.rotate_all_left(1)
            new_current_index = node.current_index
            if new_current_index != target_index:
                self.rotate_right(1, frm=new_current_index - 1, to=target_index)
            LinkedList.unlink_node(node)
            self.set_current_index_for_node(node, target_index)
            LinkedList.insert_node(node, self.current_order_dict[(target_index - 1) % self.n_nodes])

    @staticmethod
    def unlink_node(node):
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node.next = None

    @staticmethod
    def remove_segment(after_node, n_nodes):
        if n_nodes == 0:
            return None
        start = end = after_node.next
        for i in range(n_nodes - 1):
            end = end.next
        start.prev.next = end.next
        end.next.prev = start.prev
        start.prev = None
        end.next = None
        return start, end

    @staticmethod
    def insert_segment(start, end, after_node):
        after_node.next.prev = end
        end.next = after_node.next
        after_node.next = start
        start.prev = after_node

    @staticmethod
    def insert_node(node, after_node):
        after_node.next.prev = node
        node.next = after_node.next
        after_node.next = node
        node.prev = after_node

    def to_str_by_current_index(self):
        output = []
        for i in range(len(self.current_order_dict)):
            output.append(str(self.current_order_dict[i].value))
        return ', '.join(output)


class Node:
    def __init__(self, value, current_index):
        self.prev = None
        self.next = None
        self.value = value
        self.current_index = current_index

    def __repr__(self):
        return str(self.value)
