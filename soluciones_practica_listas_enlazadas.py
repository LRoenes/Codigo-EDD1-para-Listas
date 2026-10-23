"""
SOLUCIONES DE PRACTICA - ESTRUCTURAS DE DATOS I
Listas enlazadas simples y circulares.

Este archivo es una guia ejecutable para estudiar dos ejercicios similares:
1) Gestion de tareas.
2) Inventario y carrito de compras.

Restriccion respetada: no se usan listas nativas de Python (ni [] ni list()).
Los datos se almacenan en nodos enlazados. Los corchetes que aparecen en
comentarios/docstrings son solo texto explicativo.
"""

# ============================================================
# UTILIDAD: comparar prioridades
# ============================================================

def rango_prioridad(prioridad):
    prioridad = prioridad.strip().lower()
    if prioridad == "alta":
        return 1
    if prioridad == "media":
        return 2
    if prioridad == "baja":
        return 3
    return 4


# ============================================================
# EJERCICIO 1: LISTA SIMPLE DE TAREAS
# ============================================================

class Tarea:
    def __init__(self, codigo, nombre, asignatura, fecha_limite, prioridad):
        self.codigo = codigo
        self.nombre = nombre
        self.asignatura = asignatura
        self.fecha_limite = int(fecha_limite)  # formato AAAAMMDD
        self.prioridad = prioridad.title()

    def __str__(self):
        return (f"Codigo: {self.codigo} | Tarea: {self.nombre} | "
                f"Asignatura: {self.asignatura} | Fecha: {self.fecha_limite} | "
                f"Prioridad: {self.prioridad}")


class NodoTarea:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaTareas:
    def __init__(self):
        self.cabeza = None

    def esta_vacia(self):
        return self.cabeza is None

    def agregar_final(self, tarea):
        nuevo = NodoTarea(tarea)
        if self.cabeza is None:
            self.cabeza = nuevo
            return
        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo

    def mostrar(self):
        if self.esta_vacia():
            print("No hay tareas.")
            return
        actual = self.cabeza
        while actual is not None:
            print(actual.dato)
            actual = actual.siguiente

    def filtrar_asignatura(self, asignatura):
        resultado = ListaTareas()
        actual = self.cabeza
        while actual is not None:
            if actual.dato.asignatura.lower() == asignatura.lower():
                resultado.agregar_final(actual.dato)
            actual = actual.siguiente
        return resultado

    def ordenar_prioridad(self):
        # Ordenamiento burbuja intercambiando los datos de los nodos.
        if self.cabeza is None:
            return
        hubo_cambio = True
        while hubo_cambio:
            hubo_cambio = False
            actual = self.cabeza
            while actual.siguiente is not None:
                if rango_prioridad(actual.dato.prioridad) > rango_prioridad(
                        actual.siguiente.dato.prioridad):
                    temporal = actual.dato
                    actual.dato = actual.siguiente.dato
                    actual.siguiente.dato = temporal
                    hubo_cambio = True
                actual = actual.siguiente

    def buscar_codigo(self, codigo):
        actual = self.cabeza
        while actual is not None:
            if actual.dato.codigo == codigo:
                return actual.dato
            actual = actual.siguiente
        return None


# ============================================================
# EJERCICIO 1: LISTA CIRCULAR DE TAREAS
# ============================================================

