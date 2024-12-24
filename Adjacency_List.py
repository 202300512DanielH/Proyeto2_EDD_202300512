from graphviz import Digraph

class SubNode:
    def __init__(self, ruta):
        """
        Constructor para un subnodo de la lista de adyacencia.

        :param ruta: Objeto de la clase Ruta que representa la conexión.
        """
        self.ruta = ruta
        self.next = None


class Node:
    def __init__(self, origen):
        """
        Constructor para un nodo principal de la lista de adyacencia.

        :param origen: Nodo principal que representa el origen.
        """
        self.origen = origen
        self.adjacency_list = None
        self.next = None

    def append(self, ruta):
        """
        Agrega un subnodo (ruta) a la lista de adyacencia.

        :param ruta: Objeto de la clase Ruta que representa la conexión.
        """
        new_node = SubNode(ruta)
        if not self.adjacency_list:
            self.adjacency_list = new_node
        else:
            temp = self.adjacency_list
            while temp.next:
                temp = temp.next
            temp.next = new_node


class AdjacencyList:
    def __init__(self):
        """
        Constructor para la lista de adyacencia.
        """
        self.head = None

    def insert(self, origen, ruta):
        """
        Inserta una nueva ruta en la lista de adyacencia.

        :param origen: Nodo origen de la ruta.
        :param ruta: Objeto de la clase Ruta que representa la conexión.
        """
        if not self.head:
            new_node = Node(origen)
            new_node.append(ruta)
            self.head = new_node
        else:
            temp = self.head
            while temp:
                if temp.origen == origen:
                    temp.append(ruta)
                    return
                if not temp.next:
                    break
                temp = temp.next

            new_node = Node(origen)
            new_node.append(ruta)
            temp.next = new_node

    def modify(self, origen, destino, nuevo_tiempo):
        """
        Modifica el tiempo de una ruta existente.

        :param origen: Nodo origen de la ruta.
        :param destino: Nodo destino de la ruta.
        :param nuevo_tiempo: Nuevo tiempo de la ruta (int o float).
        """
        temp = self.head
        while temp:
            if temp.origen == origen:
                adj_temp = temp.adjacency_list
                while adj_temp:
                    if adj_temp.ruta.destino == destino:
                        if nuevo_tiempo <= 0:
                            raise ValueError("El tiempo de la ruta debe ser un número positivo.")
                        adj_temp.ruta.tiempo = nuevo_tiempo
                        print(f"Ruta modificada: {origen} -> {destino}, Nuevo tiempo: {nuevo_tiempo} minutos")
                        return
                    adj_temp = adj_temp.next
            temp = temp.next

        raise ValueError(f"No se encontró la ruta desde {origen} hasta {destino}.")

    def delete(self, origen, destino):
        """
        Elimina una ruta de la lista de adyacencia.

        :param origen: Nodo origen de la ruta.
        :param destino: Nodo destino de la ruta.
        """
        temp = self.head
        while temp:
            if temp.origen == origen:
                prev = None
                adj_temp = temp.adjacency_list
                while adj_temp:
                    if adj_temp.ruta.destino == destino:
                        if prev:
                            prev.next = adj_temp.next
                        else:
                            temp.adjacency_list = adj_temp.next
                        print(f"Ruta eliminada: {origen} -> {destino}")
                        return
                    prev = adj_temp
                    adj_temp = adj_temp.next
            temp = temp.next

        raise ValueError(f"No se encontró la ruta desde {origen} hasta {destino}.")

    def show_information(self, origen=None):
        """
        Muestra información sobre todas las rutas o las rutas específicas de un origen.

        :param origen: Nodo origen para filtrar (opcional).
        """
        temp = self.head
        found = False
        while temp:
            if origen is None or temp.origen == origen:
                found = True
                print(f"Origen: {temp.origen}")
                adj_temp = temp.adjacency_list
                while adj_temp:
                    print(f"  -> Destino: {adj_temp.ruta.destino}, Tiempo: {adj_temp.ruta.tiempo} minutos")
                    adj_temp = adj_temp.next
            temp = temp.next

        if not found and origen:
            print(f"No se encontraron rutas desde el origen: {origen}")

    def print_list(self):
        """
        Imprime la lista de adyacencia.
        """
        self.show_information()

    def generate_graphviz(self, filename="adjacency_list"):
        """
        Genera una representación visual de la lista de adyacencia usando Graphviz.

        :param filename: Nombre del archivo de salida.
        """
        dot = Digraph()
        dot.attr(rankdir='LR', shape='record')

        temp = self.head
        while temp:
            # Establecer color turquesa y estilo para los nodos
            node_label = f"{temp.origen}"
            dot.node(temp.origen, node_label, style="filled", fillcolor="turquoise")

            adj_temp = temp.adjacency_list
            while adj_temp:
                dest_label = f"{adj_temp.ruta.destino}\n{adj_temp.ruta.tiempo} min"
                dot.node(adj_temp.ruta.destino, dest_label, style="filled", fillcolor="turquoise")
                dot.edge(temp.origen, adj_temp.ruta.destino, label=f"{adj_temp.ruta.tiempo} min")
                adj_temp = adj_temp.next

            temp = temp.next

        dot.render(filename, format="png", cleanup=True)



