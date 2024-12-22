class Client:
    def __init__(self, dpi, nombres, apellidos, genero, telefono, direccion):
        if not isinstance(dpi, str) or len(dpi) != 13 or not dpi.isdigit():
            raise ValueError("El DPI debe ser una cadena de 13 dígitos.")

        self.dpi = dpi
        self.nombres = nombres
        self.apellidos = apellidos
        self.genero = genero
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return (f"DPI: {self.dpi}\n"
                f"Nombres: {self.nombres}\n"
                f"Apellidos: {self.apellidos}\n"
                f"Género: {self.genero}\n"
                f"Teléfono: {self.telefono}\n"
                f"Dirección: {self.direccion}")