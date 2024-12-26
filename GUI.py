import os
from PIL  import Image, ImageTk
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from graphviz import Source
#importaciones para clientes
from Client import Client
from DoLinkedCirList import DoublyCircularLinkedList
from Path import camino
#importaciones para rutas
from Route import Ruta
from Adjacency_List import AdjacencyList
from Simple_List_Trip import SimpleListTrip

#importacoin para vehiculos
from Vehicle import Vehiculo
from Btree import BTree, create_png_from_dot


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
        self.geometry("1200x800")
        self.client_list = DoublyCircularLinkedList()
        self.routes_list = AdjacencyList()
        self.vehicles_list = BTree(5)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.content_area = ctk.CTkFrame(self, corner_radius=0)
        self.content_area.pack(side="right", fill="both", expand=True)

        self.buttons = {
            "Rutas": self.show_routes,
            "Clientes": self.show_clients,
            "Vehículos": self.show_vehicles,
            "Viajes": self.show_trips,
            "Reportes": self.show_reports,
        }

        for text, command in self.buttons.items():
            button = ctk.CTkButton(self.sidebar, text=text, command=command)
            button.pack(pady=10, padx=10, fill="x")

        self.active_frame = None
        self.show_routes()

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
        self.active_frame = VehiclesModule(self.content_area, self.vehicles_list)
        self.active_frame.pack(fill="both", expand=True)

    def show_trips(self):
        self.clear_content_area()
        self.active_frame = TripModule(
            self.content_area, self.client_list, self.vehicles_list, self.routes_list, SimpleListTrip()
        )
        self.active_frame.pack(fill="both", expand=True)
    def show_routes(self):
        self.clear_content_area()
        self.active_frame = RoutesModule(self.content_area, self.routes_list, self)
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

        self.modify_button = ctk.CTkButton(nav_frame, text="Modificar Cliente", command=self.show_modify_client)
        self.modify_button.pack(side="left", padx=10)

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

    def show_modify_client(self):
        self.clear_content_area()
        self.active_frame = ModifyClientFrame(self.content_frame, self.client_list)
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

