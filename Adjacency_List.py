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

    def print_list(self):
        """
        Imprime la lista de adyacencia.
        """
        temp = self.head
        while temp:
            print(f"Origen: {temp.origen}")
            adj_temp = temp.adjacency_list
            while adj_temp:
                print(f"  -> Destino: {adj_temp.ruta.destino}, Tiempo: {adj_temp.ruta.tiempo} minutos")
                adj_temp = adj_temp.next
            temp = temp.next

    def generate_graphviz(self, filename="adjacency_list"):
        """
        Genera una representación visual de la lista de adyacencia usando Graphviz.

        :param filename: Nombre del archivo de salida.
        """
        dot = Digraph()
        dot.attr(rankdir='LR', shape='record')

        temp = self.head
        while temp:
            node_label = f"{temp.origen}"
            dot.node(temp.origen, node_label)

            adj_temp = temp.adjacency_list
            while adj_temp:
                dest_label = f"{adj_temp.ruta.destino}\n{adj_temp.ruta.tiempo} min"
                dot.node(adj_temp.ruta.destino, dest_label)
                dot.edge(temp.origen, adj_temp.ruta.destino, label=f"{adj_temp.ruta.tiempo} min")
                adj_temp = adj_temp.next

            temp = temp.next

        dot.render(filename, format="png", cleanup=True)


# Ejemplo de uso
if __name__ == "__main__":
    from Route import Ruta  # Importamos la clase Ruta

    adj_list = AdjacencyList()

    # Creando rutas
    # Creando rutas
    ruta1 = Ruta("Quetzaltenango", "Huehuetenango", 90)
    ruta2 = Ruta("Quetzaltenango", "San Marcos", 75)
    ruta3 = Ruta("Quetzaltenango", "Retalhuleu", 85)
    ruta4 = Ruta("Huehuetenango", "San Marcos", 60)
    ruta5 = Ruta("Huehuetenango", "Alta Verapaz", 80)
    ruta6 = Ruta("San Marcos", "Retalhuleu", 50)
    ruta7 = Ruta("San Marcos", "Mazatenango", 70)
    ruta8 = Ruta("Retalhuleu", "Mazatenango", 40)
    ruta9 = Ruta("Retalhuleu", "Escuintla", 60)
    ruta10 = Ruta("Mazatenango", "Escuintla", 35)
    ruta11 = Ruta("Escuintla", "Guatemala", 50)
    ruta12 = Ruta("Escuintla", "Santa Rosa", 45)
    ruta13 = Ruta("Guatemala", "Chiquimula", 80)
    ruta14 = Ruta("Guatemala", "Sacatepequez", 25)
    ruta15 = Ruta("Guatemala", "Antigua", 30)
    ruta16 = Ruta("Chiquimula", "Zacapa", 45)
    ruta17 = Ruta("Chiquimula", "Jalapa", 50)
    ruta18 = Ruta("Zacapa", "Izabal", 70)
    ruta19 = Ruta("Zacapa", "Alta Verapaz", 65)
    ruta20 = Ruta("Izabal", "Puerto Barrios", 30)
    ruta21 = Ruta("Izabal", "Livingston", 50)
    ruta22 = Ruta("Puerto Barrios", "Livingston", 25)
    ruta23 = Ruta("Puerto Barrios", "El Estor", 40)
    ruta24 = Ruta("El Estor", "Izabal", 35)
    ruta25 = Ruta("El Estor", "Alta Verapaz", 100)
    ruta26 = Ruta("Alta Verapaz", "Baja Verapaz", 60)
    ruta27 = Ruta("Alta Verapaz", "Huehuetenango", 80)
    ruta28 = Ruta("Baja Verapaz", "El Progreso", 50)
    ruta29 = Ruta("Baja Verapaz", "Jalapa", 55)
    ruta30 = Ruta("El Progreso", "Jalapa", 45)
    ruta31 = Ruta("El Progreso", "Jutiapa", 60)
    ruta32 = Ruta("Jalapa", "Jutiapa", 55)
    ruta33 = Ruta("Jutiapa", "Santa Rosa", 35)
    ruta34 = Ruta("Santa Rosa", "Guatemala", 60)
    ruta35 = Ruta("Sacatepequez", "Antigua", 20)
    ruta36 = Ruta("Antigua", "Guatemala", 25)
    ruta37 = Ruta("Antigua", "Santa Rosa", 50)

    # Insertando en la lista de adyacencia
    adj_list.insert("Quetzaltenango", ruta1)
    adj_list.insert("Quetzaltenango", ruta2)
    adj_list.insert("Quetzaltenango", ruta3)
    adj_list.insert("Huehuetenango", ruta4)
    adj_list.insert("Huehuetenango", ruta5)
    adj_list.insert("San Marcos", ruta6)
    adj_list.insert("San Marcos", ruta7)
    adj_list.insert("Retalhuleu", ruta8)
    adj_list.insert("Retalhuleu", ruta9)
    adj_list.insert("Mazatenango", ruta10)
    adj_list.insert("Escuintla", ruta11)
    adj_list.insert("Escuintla", ruta12)
    adj_list.insert("Guatemala", ruta13)
    adj_list.insert("Guatemala", ruta14)
    adj_list.insert("Guatemala", ruta15)
    adj_list.insert("Chiquimula", ruta16)
    adj_list.insert("Chiquimula", ruta17)
    adj_list.insert("Zacapa", ruta18)
    adj_list.insert("Zacapa", ruta19)
    adj_list.insert("Izabal", ruta20)
    adj_list.insert("Izabal", ruta21)
    adj_list.insert("Puerto Barrios", ruta22)
    adj_list.insert("Puerto Barrios", ruta23)
    adj_list.insert("El Estor", ruta24)
    adj_list.insert("El Estor", ruta25)
    adj_list.insert("Alta Verapaz", ruta26)
    adj_list.insert("Alta Verapaz", ruta27)
    adj_list.insert("Baja Verapaz", ruta28)
    adj_list.insert("Baja Verapaz", ruta29)
    adj_list.insert("El Progreso", ruta30)
    adj_list.insert("El Progreso", ruta31)
    adj_list.insert("Jalapa", ruta32)
    adj_list.insert("Jutiapa", ruta33)
    adj_list.insert("Santa Rosa", ruta34)
    adj_list.insert("Sacatepequez", ruta35)
    adj_list.insert("Antigua", ruta36)
    adj_list.insert("Antigua", ruta37)

    # Imprimiendo la lista de adyacencia
    adj_list.print_list()

    # Generando el archivo Graphviz
    adj_list.generate_graphviz("adjacency_list_graph")
