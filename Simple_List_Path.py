from Path import camino
import graphviz
class Node:
    def __init__(self, path):
        self.path = path
        self.next = None

class SimpleListPath:
    def __init__(self):
        self.head = None

    def insert(self, path):
        new_node = Node(path)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

    def to_dot(self):
        dot_str = "digraph G {\n"
        dot_str += "rankdir=LR;\n"
        current = self.head
        node_id = 0
        while current is not None:
            dot_str += f'node{node_id} [label="{current.path.origen} -> {current.path.destino} ({current.path.duracion})"];\n'
            if current.next is not None:
                dot_str += f'node{node_id} -> node{node_id + 1};\n'
            current = current.next
            node_id += 1
        dot_str += "}\n"
        return dot_str

    def save_png(self, filename):
        dot_str = self.to_dot()
        graph = graphviz.Source(dot_str)
        graph.format = 'png'
        graph.render(filename, cleanup=True)
