from graphviz import Digraph
from Client import Client

class Node:
    def __init__(self, client):
        """
        Constructor para el nodo de la lista.

        :param client: Instancia de la clase Client.
        """
        self.client = client
        self.next = None
        self.prev = None

class DoublyCircularLinkedList:
    def __init__(self):
        """
        Constructor para la lista circular doblemente enlazada.
        """
        self.head = None

    def is_empty(self):
        """
        Verifica si la lista está vacía.
        """
        return self.head is None

    def add(self, client):
        """
        Añade un nuevo cliente a la lista.

        :param client: Instancia de la clase Client.
        """
        new_node = Node(client)
        if self.is_empty():
            self.head = new_node
            self.head.next = self.head
            self.head.prev = self.head
        else:
            tail = self.head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

    def remove(self, dpi):
        """
        Elimina un cliente de la lista por su DPI.

        :param dpi: DPI del cliente a eliminar.
        """
        if self.is_empty():
            return False

        current = self.head
        while True:
            if current.client.dpi == dpi:
                if current.next == current:  # Solo un nodo en la lista
                    self.head = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    if current == self.head:
                        self.head = current.next
                return True
            current = current.next
            if current == self.head:
                break
        return False

    def generate_graphviz(self, filename="circular_list"):
        """
        Genera una representación de la lista en formato Graphviz.

        :param filename: Nombre del archivo para guardar la imagen.
        """
        if self.is_empty():
            print("La lista está vacía.")
            return

        dot = Digraph()
        dot.attr(rankdir='LR', shape='record')

        current = self.head
        while True:
            node_label = f"DPI: {current.client.dpi}\nNombres: {current.client.nombres}"
            dot.node(str(id(current)), node_label)

            if current.next:
                dot.edge(str(id(current)), str(id(current.next)), constraint='true')
                dot.edge(str(id(current.next)), str(id(current)), constraint='true')

            current = current.next
            if current == self.head:
                break

        dot.render(filename, format="png", cleanup=True)

    def display(self):
        """
        Muestra los clientes en la lista.
        """
        if self.is_empty():
            print("La lista está vacía.")
            return

        current = self.head
        while True:
            print(current.client)
            current = current.next
            if current == self.head:
                break


"""
if __name__ == "__main__":
    lista = DoublyCircularLinkedList()
    lista.add(Client("123456789", "Juan Pérez"))
    lista.add(Client("987654321", "María López"))
    lista.add(Client("456789123", "Carlos Pérez"))
    lista.add(Client("789123456", "Ana López"))

    lista.display()
  lista.generate_graphviz()
"""