import os
from PIL  import Image, ImageTk
import customtkinter as ctk
from tkinter import messagebox
from Client import Client
from DoLinkedCirList import DoublyCircularLinkedList


class WelcomeWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Llega Rapidito")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.setup_ui()

    def setup_ui(self):
        self.welcome_label = ctk.CTkLabel(
            self, text="¡Bienvenido a Llega Rapidito!", font=ctk.CTkFont(size=32, weight="bold")
        )
        self.welcome_label.pack(pady=50)

        self.sub_label = ctk.CTkLabel(
            self,
            text="Tu herramienta todo-en-uno para gestionar clientes, vehículos, viajes, rutas y reportes.",
            font=ctk.CTkFont(size=16),
            wraplength=600,
        )
        self.sub_label.pack(pady=20)

        self.enter_button = ctk.CTkButton(
            self, text="Entrar", command=self.open_main_menu, font=ctk.CTkFont(size=20), width=200
        )
        self.enter_button.pack(pady=50)

    def open_main_menu(self):
        self.destroy()
        main_menu = MainMenu()
        main_menu.mainloop()


class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Llega Rapidito - Menú Principal")
        self.geometry("1000x700")
        self.client_list = DoublyCircularLinkedList()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.content_area = ctk.CTkFrame(self, corner_radius=0)
        self.content_area.pack(side="right", fill="both", expand=True)

        self.buttons = {
            "Clientes": self.show_clients,
            "Vehículos": self.show_vehicles,
            "Viajes": self.show_trips,
            "Rutas": self.show_routes,
            "Reportes": self.show_reports,
        }

        for text, command in self.buttons.items():
            button = ctk.CTkButton(self.sidebar, text=text, command=command)
            button.pack(pady=10, padx=10, fill="x")

        self.active_frame = None
        self.show_clients()

    def clear_content_area(self):
        if self.active_frame:
            self.active_frame.destroy()
        self.active_frame = None

    def show_clients(self):
        self.clear_content_area()
        self.active_frame = ClientsModule(self.content_area, self.client_list, self)
        self.active_frame.pack(fill="both", expand=True)

    def show_vehicles(self):
        self.clear_content_area()
        self.active_frame = GenericModule(self.content_area, "Gestión de Vehículos")
        self.active_frame.pack(fill="both", expand=True)

    def show_trips(self):
        self.clear_content_area()
        self.active_frame = GenericModule(self.content_area, "Gestión de Viajes")
        self.active_frame.pack(fill="both", expand=True)

    def show_routes(self):
        self.clear_content_area()
        self.active_frame = GenericModule(self.content_area, "Gestión de Rutas")
        self.active_frame.pack(fill="both", expand=True)

    def show_reports(self):
        self.clear_content_area()
        self.active_frame = GenericModule(self.content_area, "Generación de Reportes")
        self.active_frame.pack(fill="both", expand=True)


