### **Manual Técnico para la Aplicación de Gestión de Viajes "Llega Rapidito"**

---

### **Descripción General del Proyecto**
"Llega Rapidito" es una aplicación de gestión de viajes desarrollada en Python que emplea estructuras de datos avanzadas para administrar rutas, clientes, vehículos y viajes. Incluye una interfaz gráfica de usuario (GUI) para facilitar la interacción con las funcionalidades principales.

---

### **Requisitos Técnicos**

#### **Software y Dependencias**
- **Python**: Versión 3.9 o superior.
- **Bibliotecas**:
  - `customtkinter`: Para la creación de la GUI.
  - `PIL` (Pillow): Para la manipulación de imágenes.
  - `graphviz`: Para la generación de representaciones gráficas de estructuras de datos.

#### **Archivos del Proyecto**
- **GUI.py**: Punto de entrada principal de la aplicación.
- **Adjacency_List.py**: Implementación de la lista de adyacencia para la gestión de rutas.
- **Simple_List_Path.py**: Lista simple para almacenar caminos entre nodos.
- **Path.py**: Clase para representar un camino entre dos nodos.
- **Route.py**: Clase que define una ruta con origen, destino y tiempo.
- **Trip.py**: Clase que encapsula un viaje con su información básica.
- **Simple_List_Trip.py**: Lista simple para almacenar los viajes creados.
- **DoLinkedCirList.py**: Lista circular doblemente enlazada para la gestión de clientes.
- **Btree.py**: Implementación del árbol B para la gestión de vehículos.
- **Client.py**: Clase que representa un cliente con datos personales.
- **Vehicle.py**: Clase que define las características de un vehículo.

---

### **Estructura del Proyecto**

#### **Estructuras de Datos Utilizadas**
1. **Lista de Adyacencia**:
   - Representa las rutas entre diferentes destinos.
   - Métodos principales:
     - `insert`: Añade una nueva ruta.
     - `modify`: Modifica el tiempo de una ruta existente.
     - `delete`: Elimina una ruta.
     - `generate_graphviz`: Crea un gráfico visual de las rutas.

2. **Lista Circular Doblemente Enlazada**:
   - Gestiona los clientes registrados.
   - Métodos principales:
     - `add`: Añade un nuevo cliente.
     - `remove`: Elimina un cliente por su DPI.
     - `generate_graphviz`: Crea una visualización de los clientes.

3. **Árbol B**:
   - Administra los vehículos disponibles.
   - Métodos principales:
     - `insert_value`: Inserta un nuevo vehículo.
     - `delete`: Elimina un vehículo.
     - `print_vehicle`: Genera una representación gráfica del árbol.

4. **Lista Simple de Viajes**:
   - Almacena y organiza los viajes creados.
   - Métodos principales:
     - `insert`: Añade un nuevo viaje.
     - `save_png`: Genera una representación gráfica de la lista de viajes.

---

### **Funcionamiento Interno**

#### **Inicio de la Aplicación**
- El archivo `GUI.py` inicia la aplicación creando una ventana de bienvenida mediante `customtkinter`.
- Al acceder al menú principal, se instancian las estructuras de datos necesarias para gestionar clientes, rutas, vehículos y viajes.

#### **Módulos de la Aplicación**
1. **Clientes**:
   - **Funciones clave**: Añadir, modificar, eliminar y visualizar clientes.
   - **Estructura utilizada**: Lista circular doblemente enlazada.

2. **Rutas**:
   - **Funciones clave**: Añadir, modificar, eliminar y visualizar rutas.
   - **Estructura utilizada**: Lista de adyacencia.

3. **Vehículos**:
   - **Funciones clave**: Añadir, modificar, eliminar y visualizar vehículos.
   - **Estructura utilizada**: Árbol B.

4. **Viajes**:
   - **Funciones clave**: Crear y visualizar viajes.
   - **Estructura utilizada**: Lista simple.

5. **Reportes**:
   - Genera estadísticas como los viajes más largos, vehículos más usados, y clientes más frecuentes.

---

### **Representación Gráfica**
- **Graphviz** se utiliza para visualizar estructuras de datos complejas.
  - Se generan imágenes en formato PNG mediante métodos específicos en cada clase.
  - Ejemplo de uso: `generate_graphviz` en la lista de adyacencia crea un gráfico de las rutas disponibles.

---

### **Errores Comunes y Soluciones**
1. **Error al cargar archivos de texto**:
   - **Causa**: Formato incorrecto.
   - **Solución**: Verifique que el archivo respete el formato esperado.

2. **Visualizaciones no generadas**:
   - **Causa**: Dependencia faltante o datos insuficientes.
   - **Solución**: Instale `graphviz` y asegúrese de que existan datos registrados.

3. **Errores en la GUI**:
   - **Causa**: Configuración errónea o datos incompletos.
   - **Solución**: Verifique que todos los campos estén correctamente completados.

---

### **Pruebas Unitarias**
- Cada clase y estructura cuenta con métodos básicos para validar su correcto funcionamiento.
- Ejemplo:
  - **Lista de Adyacencia**:
    ```python
    routes = AdjacencyList()
    routes.insert("A", Ruta("A", "B", 10))
    routes.show_information()
    ```

---



### **Contacto de Soporte**
Para consultas técnicas, contacto: Daniel Andreé Hernandez Flores - 202300512