class ModifyClientFrame(ctk.CTkFrame):
    def __init__(self, parent, client_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.client_list = client_list
        self.selected_client = None  # Almacena el cliente seleccionado para modificar
        self.setup_ui()

    def setup_ui(self):
        # Título
        self.title_label = ctk.CTkLabel(self, text="Modificar Cliente", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # Selección de DPI
        self.dpi_label = ctk.CTkLabel(self, text="Seleccione el DPI del cliente:", font=ctk.CTkFont(size=14))
        self.dpi_label.pack(pady=(10, 0))

        self.dpi_combobox = ctk.CTkComboBox(self, command=self.load_client_info)
        self.dpi_combobox.pack(pady=(0, 10), padx=20, fill="x")

        # Campos de formulario para modificar los datos
        self.name_entry = self.create_form_entry("Nombre:")
        self.last_name_entry = self.create_form_entry("Apellido:")
        self.gender_combobox = self.create_combobox("Género:", ["Masculino", "Femenino", "Prefiero no decirlo"])
        self.phone_entry = self.create_form_entry("Teléfono:")
        self.address_entry = self.create_form_entry("Dirección:")

        # Botón para guardar cambios
        self.save_button = ctk.CTkButton(self, text="Guardar Cambios", command=self.modify_client, state="disabled")
        self.save_button.pack(pady=20)

        # Cargar los DPI disponibles
        self.load_dpi_list()

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

    def load_dpi_list(self):
        """Carga todos los DPI disponibles en la lista desplegable."""
        if self.client_list.is_empty():
            self.dpi_combobox.configure(values=[], state="disabled")
            self.clear_form()
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
        """Carga y muestra los datos del cliente seleccionado para su modificación."""
        current = self.client_list.head
        while True:
            if current.client.dpi == selected_dpi:
                self.selected_client = current.client
                self.name_entry.delete(0, "end")
                self.name_entry.insert(0, current.client.nombres)
                self.last_name_entry.delete(0, "end")
                self.last_name_entry.insert(0, current.client.apellidos)
                self.gender_combobox.set(current.client.genero)
                self.phone_entry.delete(0, "end")
                self.phone_entry.insert(0, current.client.telefono)
                self.address_entry.delete(0, "end")
                self.address_entry.insert(0, current.client.direccion)
                self.save_button.configure(state="normal")
                return
            current = current.next
            if current == self.client_list.head:
                break

    def modify_client(self):
        """Guarda los cambios en los datos del cliente."""
        if self.selected_client:
            self.selected_client.nombres = self.name_entry.get()
            self.selected_client.apellidos = self.last_name_entry.get()
            self.selected_client.genero = self.gender_combobox.get()
            self.selected_client.telefono = self.phone_entry.get()
            self.selected_client.direccion = self.address_entry.get()

            messagebox.showinfo("Éxito", f"Cliente con DPI {self.selected_client.dpi} modificado correctamente.")
            self.clear_form()
            self.save_button.configure(state="disabled")
            self.load_dpi_list()
        else:
            messagebox.showerror("Error", "No se pudo modificar el cliente.")

    def clear_form(self):
        """Limpia los campos del formulario."""
        self.name_entry.delete(0, "end")
        self.last_name_entry.delete(0, "end")
        self.gender_combobox.set("")
        self.phone_entry.delete(0, "end")
        self.address_entry.delete(0, "end")


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

class RoutesModule(ctk.CTkFrame):
    def __init__(self, parent, adjacency_list, main_menu, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.adjacency_list = adjacency_list
        self.main_menu = main_menu
        self.active_frame = None  # Para gestionar vistas activas
        self.setup_ui()

    def setup_ui(self):
        # Título del módulo
        self.title_label = ctk.CTkLabel(self, text="Gestión de Rutas", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)

        # Botones de navegación interna
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(fill="x", padx=10, pady=10)

        self.add_button = ctk.CTkButton(nav_frame, text="Agregar Ruta", command=self.show_add_route)
        self.add_button.pack(side="left", padx=10)

        self.modify_button = ctk.CTkButton(nav_frame, text="Modificar Ruta", command=self.show_modify_route)
        self.modify_button.pack(side="left", padx=10)

        self.delete_button = ctk.CTkButton(nav_frame, text="Eliminar Ruta", command=self.show_delete_route)
        self.delete_button.pack(side="left", padx=10)

        self.view_button = ctk.CTkButton(nav_frame, text="Mostrar Rutas", command=self.show_view_routes)
        self.view_button.pack(side="left", padx=10)

        self.graph_button = ctk.CTkButton(nav_frame, text="Visualizar Estructura", command=self.show_graph_structure)
        self.graph_button.pack(side="left", padx=10)

        self.graph_button = ctk.CTkButton(nav_frame, text="Carga Masiva", command=self.show_mass_upload)
        self.graph_button.pack(side="left", padx=10)


        # Área de contenido para las vistas
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Mostrar la vista inicial
        self.show_add_route()

    def clear_content_area(self):
        if self.active_frame:
            self.active_frame.destroy()
            self.active_frame = None

    def show_add_route(self):
        self.clear_content_area()
        self.active_frame = AddRouteFrame(self.content_frame, self.adjacency_list)
        self.active_frame.pack(fill="both", expand=True)

    def show_modify_route(self):
        self.clear_content_area()
        self.active_frame = ModifyRouteFrame(self.content_frame, self.adjacency_list)
        self.active_frame.pack(fill="both", expand=True)

    def show_delete_route(self):
        self.clear_content_area()
        self.active_frame = DeleteRouteFrame(self.content_frame, self.adjacency_list)
        self.active_frame.pack(fill="both", expand=True)

    def show_view_routes(self):
        self.clear_content_area()
        self.active_frame = ViewRoutesFrame(self.content_frame, self.adjacency_list)
        self.active_frame.pack(fill="both", expand=True)

    def show_graph_structure(self):
        self.clear_content_area()
        self.active_frame = GraphRoutesFrame(self.content_frame, self.adjacency_list)
        self.active_frame.pack(fill="both", expand=True)

    def show_mass_upload(self):
        self.clear_content_area()
        self.active_frame = MassiveRouteFrame(self.content_frame, self.adjacency_list)
        self.active_frame.pack(fill="both", expand=True)


class AddRouteFrame(ctk.CTkFrame):
    def __init__(self, parent, adjacency_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.adjacency_list = adjacency_list
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Agregar Ruta", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        self.origen_entry = self.create_form_entry("Origen:")
        self.destino_entry = self.create_form_entry("Destino:")
        self.tiempo_entry = self.create_form_entry("Tiempo (min):")

        self.add_button = ctk.CTkButton(self, text="Agregar Ruta", command=self.add_route)
        self.add_button.pack(pady=20)

    def create_form_entry(self, label_text):
        label = ctk.CTkLabel(self, text=label_text, font=ctk.CTkFont(size=14))
        label.pack(pady=(10, 0))
        entry = ctk.CTkEntry(self)
        entry.pack(pady=(0, 10), padx=20, fill="x")
        return entry

    def add_route(self):
        origen = self.origen_entry.get()
        destino = self.destino_entry.get()
        try:
            tiempo = float(self.tiempo_entry.get())
            ruta = Ruta(origen, destino, tiempo)
            self.adjacency_list.insert(origen, ruta)
            messagebox.showinfo("Éxito", f"Ruta agregada:\n{ruta}")
            self.clear_form()
        except ValueError as e:
            messagebox.showerror("Error", f"Error al agregar la ruta: {e}")

    def clear_form(self):
        self.origen_entry.delete(0, "end")
        self.destino_entry.delete(0, "end")
        self.tiempo_entry.delete(0, "end")


class ModifyRouteFrame(ctk.CTkFrame):
    def __init__(self, parent, adjacency_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.adjacency_list = adjacency_list
        self.selected_origen = None
        self.selected_destino = None
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Modificar Ruta", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # Selección de Origen
        self.origen_label = ctk.CTkLabel(self, text="Seleccione el Origen:", font=ctk.CTkFont(size=14))
        self.origen_label.pack(pady=(10, 0))
        self.origen_combobox = ctk.CTkComboBox(self, command=self.load_destinations)
        self.origen_combobox.pack(pady=(0, 10), padx=20, fill="x")

        # Selección de Destino
        self.destino_label = ctk.CTkLabel(self, text="Seleccione el Destino:", font=ctk.CTkFont(size=14))
        self.destino_label.pack(pady=(10, 0))
        self.destino_combobox = ctk.CTkComboBox(self)
        self.destino_combobox.pack(pady=(0, 10), padx=20, fill="x")

        # Campos de modificación
        self.nuevo_destino_entry = self.create_form_entry("Nuevo Destino:")
        self.nuevo_tiempo_entry = self.create_form_entry("Nuevo Tiempo (min):")

        self.modify_button = ctk.CTkButton(self, text="Modificar Ruta", command=self.modify_route)
        self.modify_button.pack(pady=20)

        self.load_origins()

    def create_form_entry(self, label_text):
        label = ctk.CTkLabel(self, text=label_text, font=ctk.CTkFont(size=14))
        label.pack(pady=(10, 0))
        entry = ctk.CTkEntry(self)
        entry.pack(pady=(0, 10), padx=20, fill="x")
        return entry

    def load_origins(self):
        """Carga los nodos de origen en el comboBox."""
        origins = []
        temp = self.adjacency_list.head
        while temp:
            origins.append(temp.origen)
            temp = temp.next
        self.origen_combobox.configure(values=origins)

    def load_destinations(self, selected_origen):
        """Carga los destinos disponibles para el origen seleccionado."""
        self.selected_origen = selected_origen
        destinations = []
        temp = self.adjacency_list.head
        while temp:
            if temp.origen == selected_origen:
                adj_temp = temp.adjacency_list
                while adj_temp:
                    destinations.append(adj_temp.ruta.destino)
                    adj_temp = adj_temp.next
                break
            temp = temp.next
        self.destino_combobox.configure(values=destinations)

    def modify_route(self):
        """Modifica la ruta seleccionada."""
        origen = self.selected_origen
        destino = self.destino_combobox.get()
        nuevo_destino = self.nuevo_destino_entry.get()
        try:
            nuevo_tiempo = float(self.nuevo_tiempo_entry.get())
            if nuevo_destino:
                # Cambiar destino si es necesario
                self.adjacency_list.delete(origen, destino)
                ruta_modificada = Ruta(origen, nuevo_destino, nuevo_tiempo)
                self.adjacency_list.insert(origen, ruta_modificada)
            else:
                # Solo modificar el tiempo
                self.adjacency_list.modify(origen, destino, nuevo_tiempo)
            messagebox.showinfo("Éxito", f"Ruta modificada: {origen} -> {nuevo_destino or destino}, Nuevo tiempo: {nuevo_tiempo} minutos")
            self.clear_form()
        except ValueError as e:
            messagebox.showerror("Error", f"Error al modificar la ruta: {e}")

    def clear_form(self):
        """Limpia los campos del formulario."""
        self.origen_combobox.set("")
        self.destino_combobox.set("")
        self.nuevo_destino_entry.delete(0, "end")
        self.nuevo_tiempo_entry.delete(0, "end")



class DeleteRouteFrame(ctk.CTkFrame):
    def __init__(self, parent, adjacency_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.adjacency_list = adjacency_list
        self.selected_origen = None
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Eliminar Ruta", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # Selección de Origen
        self.origen_label = ctk.CTkLabel(self, text="Seleccione el Origen:", font=ctk.CTkFont(size=14))
        self.origen_label.pack(pady=(10, 0))
        self.origen_combobox = ctk.CTkComboBox(self, command=self.load_destinations)
        self.origen_combobox.pack(pady=(0, 10), padx=20, fill="x")

        # Selección de Destino
        self.destino_label = ctk.CTkLabel(self, text="Seleccione el Destino:", font=ctk.CTkFont(size=14))
        self.destino_label.pack(pady=(10, 0))
        self.destino_combobox = ctk.CTkComboBox(self)
        self.destino_combobox.pack(pady=(0, 10), padx=20, fill="x")

        self.delete_button = ctk.CTkButton(self, text="Eliminar Ruta", command=self.delete_route)
        self.delete_button.pack(pady=20)

        self.load_origins()

    def load_origins(self):
        """Carga los nodos de origen en el comboBox."""
        origins = []
        temp = self.adjacency_list.head
        while temp:
            origins.append(temp.origen)
            temp = temp.next
        self.origen_combobox.configure(values=origins)

    def load_destinations(self, selected_origen):
        """Carga los destinos disponibles para el origen seleccionado."""
        self.selected_origen = selected_origen
        destinations = []
        temp = self.adjacency_list.head
        while temp:
            if temp.origen == selected_origen:
                adj_temp = temp.adjacency_list
                while adj_temp:
                    destinations.append(adj_temp.ruta.destino)
                    adj_temp = adj_temp.next
                break
            temp = temp.next
        self.destino_combobox.configure(values=destinations)

    def delete_route(self):
        """Elimina la ruta seleccionada."""
        origen = self.selected_origen
        destino = self.destino_combobox.get()
        try:
            self.adjacency_list.delete(origen, destino)
            messagebox.showinfo("Éxito", f"Ruta eliminada: {origen} -> {destino}")
            self.clear_form()
        except ValueError as e:
            messagebox.showerror("Error", f"Error al eliminar la ruta: {e}")

    def clear_form(self):
        """Limpia los campos del formulario."""
        self.origen_combobox.set("")
        self.destino_combobox.set("")



class ViewRoutesFrame(ctk.CTkFrame):
    def __init__(self, parent, adjacency_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.adjacency_list = adjacency_list
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Lista de Rutas", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # Contenedor con scrollbar
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=400, height=300)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Botón para actualizar la tabla
        self.refresh_button = ctk.CTkButton(self, text="Actualizar", command=self.display_routes)
        self.refresh_button.pack(pady=10)

        # Mostrar encabezados de la tabla
        self.display_table_headers()

        # Cargar datos
        self.display_routes()

    def display_table_headers(self):
        headers = ["Origen", "Destino", "Tiempo (min)"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.scrollable_frame, text=header, font=ctk.CTkFont(size=14, weight="bold"))
            label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

    def display_routes(self):
        # Eliminar filas existentes para evitar duplicados
        for widget in self.scrollable_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:  # Mantener encabezados
                widget.destroy()

        temp = self.adjacency_list.head
        if not temp:
            no_data_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No hay rutas disponibles.",
                font=ctk.CTkFont(size=14, slant="italic"),
            )
            no_data_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        else:
            row = 1
            while temp:
                origen = temp.origen
                adj_temp = temp.adjacency_list
                while adj_temp:
                    destino = adj_temp.ruta.destino
                    tiempo = adj_temp.ruta.tiempo
                    data = [origen, destino, f"{tiempo} min"]
                    for col, value in enumerate(data):
                        label = ctk.CTkLabel(self.scrollable_frame, text=value, font=ctk.CTkFont(size=12))
                        label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                    adj_temp = adj_temp.next
                    row += 1
                temp = temp.next



class GraphRoutesFrame(ctk.CTkFrame):
    def __init__(self, parent, adjacency_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.adjacency_list = adjacency_list
        self.image_label = None
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Visualizar Estructura", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        self.generate_button = ctk.CTkButton(self, text="Generar Visualización", command=self.generate_graph)
        self.generate_button.pack(pady=20)

        self.image_label = ctk.CTkLabel(self, text="La imagen se mostrará aquí.", font=ctk.CTkFont(size=14))
        self.image_label.pack(fill="both", expand=True, padx=10, pady=10)

    def generate_graph(self):
        filename = "adjacency_list_graph"
        self.adjacency_list.generate_graphviz(filename)

        try:
            from PIL import Image, ImageTk

            image = Image.open(f"{filename}.png")
            image = image.resize((600, 400), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

class MassiveRouteFrame(ctk.CTkFrame):
    def __init__(self, parent, adjacency_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.adjacency_list = adjacency_list
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Carga Masiva de Rutas", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # Botón para seleccionar archivo
        self.upload_button = ctk.CTkButton(self, text="Seleccionar Archivo", command=self.select_file)
        self.upload_button.pack(pady=20)

        # Área para mostrar resultados
        self.result_textbox = ctk.CTkTextbox(self, height=200)
        self.result_textbox.pack(fill="both", expand=True, padx=10, pady=10)

    def select_file(self):
        """Abre un cuadro de diálogo para seleccionar el archivo."""
        from tkinter import filedialog

        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=(
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*"),
            ),
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
                data = line.strip().split("/")
                if len(data) == 3 and data[2].endswith('%'):
                    origen, destino, tiempo = map(str.strip, data)
                    tiempo = tiempo.rstrip('%')
                    try:
                        tiempo = float(tiempo)
                        if tiempo <= 0:
                            raise ValueError("El tiempo debe ser un número positivo.")
                        # Crear y agregar ruta
                        ruta = Ruta(origen, destino, tiempo)
                        self.adjacency_list.insert(origen, ruta)
                        added_count += 1
                    except ValueError as ve:
                        self.result_textbox.insert("end", f"Error en la línea: {line.strip()} - {ve}\n")
                else:
                    self.result_textbox.insert("end", f"Formato inválido en la línea: {line.strip()}\n")

            self.result_textbox.insert("end", f"{added_count} rutas agregadas correctamente.\n")
        except Exception as e:
            self.result_textbox.insert("end", f"Error al procesar el archivo: {e}\n")

class VehiclesModule(ctk.CTkFrame):
    def __init__(self, parent, btree, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.btree = btree
        self.active_frame = None
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Gestión de Vehículos", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)

        # Botones de navegación
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(fill="x", padx=10, pady=10)

        self.add_button = ctk.CTkButton(nav_frame, text="Agregar Vehículo", command=self.show_add_vehicle)
        self.add_button.pack(side="left", padx=10)

        self.modify_button = ctk.CTkButton(nav_frame, text="Modificar Vehículo", command=self.show_modify_vehicle)
        self.modify_button.pack(side="left", padx=10)

        self.delete_button = ctk.CTkButton(nav_frame, text="Eliminar Vehículo", command=self.show_delete_vehicle)
        self.delete_button.pack(side="left", padx=10)

        self.view_button = ctk.CTkButton(nav_frame, text="Mostrar Vehículos", command=self.show_view_vehicles)
        self.view_button.pack(side="left", padx=10)

        self.graph_button = ctk.CTkButton(nav_frame, text="Visualizar Estructura", command=self.show_graph_structure)
        self.graph_button.pack(side="left", padx=10)

        self.mass_upload_button = ctk.CTkButton(nav_frame, text="Carga Masiva", command=self.show_mass_upload)
        self.mass_upload_button.pack(side="left", padx=10)

        # Área de contenido
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Vista inicial
        self.show_add_vehicle()

    def clear_content_area(self):
        if self.active_frame:
            self.active_frame.destroy()
            self.active_frame = None

    def show_add_vehicle(self):
        self.clear_content_area()
        self.active_frame = AddVehicleFrame(self.content_frame, self.btree)
        self.active_frame.pack(fill="both", expand=True)

    def show_modify_vehicle(self):
        self.clear_content_area()
        self.active_frame = ModifyVehicleFrame(self.content_frame, self.btree)
        self.active_frame.pack(fill="both", expand=True)


    def show_delete_vehicle(self):
        self.clear_content_area()
        self.active_frame = DeleteVehicleFrame(self.content_frame, self.btree)
        self.active_frame.pack(fill="both", expand=True)

    def show_view_vehicles(self):
        self.clear_content_area()
        self.active_frame = ViewVehiclesFrame(self.content_frame, self.btree)
        self.active_frame.pack(fill="both", expand=True)

    def show_graph_structure(self):
        self.clear_content_area()
        self.active_frame = GraphStructureVehiclesFrame(self.content_frame, self.btree)
        self.active_frame.pack(fill="both", expand=True)

    def show_mass_upload(self):
        self.clear_content_area()
        self.active_frame = MassUploadVehiclesFrame(self.content_frame, self.btree)
        self.active_frame.pack(fill="both", expand=True)


class AddVehicleFrame(ctk.CTkFrame):
    def __init__(self, parent, btree, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.btree = btree
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Agregar Vehículo", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.pack(pady=10)

        self.placa_label = ctk.CTkLabel(self, text="Placa:")
        self.placa_label.pack(pady=5)
        self.placa_entry = ctk.CTkEntry(self)
        self.placa_entry.pack(pady=5)

        self.marca_label = ctk.CTkLabel(self, text="Marca:")
        self.marca_label.pack(pady=5)
        self.marca_entry = ctk.CTkEntry(self)
        self.marca_entry.pack(pady=5)

        self.modelo_label = ctk.CTkLabel(self, text="Modelo:")
        self.modelo_label.pack(pady=5)
        self.modelo_entry = ctk.CTkEntry(self)
        self.modelo_entry.pack(pady=5)

        self.precio_label = ctk.CTkLabel(self, text="Precio:")
        self.precio_label.pack(pady=5)
        self.precio_entry = ctk.CTkEntry(self)
        self.precio_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(self, text="Agregar", command=self.add_vehicle)
        self.add_button.pack(pady=20)

    def add_vehicle(self):
        placa = self.placa_entry.get()
        marca = self.marca_entry.get()
        modelo = self.modelo_entry.get()
        try:
            precio = float(self.precio_entry.get())
            vehicle = Vehiculo(placa, marca, modelo, precio)
            self.btree.insert_value(vehicle)
            messagebox.showinfo("Éxito", f"Vehículo {placa} agregado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Precio inválido. Por favor ingrese un número.")


class ModifyVehicleFrame(ctk.CTkFrame):
    def __init__(self, parent, btree, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.btree = btree
        self.selected_vehicle = None
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Modificar Vehículo", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.pack(pady=10)

        # Combobox para seleccionar placa
        self.select_label = ctk.CTkLabel(self, text="Seleccionar Vehículo (Placa):")
        self.select_label.pack(pady=5)

        self.placa_combobox = ctk.CTkComboBox(self, command=self.load_vehicle_data)
        self.placa_combobox.pack(pady=5)

        # Cargar las placas disponibles al inicializar la vista
        self.update_combobox()

        # Campos para mostrar y modificar datos
        self.marca_label = ctk.CTkLabel(self, text="Marca:")
        self.marca_label.pack(pady=5)
        self.marca_entry = ctk.CTkEntry(self)
        self.marca_entry.pack(pady=5)

        self.modelo_label = ctk.CTkLabel(self, text="Modelo:")
        self.modelo_label.pack(pady=5)
        self.modelo_entry = ctk.CTkEntry(self)
        self.modelo_entry.pack(pady=5)

        self.precio_label = ctk.CTkLabel(self, text="Precio:")
        self.precio_label.pack(pady=5)
        self.precio_entry = ctk.CTkEntry(self)
        self.precio_entry.pack(pady=5)

        self.modify_button = ctk.CTkButton(self, text="Modificar", command=self.modify_vehicle)
        self.modify_button.pack(pady=20)

    def update_combobox(self):
        """Actualiza las placas en el combobox."""
        plates = self.get_vehicle_plates()
        self.placa_combobox.configure(values=plates)

    def get_vehicle_plates(self):
        """Obtiene todas las placas de los vehículos en el árbol B."""
        plates = []

        def traverse(node):
            if node is not None:
                for key in node.keys:
                    plates.append(key.placa)
                for child in node.children:
                    traverse(child)

        traverse(self.btree.root)
        return plates

    def load_vehicle_data(self, event):
        """Carga los datos del vehículo seleccionado en los campos de entrada."""
        placa = self.placa_combobox.get()
        self.selected_vehicle = self.find_vehicle_by_plate(placa, self.btree.root)

        if self.selected_vehicle:
            self.marca_entry.delete(0, "end")
            self.marca_entry.insert(0, self.selected_vehicle.marca)

            self.modelo_entry.delete(0, "end")
            self.modelo_entry.insert(0, self.selected_vehicle.modelo)

            self.precio_entry.delete(0, "end")
            self.precio_entry.insert(0, str(self.selected_vehicle.precio))
        else:
            messagebox.showerror("Error", "Vehículo no encontrado.")

    def find_vehicle_by_plate(self, placa, node):
        """Busca un vehículo por su placa en el árbol B."""
        if node is None:
            return None

        for key in node.keys:
            if key.placa.strip() == placa.strip():
                return key

        for child in node.children:
            result = self.find_vehicle_by_plate(placa, child)
            if result:
                return result

        return None

    def modify_vehicle(self):
        """Modifica los datos del vehículo seleccionado en el árbol B."""
        if not self.selected_vehicle:
            messagebox.showerror("Error", "Seleccione un vehículo primero.")
            return

        try:
            new_marca = self.marca_entry.get()
            new_modelo = self.modelo_entry.get()
            new_precio = float(self.precio_entry.get())

            # Actualizar los datos del vehículo
            self.selected_vehicle.marca = new_marca
            self.selected_vehicle.modelo = new_modelo
            self.selected_vehicle.precio = new_precio

            messagebox.showinfo("Éxito", f"Vehículo {self.selected_vehicle.placa} modificado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Precio inválido. Por favor ingrese un número.")



class DeleteVehicleFrame(ctk.CTkFrame):
    def __init__(self, parent, btree, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.btree = btree
        self.selected_vehicle = None
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Eliminar Vehículo", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.pack(pady=10)

        # Combobox para seleccionar placa
        self.select_label = ctk.CTkLabel(self, text="Seleccionar Vehículo (Placa):")
        self.select_label.pack(pady=5)

        self.placa_combobox = ctk.CTkComboBox(self, command=self.load_vehicle_data)
        self.placa_combobox.pack(pady=5)

        # Cargar las placas disponibles al inicializar la vista
        self.update_combobox()

        # Información del vehículo seleccionado
        self.info_label = ctk.CTkLabel(self, text="Información del Vehículo:", font=ctk.CTkFont(size=16, weight="bold"))
        self.info_label.pack(pady=10)

        self.vehicle_info_text = ctk.CTkTextbox(self, height=5)
        self.vehicle_info_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.vehicle_info_text.configure(state="disabled")

        # Botón para eliminar
        self.delete_button = ctk.CTkButton(self, text="Eliminar", command=self.delete_vehicle, state="disabled")
        self.delete_button.pack(pady=20)

    def update_combobox(self):
        """Actualiza las placas en el combobox."""
        plates = self.get_vehicle_plates()
        self.placa_combobox.configure(values=plates)

    def get_vehicle_plates(self):
        """Obtiene todas las placas de los vehículos en el árbol B."""
        plates = []

        def traverse(node):
            if node is not None:
                for key in node.keys:
                    plates.append(key.placa)
                for child in node.children:
                    traverse(child)

        traverse(self.btree.root)
        return plates

    def load_vehicle_data(self, event):
        """Carga los datos del vehículo seleccionado en el área de texto."""
        placa = self.placa_combobox.get()
        self.selected_vehicle = self.find_vehicle_by_plate(placa, self.btree.root)

        if self.selected_vehicle:
            self.vehicle_info_text.configure(state="normal")
            self.vehicle_info_text.delete("1.0", "end")
            self.vehicle_info_text.insert("end", f"Placa: {self.selected_vehicle.placa}\n")
            self.vehicle_info_text.insert("end", f"Marca: {self.selected_vehicle.marca}\n")
            self.vehicle_info_text.insert("end", f"Modelo: {self.selected_vehicle.modelo}\n")
            self.vehicle_info_text.insert("end", f"Precio: {self.selected_vehicle.precio}\n")
            self.vehicle_info_text.configure(state="disabled")

            self.delete_button.configure(state="normal")
        else:
            messagebox.showerror("Error", "Vehículo no encontrado.")
            self.delete_button.configure(state="disabled")

    def find_vehicle_by_plate(self, placa, node):
        """Busca un vehículo por su placa en el árbol B."""
        if node is None:
            return None

        for key in node.keys:
            if key.placa.strip() == placa.strip():
                return key

        for child in node.children:
            result = self.find_vehicle_by_plate(placa, child)
            if result:
                return result

        return None

    def delete_vehicle(self):
        """Elimina el vehículo seleccionado del árbol B."""
        if not self.selected_vehicle:
            messagebox.showerror("Error", "Seleccione un vehículo primero.")
            return

        try:
            self.btree.delete(self.selected_vehicle)
            messagebox.showinfo("Éxito", f"Vehículo {self.selected_vehicle.placa} eliminado correctamente.")

            # Actualizar combobox y deshabilitar el botón
            self.update_combobox()
            self.vehicle_info_text.configure(state="normal")
            self.vehicle_info_text.delete("1.0", "end")
            self.vehicle_info_text.configure(state="disabled")
            self.delete_button.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el vehículo: {e}")



class ViewVehiclesFrame(ctk.CTkFrame):
    def __init__(self, parent, btree, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.btree = btree
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Lista de Vehículos", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # Contenedor de la tabla con scrollbar
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=600, height=400)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Botón para actualizar la tabla
        self.refresh_button = ctk.CTkButton(self, text="Actualizar", command=self.display_vehicles)
        self.refresh_button.pack(pady=10)

        # Mostrar encabezados de la tabla
        self.display_table_headers()

        # Cargar datos iniciales
        self.display_vehicles()

    def display_table_headers(self):
        headers = ["Placa", "Marca", "Modelo", "Precio"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.scrollable_frame, text=header, font=ctk.CTkFont(size=14, weight="bold"))
            label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

    def display_vehicles(self):
        # Eliminar filas existentes para evitar duplicados
        for widget in self.scrollable_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:  # Mantener encabezados
                widget.destroy()

        vehicles = self.get_all_vehicles()
        if not vehicles:
            no_data_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No hay vehículos disponibles.",
                font=ctk.CTkFont(size=14, slant="italic"),
            )
            no_data_label.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
        else:
            for row, vehicle in enumerate(vehicles, start=1):
                data = [
                    vehicle.placa,
                    vehicle.marca,
                    vehicle.modelo,
                    f"{vehicle.precio:.2f}",
                ]
                for col, value in enumerate(data):
                    label = ctk.CTkLabel(self.scrollable_frame, text=value, font=ctk.CTkFont(size=12))
                    label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def get_all_vehicles(self):
        """Obtiene todos los vehículos del árbol B."""
        vehicles = []

        def traverse(node):
            if node is not None:
                for key in node.keys:
                    vehicles.append(key)
                for child in node.children:
                    traverse(child)

        traverse(self.btree.root)
        return vehicles

class GraphStructureVehiclesFrame(ctk.CTkFrame):
    def __init__(self, parent, btree, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.btree = btree
        self.image_label = None
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Visualización de Estructura del Árbol B", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # Botón para generar visualización
        self.generate_button = ctk.CTkButton(self, text="Generar Visualización", command=self.generate_graph)
        self.generate_button.pack(pady=20)

        # Contenedor para la imagen
        self.image_label = ctk.CTkLabel(self, text="La imagen se mostrará aquí.", font=ctk.CTkFont(size=14))
        self.image_label.pack(fill="both", expand=True, padx=10, pady=10)

    def generate_graph(self):
        """Genera y muestra el gráfico de la estructura del árbol B."""
        try:
            # Generar el contenido del DOT y crear el archivo PNG
            tree_print = self.btree.print_vehicle()
            create_png_from_dot(tree_print, "btree_graph")

            # Ruta del archivo generado
            image_path = "btree_graph.png"

            # Mostrar la imagen en la interfaz
            self.display_image(image_path)

            messagebox.showinfo("Éxito", "Visualización generada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la visualización: {e}")

    def display_image(self, image_path):
        """Carga y muestra la imagen generada en la interfaz."""
        try:
            from PIL import Image, ImageTk

            # Cargar la imagen y redimensionarla si es necesario
            image = Image.open(image_path)
            image = image.resize((800, 600), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            # Actualizar la etiqueta con la imagen
            self.image_label.configure(image=photo, text="")  # Eliminar texto marcador
            self.image_label.image = photo  # Mantener referencia para evitar garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")



class MassUploadVehiclesFrame(ctk.CTkFrame):
    def __init__(self, parent, btree, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.btree = btree
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Carga Masiva de Vehículos", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # Botón para seleccionar archivo
        self.upload_button = ctk.CTkButton(self, text="Seleccionar Archivo", command=self.select_file)
        self.upload_button.pack(pady=20)

        # Área para mostrar resultados
        self.result_textbox = ctk.CTkTextbox(self, height=200)
        self.result_textbox.pack(fill="both", expand=True, padx=10, pady=10)

    def select_file(self):
        """Abre un cuadro de diálogo para seleccionar el archivo."""
        from tkinter import filedialog

        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=(
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*"),
            ),
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
                data = line.strip().split(":")
                if len(data) == 4 and data[3].endswith(";"):
                    placa, marca, modelo, precio = map(str.strip, data)
                    precio = precio.rstrip(";")
                    try:
                        precio = float(precio)
                        if precio <= 0:
                            raise ValueError("El precio debe ser un número positivo.")
                        # Crear y agregar vehículo
                        vehicle = Vehiculo(placa, marca, modelo, precio)
                        self.btree.insert_value(vehicle)
                        added_count += 1
                    except ValueError as ve:
                        self.result_textbox.insert("end", f"Error en la línea: {line.strip()} - {ve}\n")
                else:
                    self.result_textbox.insert("end", f"Formato inválido en la línea: {line.strip()}\n")

            self.result_textbox.insert("end", f"{added_count} vehículos agregados correctamente.\n")
        except Exception as e:
            self.result_textbox.insert("end", f"Error al procesar el archivo: {e}\n")


class TripModule(ctk.CTkFrame):
    def __init__(self, parent, client_list, vehicle_tree, adjacency_list, trip_list, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.client_list = client_list
        self.vehicle_tree = vehicle_tree
        self.adjacency_list = adjacency_list
        self.trip_list = trip_list
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Gestión de Viajes", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)

        # Selección de cliente
        self.client_label = ctk.CTkLabel(self, text="Seleccione Cliente:")
        self.client_label.pack(pady=5)
        self.client_combobox = ctk.CTkComboBox(self, values=self.get_clients())
        self.client_combobox.pack(pady=5)

        # Selección de vehículo
        self.vehicle_label = ctk.CTkLabel(self, text="Seleccione Vehículo:")
        self.vehicle_label.pack(pady=5)
        self.vehicle_combobox = ctk.CTkComboBox(self, values=self.get_vehicles())
        self.vehicle_combobox.pack(pady=5)

        # Selección de origen y destino
        self.origin_label = ctk.CTkLabel(self, text="Seleccione Origen:")
        self.origin_label.pack(pady=5)
        self.origin_combobox = ctk.CTkComboBox(self, values=self.get_locations())
        self.origin_combobox.pack(pady=5)

        self.destination_label = ctk.CTkLabel(self, text="Seleccione Destino:")
        self.destination_label.pack(pady=5)
        self.destination_combobox = ctk.CTkComboBox(self, values=self.get_locations())
        self.destination_combobox.pack(pady=5)

        # Botón para crear viaje
        self.create_trip_button = ctk.CTkButton(self, text="Crear Viaje", command=self.create_trip)
        self.create_trip_button.pack(pady=20)

        # Botón para mostrar estructura de viaje
        self.show_trip_button = ctk.CTkButton(self, text="Mostrar Viaje", command=self.show_trip_structure)
        self.show_trip_button.pack(pady=20)

        # Área de resultados para mostrar la estructura del viaje
        #self.result_text = ctk.CTkTextbox(self, height=200)
        #self.result_text.pack(fill="both", expand=True, padx=10, pady=10)

    def get_clients(self):
        """Obtiene todos los clientes de la lista circular."""
        clients = []
        current = self.client_list.head
        if current:
            while True:
                clients.append(f"{current.client.dpi} - {current.client.nombres}")
                current = current.next
                if current == self.client_list.head:
                    break
        return clients

    def get_vehicles(self):
        """Obtiene todos los vehículos del árbol B."""
        vehicles = []

        def traverse(node):
            if node:
                for key in node.keys:
                    vehicles.append(f"{key.placa} - {key.marca}")
                for child in node.children:
                    traverse(child)

        traverse(self.vehicle_tree.root)
        return vehicles

    def get_locations(self):
        """Obtiene todos los nodos de origen de la lista de adyacencia."""
        locations = []
        current = self.adjacency_list.head
        while current:
            locations.append(current.origen)
            current = current.next
        return locations

    def create_trip(self):
        """Crea un viaje basado en los datos seleccionados."""
        cliente = self.client_combobox.get()
        vehiculo = self.vehicle_combobox.get()
        origen = self.origin_combobox.get()
        destino = self.destination_combobox.get()

        if not (cliente and vehiculo and origen and destino):
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        try:
            # Calcular la ruta más corta
            paths = self.calculate_shortest_path(origen, destino)
            if not paths:
                messagebox.showerror("Error", "No se encontró una ruta válida entre los puntos seleccionados.")
                return

            # Crear el viaje
            self.trip_list.insert(origen, destino, "Fecha y Hora", cliente, vehiculo, paths)
            messagebox.showinfo("Éxito", "Viaje creado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el viaje: {e}")

    def calculate_shortest_path(self, origen, destino):
        """
        Calcula la ruta más corta desde origen hasta destino utilizando el algoritmo de Dijkstra.
        Devuelve una lista de objetos `camino` representando el camino más corto.
        """
        # Inicializar estructuras
        distances = {}
        previous_nodes = {}
        unvisited_nodes = set()

        # Población inicial de las estructuras
        current = self.adjacency_list.head
        while current:
            distances[current.origen] = float('inf')  # Distancia infinita inicialmente
            previous_nodes[current.origen] = None  # Nodo previo para reconstrucción
            unvisited_nodes.add(current.origen)
            current = current.next

        # Establecer la distancia inicial del nodo origen
        distances[origen] = 0

        while unvisited_nodes:
            # Elegir el nodo con la menor distancia en `distances`
            current_node = min(
                unvisited_nodes, key=lambda node: distances[node]
            )
            unvisited_nodes.remove(current_node)

            # Si llegamos al destino, terminamos
            if current_node == destino:
                break

            # Buscar las rutas salientes del nodo actual
            current = self.adjacency_list.head
            while current and current.origen != current_node:
                current = current.next

            if current:
                adj_node = current.adjacency_list
                while adj_node:
                    neighbor = adj_node.ruta.destino
                    new_distance = distances[current_node] + adj_node.ruta.tiempo
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous_nodes[neighbor] = current_node
                    adj_node = adj_node.next

        # Reconstruir el camino más corto
        path = []
        current_node = destino
        while current_node and previous_nodes[current_node] is not None:
            prev_node = previous_nodes[current_node]
            current = self.adjacency_list.head
            while current and current.origen != prev_node:
                current = current.next

            if current:
                adj_node = current.adjacency_list
                while adj_node and adj_node.ruta.destino != current_node:
                    adj_node = adj_node.next

                if adj_node:
                    path.insert(0, camino(prev_node, current_node, adj_node.ruta.tiempo))

            current_node = prev_node

        # Si no hay camino encontrado
        if not path:
            return []

        return path

    def show_trip_structure(self):
        """Muestra la estructura de un viaje seleccionado."""
        trip_id = simpledialog.askinteger("Seleccionar Viaje", "Ingrese el ID del viaje:")
        if not trip_id:
            return

        # Buscar el viaje por ID
        current = self.trip_list.head
        while current:
            if current.trip.id == trip_id:
                self.display_trip_graph(current.trip)
                return
            current = current.next

        messagebox.showerror("Error", f"No se encontró un viaje con ID {trip_id}.")

    def display_trip_graph(self, trip):
        """Genera y muestra el gráfico del camino del viaje, incluyendo el tiempo total."""
        try:
            # Calcular el tiempo total del camino
            total_time = 0
            camino = trip.camino.head
            while camino:
                total_time += camino.path.duracion
                camino = camino.next

            # Generar el gráfico del camino
            filename = f"trip_{trip.id}_path"
            trip.camino.save_png(filename)  # Genera el archivo PNG
            image_path = f"{filename}.png"

            if os.path.exists(image_path):
                # Mostrar el tiempo total antes del gráfico
                messagebox.showinfo("Tiempo Total", f"El tiempo total del viaje es: {total_time} minutos.")
                self.display_graph(image_path)
            else:
                messagebox.showerror("Error", "No se pudo generar el gráfico del camino.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el gráfico del camino: {e}")

    def display_graph(self, image_path):
        """Muestra el gráfico generado en la interfaz."""
        try:
            # Cargar la imagen
            image = Image.open(image_path)
            image = image.resize((600, 400), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            # Crear o actualizar un widget para mostrar la imagen
            if hasattr(self, "graph_label"):
                self.graph_label.configure(image=photo)
                self.graph_label.image = photo  # Mantener referencia para evitar garbage collection
            else:
                self.graph_label = ctk.CTkLabel(self, image=photo)
                self.graph_label.pack(pady=20)
                self.graph_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen del gráfico: {e}")




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
