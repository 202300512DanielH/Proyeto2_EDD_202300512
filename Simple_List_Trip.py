import graphviz

from Path import camino
from Simple_List_Path import SimpleListPath
from Trip import Viaje


class TripNode:
    def __init__(self, trip):
        self.trip = trip
        self.next = None


class SimpleListTrip:
    def __init__(self):
        self.head = None
        self.id_counter = 1  # Para generar IDs únicos

    def insert(self, lugar_origen, lugar_destino, fecha_hora, cliente, vehiculo, caminos):
        # Crear un nuevo ID para el viaje
        trip_id = self.id_counter
        self.id_counter += 1

        # Crear una lista simple de caminos
        caminos_list = SimpleListPath()
        for camino in caminos:
            caminos_list.insert(camino)

        # Crear el objeto Viaje
        new_trip = Viaje(trip_id, lugar_origen, lugar_destino, fecha_hora, cliente, vehiculo, caminos_list)

        # Insertar en la lista
        new_node = TripNode(new_trip)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

    def display_trips(self):
        current = self.head
        while current is not None:
            trip = current.trip
            print(f"ID: {trip.id}")
            print(f"Lugar Origen: {trip.lugar_origen}")
            print(f"Lugar Destino: {trip.lugar_destino}")
            print(f"Fecha y Hora: {trip.fecha_hora}")
            print(f"Cliente: {trip.cliente}")
            print(f"Vehículo: {trip.vehiculo}")
            print("Camino:")
            camino_current = trip.camino.head
            while camino_current is not None:
                path = camino_current.path
                print(f"  {path.origen} -> {path.destino} ({path.duracion})")
                camino_current = camino_current.next
            print("-" * 20)
            current = current.next

    def to_dot(self):
        dot_str = "digraph G {\n"
        dot_str += "rankdir=LR;\n"
        current = self.head
        node_id = 0
        while current is not None:
            trip = current.trip
            trip_label = f"ID: {trip.id}\\n{trip.lugar_origen} -> {trip.lugar_destino}\\nCliente: {trip.cliente}\\nVehículo: {trip.vehiculo}"
            dot_str += f'node{node_id} [label="{trip_label}", shape=box];\n'
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

    def get_longest_trips(self, n=5):
        sorted_trips = SimpleListTrip()
        temp_trips = SimpleListTrip()

        # Copiar todos los viajes a una lista temporal para evitar modificar la original
        current = self.head
        while current is not None:
            trip = current.trip
            temp_trips.insert(trip.lugar_origen, trip.lugar_destino, trip.fecha_hora, trip.cliente, trip.vehiculo,
                              trip.camino)
            current = current.next

        # Encontrar los viajes más largos iterativamente
        for _ in range(n):
            longest_trip = None
            prev_node = None
            prev_longest_node = None

            temp_current = temp_trips.head
            while temp_current is not None:
                trip = temp_current.trip
                if longest_trip is None or trip.camino.get_length() > longest_trip.camino.get_length():
                    longest_trip = trip
                    prev_longest_node = prev_node
                prev_node = temp_current
                temp_current = temp_current.next

            # Insertar el viaje más largo encontrado en la lista ordenada
            if longest_trip:
                sorted_trips.insert(
                    longest_trip.lugar_origen,
                    longest_trip.lugar_destino,
                    longest_trip.fecha_hora,
                    longest_trip.cliente,
                    longest_trip.vehiculo,
                    longest_trip.camino
                )

                # Remover el nodo del viaje más largo de la lista temporal
                if prev_longest_node is None:  # El nodo más largo es la cabeza
                    temp_trips.head = temp_trips.head.next
                else:
                    prev_longest_node.next = prev_longest_node.next.next

        return sorted_trips




