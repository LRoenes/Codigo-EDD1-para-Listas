class NodoTarea:
    def __init__(self, codigo, nombre, materia, fechaEntrega, prioridad, next=None):
        self.codigo = codigo
        self.nombre = nombre
        self.materia = materia
        self.fechaEntrega = fechaEntrega
        self.prioridad = prioridad
        self.next = next


class ListaTareas:  # Lista simple
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def length(self):
        contador = 0
        actual = self.head
        while actual is not None:
            contador += 1
            actual = actual.next
        return contador

    def insertar(self, codigo, nombre, materia, fechaEntrega, prioridad):
        self.head = NodoTarea(codigo, nombre, materia, fechaEntrega, prioridad, next=self.head)

    def print_list(self):
        node = self.head
        while node is not None:
            print(node.codigo, node.nombre, node.materia, node.fechaEntrega, node.prioridad, end=" --> ")
            node = node.next
        print()

    def asignarPrioridad(self, prioridad):
        if prioridad == "Alta":
            return 3
        elif prioridad == "Media":
            return 2
        elif prioridad == "Baja":
            return 1
        else:
            return 0

    def filtrar_por_materia(self, materiaABuscar):
        listaFiltrada = ListaTareas()
        actual = self.head
        while actual is not None:
            if actual.materia == materiaABuscar:
                listaFiltrada.insertar(
                    actual.codigo, actual.nombre, actual.materia,
                    actual.fechaEntrega, actual.prioridad
                )
            actual = actual.next
        return listaFiltrada

    def filtrar_por_prioridad(self):
        listaTareasCircular = Lista_circular()
        actual = self.head
        while actual is not None:
            if actual.prioridad == "Alta":
                listaTareasCircular.add_First(
                    actual.codigo, actual.nombre, actual.materia,
                    actual.fechaEntrega, actual.prioridad
                )
            actual = actual.next
        return listaTareasCircular

    def ordenar_lista(self):
        if self.head is None or self.head.next is None:
            return

        cambiado = True
        while cambiado:
            cambiado = False
            actual = self.head
            anterior = None
            while actual.next:
                siguiente = actual.next
                if self.asignarPrioridad(actual.prioridad) < self.asignarPrioridad(siguiente.prioridad):
                    cambiado = True
                    if anterior is None:
                        self.head = siguiente
                    else:
                        anterior.next = siguiente
                    actual.next = siguiente.next
                    siguiente.next = actual
                    anterior = siguiente
                else:
                    anterior = actual
                    actual = actual.next


class Lista_circular:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def length(self):
        if self.head is None:
            return 0
        actual = self.head
        contador = 1  # head ya cuenta
        while actual.next is not self.head:
            actual = actual.next
            contador += 1
        return contador

    def ultimo(self):
        """Devuelve el nodo último (el que apunta a head)."""
        if self.head is None:
            return None
        actual = self.head
        while actual.next is not self.head:
            actual = actual.next
        return actual

    def add_First(self, codigo, nombre, materia, fechaEntrega, prioridad):
        nuevo = NodoTarea(codigo, nombre, materia, fechaEntrega, prioridad)
        if self.head is None:
            self.head = nuevo
            nuevo.next = nuevo
            return
        ultimo = self.ultimo()
        nuevo.next = self.head
        ultimo.next = nuevo
        self.head = nuevo

    def imprimir(self):
        if self.is_empty():
            print("(lista vacia)")
            return
        cur = self.head
        print(cur.codigo, cur.nombre, cur.materia, cur.fechaEntrega, cur.prioridad, end=" --> ")
        while cur.next != self.head:
            cur = cur.next
            print(cur.codigo, cur.nombre, cur.materia, cur.fechaEntrega, cur.prioridad, end=" --> ")
        print("(apunta a head)")

    def ordenar_por_fecha(self):
        if self.head is None or self.head.next == self.head:
            return

        n = self.length()
        for i in range(n):
            cambiado = False
            anterior = self.ultimo()
            actual = self.head

            for j in range(n - 1):
                siguiente = actual.next
                if actual.fechaEntrega < siguiente.fechaEntrega:
                    cambiado = True

                    # Intercambio de enlaces de los nodos
                    actual.next = siguiente.next
                    siguiente.next = actual
                    anterior.next = siguiente

                    # Si movimos el head viejo, actualizamos head
                    if actual == self.head:
                        self.head = siguiente

                    anterior = siguiente
                else:
                    anterior = actual
                    actual = actual.next

            if not cambiado:
                break

    def remove_node(self, codigo):
        if self.is_empty():
            return

        if codigo == self.head.codigo:
            if self.head.next == self.head:
                self.head = None
                return
            cur = self.head
            while cur.next != self.head:
                cur = cur.next
            cur.next = self.head.next
            self.head = self.head.next
            return

        cur = self.head
        pre = None
        while cur.next != self.head and cur.codigo != codigo:
            pre = cur
            cur = cur.next

        if cur.codigo == codigo:
            pre.next = cur.next

    def recorrer(self):
        if self.is_empty():
            print("(lista vacia)")
            return
        cur = self.head
        while True:
            print(cur.codigo, cur.nombre, cur.materia, cur.fechaEntrega, cur.prioridad, end=" --> ")
            print("\n¿Deseas eliminar esta tarea? (si/no)")
            x = input().strip().lower()
            codigo_actual = cur.codigo
            siguiente = cur.next
            if x == "si":
                self.remove_node(codigo_actual)
                if self.head is None:
                    print("La lista quedó vacía.")
                    return
            cur = siguiente
            if cur == self.head:
                break
        print("(apunta a head)")


tareas = ListaTareas()
tareas.insertar(1, "Taller listas", "Estructura de Datos", 20260420, "Alta")
tareas.insertar(2, "Ensayo", "Física", 20260425, "Media")
tareas.insertar(3, "Parcial 1", "Cálculo", 20260418, "Alta")
tareas.insertar(4, "Quiz", "Física", 20260419, "Baja")
tareas.insertar(5, "Proyecto", "Estructura de Datos", 20260501, "Alta")
tareas.insertar(6, "Lectura", "Física", 20260422, "Media")
tareas.insertar(7, "Laboratorio", "Física", 20260421, "Alta")
tareas.insertar(8, "Exposición", "Estructura de Datos", 20260423, "Media")
tareas.insertar(9, "Actividad", "Cálculo", 20260424, "Baja")
tareas.insertar(10, "Parcial", "Estructura de Datos", 20260426, "Alta")
tareas.insertar(11, "Laboratorio", "Física", 20260430, "Alta")
tareas.insertar(12, "Laboratorio", "Física", 20260405, "Alta")
tareas.insertar(13, "Laboratorio", "Física", 20260420, "Alta")
tareas.insertar(14, "Laboratorio", "Física", 20260410, "Alta")
tareas.insertar(15, "Laboratorio", "Física", 20260419, "Alta")

print("--- Lista Simple Inicial ---")
tareas.print_list()

print("\n--- Filtrado por Física ---")
lista2 = tareas.filtrar_por_materia("Física")
lista2.print_list()

print("\n--- Filtrado ordenado por prioridad ---")
lista2.ordenar_lista()
lista2.print_list()

print("\n--- Lista Circular Filtrada (Prioridad Alta) ---")
listaCircular = lista2.filtrar_por_prioridad()
listaCircular.imprimir()

print("\n--- Lista Circular Ordenada por Fecha (Modificando enlaces) ---")
listaCircular.ordenar_por_fecha()
listaCircular.imprimir()

listaCircular.recorrer()
listaCircular.imprimir()