class ClientsModule(ctk.CTkFrame):
    def __init__(self, parent, client_list, main_menu, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.client_list = client_list
        self.main_menu = main_menu
        self.active_frame = None  # Para gestionar vistas activas
        self.setup_ui()

    def setup_ui(self):
        # Título del módulo
        self.title_label = ctk.CTkLabel(self, text="Gestión de Clientes", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)

        # Botones de navegación interna
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(fill="x", padx=10, pady=10)

        self.add_button = ctk.CTkButton(nav_frame, text="Agregar Cliente", command=self.show_add_client)
        self.add_button.pack(side="left", padx=10)

        self.view_button = ctk.CTkButton(nav_frame, text="Mostrar Clientes", command=self.show_view_clients)
        self.view_button.pack(side="left", padx=10)

        self.delete_button = ctk.CTkButton(nav_frame, text="Eliminar Cliente", command=self.show_delete_client)
        self.delete_button.pack(side="left", padx=10)

        self.graph_button = ctk.CTkButton(nav_frame, text="Visualizar Estructura", command=self.show_graph_structure)
        self.graph_button.pack(side="left", padx=10)

        self.mass_upload_button = ctk.CTkButton(nav_frame, text="Carga Masiva", command=self.show_mass_upload)
        self.mass_upload_button.pack(side="left", padx=10)

        # Área de contenido para las vistas
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Mostrar la vista inicial
        self.show_add_client()

    def clear_content_area(self):
        if self.active_frame:
            self.active_frame.destroy()
            self.active_frame = None

    def show_add_client(self):
        self.clear_content_area()
        self.active_frame = AddClientFrame(self.content_frame, self.client_list)
        self.active_frame.pack(fill="both", expand=True)

    def show_view_clients(self):
        self.clear_content_area()
        self.active_frame = ViewClientsFrame(self.content_frame, self.client_list)
        self.active_frame.pack(fill="both", expand=True)

    def show_delete_client(self):
        self.clear_content_area()
        self.active_frame = DeleteClientFrame(self.content_frame, self.client_list)
        self.active_frame.pack(fill="both", expand=True)

    def show_graph_structure(self):
        self.clear_content_area()
        self.active_frame = GraphStructureFrame(self.content_frame, self.client_list)
        self.active_frame.pack(fill="both", expand=True)

    def show_mass_upload(self):
        self.clear_content_area()
        self.active_frame = MassUploadFrame(self.content_frame, self.client_list)
        self.active_frame.pack(fill="both", expand=True)



class AddClientFrame(ctk.CTkFrame):
    def __init__(self, parent, client_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.client_list = client_list
        self.title_label = ctk.CTkLabel(self, text="Agregar Cliente", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        self.dpi_entry = self.create_form_entry("DPI:")
        self.name_entry = self.create_form_entry("Nombre:")
        self.last_name_entry = self.create_form_entry("Apellido:")
        self.gender_combobox = self.create_combobox("Género:", ["Masculino", "Femenino", "Prefiero no decirlo"])
        self.phone_entry = self.create_form_entry("Teléfono:")
        self.address_entry = self.create_form_entry("Dirección:")

        self.save_button = ctk.CTkButton(self, text="Guardar Cliente", command=self.save_client)
        self.save_button.pack(pady=20)

    def create_form_entry(self, label_text):
        label = ctk.CTkLabel(self, text=label_text, font=ctk.CTkFont(size=14))
        label.pack(pady=(10, 0))
        entry = ctk.CTkEntry(self)
        entry.pack(pady=(0, 10), padx=20, fill="x")
        return entry

    def create_combobox(self, label_text, options):
        label = ctk.CTkLabel(self, text=label_text, font=ctk.CTkFont(size=14))
        label.pack(pady=(10, 0))
        combobox = ctk.CTkComboBox(self, values=options)
        combobox.pack(pady=(0, 10), padx=20, fill="x")
        return combobox

    def save_client(self):
        dpi = self.dpi_entry.get()
        name = self.name_entry.get()
        last_name = self.last_name_entry.get()
        gender = self.gender_combobox.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()

        if dpi and name and last_name:
            client = Client(dpi, name, last_name, gender, phone, address)
            self.client_list.add(client)
            messagebox.showinfo("Éxito", f"Cliente agregado:\nDPI: {dpi}\nNombre: {name} {last_name}")
            self.clear_form()
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")

    def clear_form(self):
        self.dpi_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.last_name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.address_entry.delete(0, "end")
        self.gender_combobox.set("")

class ViewClientsFrame(ctk.CTkFrame):
    def __init__(self, parent, client_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.client_list = client_list
        self.setup_ui()

    def setup_ui(self):
        # Título
        self.title_label = ctk.CTkLabel(self, text="Lista de Clientes", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # Contenedor de la tabla
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Botón para actualizar la tabla
        self.refresh_button = ctk.CTkButton(self, text="Actualizar", command=self.display_clients)
        self.refresh_button.pack(pady=10)

        # Mostrar encabezados de la tabla
        self.display_table_headers()

        # Cargar datos
        self.display_clients()

    def display_table_headers(self):
        headers = ["DPI", "Nombre", "Apellido", "Género", "Teléfono", "Dirección"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.table_frame, text=header, font=ctk.CTkFont(size=14, weight="bold"))
            label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

    def display_clients(self):
        # Eliminar filas existentes para evitar duplicados
        for widget in self.table_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:  # Mantener encabezados
                widget.destroy()

        if self.client_list.is_empty():
            no_data_label = ctk.CTkLabel(
                self.table_frame,
                text="No hay clientes en la lista.",
                font=ctk.CTkFont(size=14, slant="italic"),
            )
            no_data_label.grid(row=1, column=0, columnspan=6, padx=5, pady=5)
        else:
            current = self.client_list.head
            row = 1
            while True:
                # Añadir los datos de cada cliente a la tabla
                client = current.client
                data = [
                    client.dpi,
                    client.nombres,
                    client.apellidos,
                    client.genero,
                    client.telefono,
                    client.direccion,
                ]
                for col, value in enumerate(data):
                    label = ctk.CTkLabel(self.table_frame, text=value, font=ctk.CTkFont(size=12))
                    label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

                current = current.next
                if current == self.client_list.head:
                    break
                row += 1


class DeleteClientFrame(ctk.CTkFrame):
    def __init__(self, parent, client_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.client_list = client_list
        self.selected_client = None  # Para almacenar el cliente seleccionado
        self.setup_ui()

    def setup_ui(self):
        # Título
        self.title_label = ctk.CTkLabel(self, text="Eliminar Cliente", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # Selección de DPI
        self.dpi_label = ctk.CTkLabel(self, text="Seleccione el DPI del cliente:", font=ctk.CTkFont(size=14))
        self.dpi_label.pack(pady=(10, 0))

        self.dpi_combobox = ctk.CTkComboBox(self, command=self.load_client_info)
        self.dpi_combobox.pack(pady=(0, 10), padx=20, fill="x")

        # Información del cliente seleccionado
        self.info_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12), justify="left")
        self.info_label.pack(pady=(10, 20))

        # Botón para eliminar
        self.delete_button = ctk.CTkButton(self, text="Eliminar Cliente", command=self.delete_client, state="disabled")
        self.delete_button.pack(pady=20)

        # Cargar los DPI disponibles
        self.load_dpi_list()

    def load_dpi_list(self):
        """Carga todos los DPI disponibles en la lista desplegable."""
        if self.client_list.is_empty():
            self.dpi_combobox.configure(values=[], state="disabled")
            self.info_label.configure(text="No hay clientes disponibles para eliminar.")
        else:
            current = self.client_list.head
            dpi_list = []
            while True:
                dpi_list.append(current.client.dpi)
                current = current.next
                if current == self.client_list.head:
                    break
            self.dpi_combobox.configure(values=dpi_list, state="normal")

    def load_client_info(self, selected_dpi):
        """Carga y muestra la información del cliente seleccionado."""
        current = self.client_list.head
        while True:
            if current.client.dpi == selected_dpi:
                self.selected_client = current.client
                self.info_label.configure(
                    text=f"DPI: {current.client.dpi}\n"
                         f"Nombre: {current.client.nombres} {current.client.apellidos}\n"
                         f"Género: {current.client.genero}\n"
                         f"Teléfono: {current.client.telefono}\n"
                         f"Dirección: {current.client.direccion}"
                )
                self.delete_button.configure(state="normal")
                return
            current = current.next
            if current == self.client_list.head:
                break
        # Si no se encuentra el cliente
        self.info_label.configure(text="Cliente no encontrado.")
        self.delete_button.configure(state="disabled")

    def delete_client(self):
        """Elimina al cliente seleccionado."""
        if self.selected_client:
            if self.client_list.remove(self.selected_client.dpi):
                messagebox.showinfo("Éxito", f"Cliente con DPI {self.selected_client.dpi} eliminado correctamente.")
                self.selected_client = None
                self.info_label.configure(text="")
                self.delete_button.configure(state="disabled")
                self.load_dpi_list()  # Actualiza la lista de DPI
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente.")



class GraphStructureFrame(ctk.CTkFrame):
    def __init__(self, parent, client_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.client_list = client_list
        self.image_label = None  # Para mostrar la imagen
        self.setup_ui()

    def setup_ui(self):
        # Título
        self.title_label = ctk.CTkLabel(self, text="Visualizar Estructura", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # Botón para generar visualización
        self.generate_button = ctk.CTkButton(self, text="Generar Visualización", command=self.generate_graph)
        self.generate_button.pack(pady=20)

        # Contenedor para la imagen
        self.image_label = ctk.CTkLabel(self, text="La imagen se mostrará aquí.", font=ctk.CTkFont(size=14))
        self.image_label.pack(fill="both", expand=True, padx=10, pady=10)

    def generate_graph(self):
        # Verificar si la lista está vacía
        if self.client_list.is_empty():
            messagebox.showinfo("Estructura", "No hay clientes en la lista para graficar.")
            return

        # Generar el archivo de gráfico
        filename = "client_structure"
        self.client_list.generate_graphviz(filename)

        # Verificar si el archivo de imagen existe
        image_path = f"{filename}.png"
        if os.path.exists(image_path):
            self.display_image(image_path)
            messagebox.showinfo("Éxito", f"Gráfico generado y visualizado como '{filename}.png'.")
        else:
            messagebox.showerror("Error", f"No se pudo encontrar '{filename}.png'.")

    def display_image(self, image_path):
        """Carga y muestra la imagen generada."""
        try:
            # Cargar la imagen
            image = Image.open(image_path)
            image = image.resize((800, 600), Image.Resampling.LANCZOS)  # Ajustar tamaño de la imagen
            photo = ImageTk.PhotoImage(image)

            # Actualizar la etiqueta con la imagen
            self.image_label.configure(image=photo, text="")  # Eliminar texto de marcador
            self.image_label.image = photo  # Mantener referencia para evitar garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

import tkinter as tk
from tkinter import filedialog

class MassUploadFrame(ctk.CTkFrame):
    def __init__(self, parent, client_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.client_list = client_list
        self.setup_ui()

    def setup_ui(self):
        # Título
        self.title_label = ctk.CTkLabel(self, text="Carga Masiva de Clientes", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # Botón para seleccionar archivo
        self.upload_button = ctk.CTkButton(self, text="Seleccionar Archivo", command=self.select_file)
        self.upload_button.pack(pady=20)

        # Área para mostrar resultados
        self.result_textbox = ctk.CTkTextbox(self, height=200)
        self.result_textbox.pack(fill="both", expand=True, padx=10, pady=10)

    def select_file(self):
        """Abre un cuadro de diálogo para seleccionar el archivo."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
        )
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        """Carga y procesa el archivo seleccionado."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            added_count = 0
            for line in lines:
                # Parsear los datos
                data = line.strip().split(",")
                if len(data) == 6:  # Asegurar que todos los campos estén presentes
                    dpi, nombres, apellidos, genero, telefono, direccion = map(str.strip, data)
                    # Crear y agregar cliente
                    client = Client(dpi, nombres, apellidos, genero, telefono, direccion)
                    self.client_list.add(client)
                    added_count += 1
                else:
                    self.result_textbox.insert(
                        "end", f"Formato inválido en la línea: {line.strip()}\n"
                    )

            self.result_textbox.insert(
                "end", f"{added_count} clientes agregados correctamente.\n"
            )
        except Exception as e:
            self.result_textbox.insert("end", f"Error al procesar el archivo: {e}\n")



class GenericModule(ctk.CTkFrame):
    def __init__(self, parent, module_name, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.title_label = ctk.CTkLabel(self, text=module_name, font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)

        self.info_label = ctk.CTkLabel(self, text=f"Este es el módulo de {module_name}.", font=ctk.CTkFont(size=16))
        self.info_label.pack(pady=20)


if __name__ == "__main__":
    app = WelcomeWindow()
    app.mainloop()
