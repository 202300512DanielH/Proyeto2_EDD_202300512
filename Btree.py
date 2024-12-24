from graphviz import Digraph
from graphviz import Source
from Vehicle import Vehiculo
import math

"""
ESTE ES EL CÓDIGO BASADO DEL ÁRBOL B QUE VIMOS EN CLASE, YA QUE DESPUÉS DE DEMASIADO TIEMPO NO PUDE HACER QUE FUNCIONARA EL QUE ESTABA CREANDO DE MANERA
PROPIA AGRADEZCO DE ANTEMANO SU COMPRENSIÓN
"""
class Node:
    def __init__(self, leaf: bool = False):
        self.leaf: bool = leaf
        self.keys: list[Vehiculo] = []
        self.children: list[Node] = []

    def __str__(self):
        return f"Leaf: {self.leaf}, Keys: {self.keys}, Children: {self.children}"

class BTree:
    def __init__(self, t: int):
        self.root: Node = Node(leaf=True)
        self.t: int = t

    def __str__(self):
        return f"{self.root}"

    def insert_value(self, value: Vehiculo):
        root: Node = self.root
        self.insert_non_full(root, value)
        if len(root.keys) > self.t - 1:
            node: Node = Node()
            self.root = node
            node.children.insert(0, root)
            self.split_page(node, 0)

    def insert_non_full(self, root: Node, value: Vehiculo):
        i: int = len(root.keys) - 1
        if root.leaf:
            root.keys.append(None)
            while i >= 0 and value.placa < root.keys[i].placa:
                root.keys[i + 1] = root.keys[i]
                i -= 1
            root.keys[i + 1] = value
        else:
            while i >= 0 and value.placa < root.keys[i].placa:
                i -= 1
            i += 1
            self.insert_non_full(root.children[i], value)
            if len(root.children[i].keys) > self.t - 1:
                self.split_page(root, i)

    def split_page(self, root: Node, i: int):
        mid_position: int = int((self.t - 1) / 2)
        child: Node = root.children[i]
        node: Node = Node(child.leaf)
        root.children.insert(i + 1, node)
        root.keys.insert(i, child.keys[mid_position])
        node.keys = child.keys[mid_position + 1:mid_position * 2 + 1]
        child.keys = child.keys[0:mid_position]
        if not child.leaf:
            node.children = child.children[mid_position + 1:mid_position * 2 + 2]
            child.children = child.children[0:mid_position + 1]

    def print_tree(self, nodo: Node, id: list[int] = [0]) -> str:
        root: Node = nodo
        tree = f'n{id[0]} [label="'
        counter: int = 0
        for item in root.keys:
            if counter == len(root.keys) - 1:
                tree += f"<f{counter}> |{item.placa}|<f{counter + 1}>"
                break
            tree += f"<f{counter}> |{item.placa}|"
            counter += 1
        tree += "\"];\n\t"
        counter = 0
        id_father = id[0]
        for item in root.children:
            tree += f'n{id_father}:f{counter} -> n{id[0] + 1};\n\t'
            id[0] += 1
            tree += self.print_tree(item, id)
            counter += 1
        return tree

    def print_vehicle(self) -> str:
        dot = 'digraph G {\n\tbgcolor="white";\n\t'
        dot += "fontcolor = black;\n\tnodesep=0.5;\n\tsplines=false;\n\t"
        dot += 'node [shape=record width=1.2 style=filled fillcolor=turquoise;\n\t'
        dot += "fontcolor=black color=transparent];\n\t"
        dot += 'edge [fontcolor= white color = black];\n\t'
        dot += self.print_tree(self.root)
        dot += '}'
        return dot

    #INTENANDO CREAR LA ELIMINACION:

    def delete(self, value: Vehiculo):
        """
        Elimina un valor del árbol B y asegura el balance.
        """
        self.delete_from_node(self.root, value)

        # Si la raíz está vacía y tiene hijos, ajusta la raíz
        if len(self.root.keys) == 0:
            if not self.root.leaf:
                self.root = self.root.children[0]
            else:
                self.root = None  # El árbol queda vacío

    def delete_from_node(self, node: Node, value: Vehiculo):
        """
        Elimina un valor de un nodo específico.
        """
        index = self.find_key(node, value)

        # Caso 1: El valor está en este nodo
        if index < len(node.keys) and node.keys[index].placa == value.placa:
            if node.leaf:
                # Caso hoja: simplemente elimina la clave
                node.keys.pop(index)
            else:
                # Caso nodo interno: maneja con predecesor o sucesor
                self.delete_internal_node(node, index)
        else:
            # Caso 2: El valor no está en este nodo
            if node.leaf:
                print(f"El valor {value.placa} no se encuentra en el árbol.")
                return

            # Asegúrate de que el hijo tenga al menos t claves antes de descender
            if len(node.children[index].keys) < self.t:
                self.fill(node, index)

            # Desciende al hijo adecuado
            # Nota: Si hubo fusión, el índice puede cambiar
            if index > len(node.keys):
                self.delete_from_node(node.children[index - 1], value)
            else:
                self.delete_from_node(node.children[index], value)

    def delete_internal_node(self, node: Node, index: int):
        """
        Maneja la eliminación de un valor en un nodo interno.
        """
        key = node.keys[index]

        # Si el hijo izquierdo tiene al menos t claves
        if len(node.children[index].keys) >= self.t:
            predecessor = self.get_predecessor(node, index)
            node.keys[index] = predecessor
            self.delete_from_node(node.children[index], predecessor)

        # Si el hijo derecho tiene al menos t claves
        elif len(node.children[index + 1].keys) >= self.t:
            successor = self.get_successor(node, index)
            node.keys[index] = successor
            self.delete_from_node(node.children[index + 1], successor)

        # Fusionar ambos hijos y eliminar del hijo fusionado
        else:
            self.merge(node, index)
            self.delete_from_node(node.children[index], key)

    def fill(self, node: Node, index: int):
        """
        Asegura que un hijo tenga al menos t - 1 claves.
        """
        if index > 0 and len(node.children[index - 1].keys) >= self.t:
            self.borrow_from_prev(node, index)
        elif index < len(node.children) - 1 and len(node.children[index + 1].keys) >= self.t:
            self.borrow_from_next(node, index)
        else:
            # Fusiona el hijo con uno de sus vecinos
            if index < len(node.children) - 1:
                self.merge(node, index)
            else:
                self.merge(node, index - 1)

    def borrow_from_prev(self, node: Node, index: int):
        """
        Pide prestada una clave del hijo anterior.
        """
        child = node.children[index]
        sibling = node.children[index - 1]

        # Mueve la última clave del hermano al padre
        child.keys.insert(0, node.keys[index - 1])
        node.keys[index - 1] = sibling.keys.pop()

        # Si no es hoja, mueve el último hijo del hermano al hijo
        if not sibling.leaf:
            child.children.insert(0, sibling.children.pop())

    def borrow_from_next(self, node: Node, index: int):
        """
        Pide prestada una clave del hijo siguiente.
        """
        child = node.children[index]
        sibling = node.children[index + 1]

        # Mueve la primera clave del hermano al padre
        child.keys.append(node.keys[index])
        node.keys[index] = sibling.keys.pop(0)

        # Si no es hoja, mueve el primer hijo del hermano al hijo
        if not sibling.leaf:
            child.children.append(sibling.children.pop(0))

    def merge(self, node: Node, index: int):
        """
        Fusiona dos hijos en un único hijo y asegura el balance.
        """
        child = node.children[index]
        sibling = node.children[index + 1]

        # Mueve la clave del padre al hijo
        child.keys.append(node.keys.pop(index))

        # Agrega las claves y los hijos del hermano al hijo
        child.keys.extend(sibling.keys)
        if not sibling.leaf:
            child.children.extend(sibling.children)

        # Elimina el puntero al hermano
        node.children.pop(index + 1)

    def get_predecessor(self, node: Node, index: int) -> Vehiculo:
        """
        Encuentra el predecesor de una clave.
        """
        current = node.children[index]
        while not current.leaf:
            current = current.children[-1]
        return current.keys[-1]

    def get_successor(self, node: Node, index: int) -> Vehiculo:
        """
        Encuentra el sucesor de una clave.
        """
        current = node.children[index + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    def find_key(self, node: Node, value: Vehiculo) -> int:
        """
        Encuentra la posición de una clave en un nodo.
        """
        for i, key in enumerate(node.keys):
            if key.placa >= value.placa:
                return i
        return len(node.keys)




def create_png_from_dot(dot_content: str, output_filename: str):
    """
    Genera un archivo .png a partir de un contenido DOT.

    :param dot_content: La estructura en formato DOT generada por print_vehicle().
    :param output_filename: Nombre del archivo de salida (sin extensión).
    """
    # Crea una fuente Graphviz a partir del contenido DOT
    src = Source(dot_content)
    # Renderiza el archivo como PNG
    src.format = 'png'
    src.render(output_filename, cleanup=True)  # Genera el archivo .png y elimina archivos intermedios
    print(f"Archivo {output_filename}.png creado exitosamente.")