class NodoTareaCircular:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaCircularTareas:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamano = 0

    def esta_vacia(self):
        return self.cabeza is None

    def agregar_final(self, tarea):
        nuevo = NodoTareaCircular(tarea)
        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
            nuevo.siguiente = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self.tamano += 1

    def mostrar(self):
        if self.cabeza is None:
            print("La lista circular esta vacia.")
            return
        actual = self.cabeza
        for _ in range(self.tamano):
            print(actual.dato)
            actual = actual.siguiente

    def agregar_altas_de_asignatura(self, lista_simple, asignatura):
        actual = lista_simple.cabeza
        agregadas = 0
        while actual is not None:
            tarea = actual.dato
            if (tarea.asignatura.lower() == asignatura.lower()
                    and tarea.prioridad.lower() == "alta"):
                self.agregar_final(tarea)
                agregadas += 1
            actual = actual.siguiente
        return agregadas

    def adelantar_por_fecha(self):
        """Mueve la tarea con fecha mas cercana a la cabeza sin romper el ciclo."""
        if self.cabeza is None or self.cabeza is self.cola:
            return False

        anterior = self.cola
        actual = self.cabeza
        anterior_mejor = self.cola
        mejor = self.cabeza

        for _ in range(self.tamano):
            if actual.dato.fecha_limite < mejor.dato.fecha_limite:
                mejor = actual
                anterior_mejor = anterior
            anterior = actual
            actual = actual.siguiente

        if mejor is self.cabeza:
            return True

        # Desenganchar el nodo elegido.
        anterior_mejor.siguiente = mejor.siguiente
        if mejor is self.cola:
            self.cola = anterior_mejor

        # Insertarlo como nueva cabeza.
        mejor.siguiente = self.cabeza
        self.cabeza = mejor
        self.cola.siguiente = self.cabeza
        return True

    def eliminar_codigo(self, codigo):
        if self.cabeza is None:
            return False

        anterior = self.cola
        actual = self.cabeza

        for _ in range(self.tamano):
            if actual.dato.codigo == codigo:
                if self.tamano == 1:
                    self.cabeza = None
                    self.cola = None
                else:
                    anterior.siguiente = actual.siguiente
                    if actual is self.cabeza:
                        self.cabeza = actual.siguiente
                    if actual is self.cola:
                        self.cola = anterior
                    self.cola.siguiente = self.cabeza
                self.tamano -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def preguntar_completadas(self):
        """Pregunta por cada tarea y elimina las que el usuario marque como hechas."""
        if self.cabeza is None:
            print("No hay tareas pendientes.")
            return

        actual = self.cabeza
        procesadas = 0
        # El numero de nodos por procesar se fija antes de comenzar.
        cantidad_inicial = self.tamano
        while procesadas < cantidad_inicial and self.cabeza is not None:
            siguiente = actual.siguiente
            respuesta = input(
                f"¿Terminaste '{actual.dato.nombre}' (codigo {actual.dato.codigo})? (s/n): "
            ).strip().lower()
            if respuesta == "s" or respuesta == "si":
                self.eliminar_codigo(actual.dato.codigo)
            actual = siguiente
            procesadas += 1
            # Si se borro la cabeza, el puntero guardado puede apuntar a un nodo
            # eliminado pero su enlace sigue siendo util; reiniciar desde cabeza
            # evita recorrer referencias fuera del ciclo actualizado.
            if self.cabeza is not None and procesadas < cantidad_inicial:
                actual = self.cabeza
                for _ in range(min(procesadas, self.tamano)):
                    actual = actual.siguiente


def demo_tareas():
    print("\n" + "=" * 60)
    print("EJERCICIO 1 - GESTION DE TAREAS")
    print("=" * 60)
    tareas = ListaTareas()
    tareas.agregar_final(Tarea(101, "Taller de nodos", "Estructura de Datos", 20261025, "Alta"))
    tareas.agregar_final(Tarea(102, "Leer capitulos", "Bases de Datos", 20261028, "Media"))
    tareas.agregar_final(Tarea(103, "Resolver ejercicios", "Estructura de Datos", 20261023, "Alta"))
    tareas.agregar_final(Tarea(104, "Informe", "Calculo", 20261102, "Baja"))
    tareas.agregar_final(Tarea(105, "Repasar recursividad", "Estructura de Datos", 20261030, "Media"))
    tareas.agregar_final(Tarea(106, "Quiz", "Bases de Datos", 20261024, "Alta"))
    tareas.agregar_final(Tarea(107, "Proyecto", "Calculo", 20261105, "Media"))
    tareas.agregar_final(Tarea(108, "Practica", "Estructura de Datos", 20261022, "Baja"))
    tareas.agregar_final(Tarea(109, "Lectura", "Calculo", 20261026, "Alta"))
    tareas.agregar_final(Tarea(110, "Estudiar", "Bases de Datos", 20261031, "Baja"))

    print("\nTodas las tareas:")
    tareas.mostrar()

    asignatura = "Estructura de Datos"
    print(f"\nTareas de {asignatura}, ordenadas por prioridad:")
    filtradas = tareas.filtrar_asignatura(asignatura)
    filtradas.ordenar_prioridad()
    filtradas.mostrar()

    circular = ListaCircularTareas()
    circular.agregar_altas_de_asignatura(tareas, asignatura)
    print(f"\nTareas de prioridad Alta de {asignatura} en lista circular:")
    circular.mostrar()

    circular.adelantar_por_fecha()
    print("\nLista circular luego de adelantar la fecha mas cercana:")
    circular.mostrar()

    # Descomenta esta linea para probar la eliminacion interactiva.
    # circular.preguntar_completadas()


