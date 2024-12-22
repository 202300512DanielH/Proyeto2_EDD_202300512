class Ruta:
    def __init__(self, origen, destino, tiempo):
        """
        Constructor para la clase Ruta.

        :param origen: Origen de la ruta (cadena).
        :param destino: Destino de la ruta (cadena).
        :param tiempo: Tiempo de la ruta en minutos (int o float).
        """
        if not origen or not destino:
            raise ValueError("Origen y destino no pueden estar vacíos.")

        if not isinstance(tiempo, (int, float)) or tiempo <= 0:
            raise ValueError("El tiempo de la ruta debe ser un número positivo.")

        self.origen = origen
        self.destino = destino
        self.tiempo = tiempo

    def __str__(self):
        """
        Representación en cadena del objeto Ruta.
        """
        return f"Ruta: {self.origen} -> {self.destino}, Tiempo: {self.tiempo} minutos"
