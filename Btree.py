from graphviz import Digraph

class Node:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, t=5):
        """
        Inicializa un Árbol B de orden t (grado mínimo).
        :param t: Orden del árbol B.
        """
        self.root = Node(leaf=True)
        self.t = t

    def print_tree(self, x, lvl=0):
        """
        Imprime el Árbol B en niveles.
        :param x: Nodo raíz.
        :param lvl: Nivel actual.
        """
        print("Nivel", lvl, "->", len(x.keys), end=": ")
        for k in x.keys:
            print(k, end=" ")
        print()
        lvl += 1
        for child in x.children:
            self.print_tree(child, lvl)

    def insert(self, k):
        """
        Inserta una clave en el Árbol B.
        :param k: Clave a insertar.
        """
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = Node()
            self.root = temp
            temp.children.append(root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, x, k):
        """
        Inserta una clave en un nodo no lleno.
        :param x: Nodo donde insertar.
        :param k: Clave a insertar.
        """
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(None)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_non_full(x.children[i], k)

    def _split_child(self, x, i):
        """
        Divide un nodo hijo lleno.
        :param x: Nodo padre.
        :param i: Índice del hijo a dividir.
        """
        t = self.t
        y = x.children[i]
        z = Node(leaf=y.leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:]
        y.keys = y.keys[:t - 1]

        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

    def generate_graphviz(self, filename="btree_visualization"):
        """
        Genera una representación visual del Árbol B usando Graphviz.
        :param filename: Nombre del archivo de salida.
        """
        def add_nodes_edges(dot, node, parent_id=None):
            node_id = id(node)
            label = " | ".join(map(str, node.keys))
            dot.node(str(node_id), f"{{ {label} }}", shape="record")

            if parent_id is not None:
                dot.edge(str(parent_id), str(node_id))

            for child in node.children:
                add_nodes_edges(dot, child, node_id)

        dot = Digraph()
        dot.attr(rankdir='TB', shape='record')  # Vertical layout to show correct levels

        if self.root:
            add_nodes_edges(dot, self.root)

        dot.render(filename, format="png", cleanup=True)

# Ejemplo de uso
if __name__ == "__main__":
    b_tree = BTree(t=5)  # Orden 5

    # Vehículos con claves y datos
    vehicles = [
        ("P0123ABC", "Toyota", "Corolla", 23.5),
        ("P0456DEF", "Honda", "Civic", 22.0),
        ("P0789GHI", "Ford", "Focus", 21.5),
        ("P0123JKL", "Chevrolet", "Cruze", 24.0),
        ("P0456MNO", "Nissan", "Sentra", 23.0),
        ("P0789PQR", "Hyundai", "Elantra", 22.5),
        ("P0123STU", "Kia", "Optima", 24.5),
        ("P0456VWX", "Volkswagen", "Jetta", 25.0),
        ("P0789YZA", "Subaru", "Impreza", 23.5),
        ("P0123BCD", "Mazda", "3", 24.0),
        ("P0456EFG", "BMW", "3 Series", 35.0),
        ("P0789HIJ", "Mercedes-Benz", "C-Class", 36.5),
        ("P0123KLM", "Audi", "A4", 34.0),
        ("P0456NOP", "Lexus", "IS", 33.5),
        ("P0789QRS", "Acura", "TLX", 32.0),
        ("P0123TUV", "Infiniti", "Q50", 31.5),
        ("P0456WXY", "Cadillac", "ATS", 30.0),
        ("P0789ZAB", "Jaguar", "XE", 37.0),
        ("P0123CDE", "Alfa Romeo", "Giulia", 38.5),
        ("P0456FGH", "Genesis", "G70", 29.5),
    ]

    # Inserta los vehículos en el Árbol B usando solo las placas como claves
    for vehicle in vehicles:
        b_tree.insert(vehicle[0])

    print("Árbol B generado:")
    b_tree.print_tree(b_tree.root)

    print("\nGenerando Graphviz...")
    b_tree.generate_graphviz("btree_visualization")