# ============================================================
# EJERCICIO 2: INVENTARIO EN LISTA SIMPLE
# ============================================================

class Producto:
    def __init__(self, codigo, nombre, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = float(precio)

    def __str__(self):
        return f"Codigo: {self.codigo} | {self.nombre} | Precio unitario: ${self.precio:.2f}"


class NodoProducto:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Inventario:
    def __init__(self):
        self.cabeza = None

    def agregar_final(self, producto):
        nuevo = NodoProducto(producto)
        if self.cabeza is None:
            self.cabeza = nuevo
            return
        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo

    def mostrar(self):
        if self.cabeza is None:
            print("Inventario vacio.")
            return
        actual = self.cabeza
        while actual is not None:
            print(actual.dato)
            actual = actual.siguiente

    def ordenar_por_precio(self):
        hubo_cambio = True
        while hubo_cambio:
            hubo_cambio = False
            actual = self.cabeza
            while actual is not None and actual.siguiente is not None:
                if actual.dato.precio > actual.siguiente.dato.precio:
                    temporal = actual.dato
                    actual.dato = actual.siguiente.dato
                    actual.siguiente.dato = temporal
                    hubo_cambio = True
                actual = actual.siguiente

    def cinco_mas_baratos(self):
        """Devuelve una nueva lista simple con hasta los cinco primeros productos."""
        resultado = Inventario()
        actual = self.cabeza
        contador = 0
        while actual is not None and contador < 5:
            p = actual.dato
            resultado.agregar_final(Producto(p.codigo, p.nombre, p.precio))
            contador += 1
            actual = actual.siguiente
        return resultado


# ============================================================
# EJERCICIO 2: CARRITO EN LISTA CIRCULAR
# ============================================================

class ItemCarrito:
    def __init__(self, codigo, nombre, precio_unitario, cantidad):
        self.codigo = codigo
        self.nombre = nombre
        self.precio_unitario = float(precio_unitario)
        self.cantidad = int(cantidad)
        self.total = self.precio_unitario * self.cantidad

    def __str__(self):
        return (f"Codigo: {self.codigo} | {self.nombre} | "
                f"Unitario: ${self.precio_unitario:.2f} | Cantidad: {self.cantidad} | "
                f"Total: ${self.total:.2f}")


class NodoCarrito:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class CarritoCompras:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamano = 0

    def esta_vacio(self):
        return self.cabeza is None

    def agregar_final(self, item):
        nuevo = NodoCarrito(item)
        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
            nuevo.siguiente = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self.tamano += 1

    def mostrar(self):
        if self.cabeza is None:
            print("Carrito vacio.")
            return
        actual = self.cabeza
        for _ in range(self.tamano):
            print(actual.dato)
            actual = actual.siguiente
        print(f"Total del carrito: ${self.total_carrito():.2f}")

    def total_carrito(self):
        suma = 0.0
        actual = self.cabeza
        for _ in range(self.tamano):
            suma += actual.dato.total
            actual = actual.siguiente
        return suma

    def ordenar_por_total(self):
        if self.tamano < 2:
            return
        hubo_cambio = True
        while hubo_cambio:
            hubo_cambio = False
            actual = self.cabeza
            for _ in range(self.tamano - 1):
                siguiente = actual.siguiente
                if actual.dato.total > siguiente.dato.total:
                    temporal = actual.dato
                    actual.dato = siguiente.dato
                    siguiente.dato = temporal
                    hubo_cambio = True
                actual = siguiente

    def eliminar_codigo(self, codigo):
        if self.cabeza is None:
            return False
        anterior = self.cola
        actual = self.cabeza
        for _ in range(self.tamano):
            if actual.dato.codigo == codigo:
                if self.tamano == 1:
                    self.cabeza = None
                    self.cola = None
                else:
                    anterior.siguiente = actual.siguiente
                    if actual is self.cabeza:
                        self.cabeza = actual.siguiente
                    if actual is self.cola:
                        self.cola = anterior
                    self.cola.siguiente = self.cabeza
                self.tamano -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def comprar_dos(self, codigo_uno, codigo_dos):
        """Simula comprar/eliminar dos productos seleccionados por codigo."""
        if codigo_uno == codigo_dos:
            print("Selecciona dos codigos diferentes.")
            return
        eliminado_uno = self.eliminar_codigo(codigo_uno)
        eliminado_dos = self.eliminar_codigo(codigo_dos)
        if eliminado_uno:
            print(f"Producto {codigo_uno} comprado y retirado del carrito.")
        else:
            print(f"No se encontro el producto {codigo_uno}.")
        if eliminado_dos:
            print(f"Producto {codigo_dos} comprado y retirado del carrito.")
        else:
            print(f"No se encontro el producto {codigo_dos}.")


def demo_carrito():
    print("\n" + "=" * 60)
    print("EJERCICIO 2 - INVENTARIO Y CARRITO")
    print("=" * 60)
    inventario = Inventario()
    inventario.agregar_final(Producto(201, "Cuaderno", 4500))
    inventario.agregar_final(Producto(202, "Lapicero", 1800))
    inventario.agregar_final(Producto(203, "Borrador", 1200))
    inventario.agregar_final(Producto(204, "Regla", 2500))
    inventario.agregar_final(Producto(205, "Marcador", 3200))
    inventario.agregar_final(Producto(206, "Carpeta", 2100))
    inventario.agregar_final(Producto(207, "Resaltador", 2800))
    inventario.agregar_final(Producto(208, "Tijeras", 5200))
    inventario.agregar_final(Producto(209, "Pegante", 3000))
    inventario.agregar_final(Producto(210, "Block", 6000))

    print("\nInventario original:")
    inventario.mostrar()

    inventario.ordenar_por_precio()
    print("\nInventario ordenado por precio ascendente:")
    inventario.mostrar()

    baratos = inventario.cinco_mas_baratos()
    print("\nLos cinco productos mas economicos:")
    baratos.mostrar()

    carrito = CarritoCompras()
    actual = baratos.cabeza
    while actual is not None:
        cantidad = 2 if actual.dato.codigo % 2 == 0 else 1
        p = actual.dato
        carrito.agregar_final(ItemCarrito(p.codigo, p.nombre, p.precio, cantidad))
        actual = actual.siguiente

    carrito.ordenar_por_total()
    print("\nCarrito circular ordenado por total de cada producto:")
    carrito.mostrar()

    # Para la demostracion, se compran los dos primeros codigos del carrito.
    if carrito.cabeza is not None and carrito.tamano >= 2:
        codigo_uno = carrito.cabeza.dato.codigo
        codigo_dos = carrito.cabeza.siguiente.dato.codigo
        print("\nCompra de dos productos seleccionados:")
        carrito.comprar_dos(codigo_uno, codigo_dos)

    print("\nProductos que quedan en el carrito:")
    carrito.mostrar()


if __name__ == "__main__":
    demo_tareas()
    demo_carrito()
