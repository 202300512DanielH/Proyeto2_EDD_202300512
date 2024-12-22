class Vehiculo:
    def __init__(self, placa, marca, modelo, precio_por_segundo):
        """
        Constructor para la clase Vehiculo.

        :param placa: Placa única del vehículo (cadena).
        :param marca: Marca del vehículo (cadena).
        :param modelo: Modelo del vehículo (cadena).
        :param precio_por_segundo: Precio por segundo de uso (float o int).
        """
        if not placa:
            raise ValueError("La placa no puede estar vacía.")

        if not isinstance(precio_por_segundo, (int, float)) or precio_por_segundo <= 0:
            raise ValueError("El precio por segundo debe ser un número positivo.")

        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.precio_por_segundo = precio_por_segundo

    def __str__(self):
        """
        Representación en cadena del objeto Vehiculo.
        """
        return (f"Placa: {self.placa}\n"
                f"Marca: {self.marca}\n"
                f"Modelo: {self.modelo}\n"
                f"Precio por segundo: {self.precio_por_segundo:.2f}")