"""
=====================================================================
GUIA FINAL BASICA - ESTRUCTURAS DE DATOS 1
  1. Eliminar (lo mas basico)      -> lista simple y circular
  2. Ordenar  (lo mas basico)      -> lista simple y circular
  3. Nodo que guarda una LISTA como atributo (ej: estudiante con notas)
=====================================================================
Ejecuta el archivo: cada ejemplo imprime ANTES y DESPUES.
Cada metodo es corto a proposito: puedes escribirlo de memoria en el parcial.
"""


class Nodo:
    def __init__(self, data):
        self.data = data
        self.next = None


# =====================================================================
# 1. LISTA SIMPLE
# =====================================================================
class ListaSimple:
    def __init__(self):
        self.head = None

    def agregar_al_final(self, data):
        nuevo = Nodo(data)
        if self.head is None:
            self.head = nuevo
            return
        actual = self.head
        while actual.next is not None:
            actual = actual.next
        actual.next = nuevo

    def imprimir(self):
        if self.head is None:
            print("(lista vacia)")
            return
        actual = self.head
        texto = ""
        while actual is not None:
            texto += str(actual.data) + " --> "
            actual = actual.next
        print(texto + "None")

    # ---------------- ELIMINAR ----------------
    def eliminar_inicio(self):
        if self.head is None:                # lista vacia
            print("La lista esta vacia")
            return
        self.head = self.head.next           # el segundo pasa a ser el primero

    def eliminar_final(self):
        if self.head is None:                # lista vacia
            print("La lista esta vacia")
            return
        if self.head.next is None:           # un solo nodo
            self.head = None
            return
        actual = self.head
        while actual.next.next is not None:  # parar en el PENULTIMO
            actual = actual.next
        actual.next = None

    def eliminar_dato(self, dato):
        if self.head is None:                # lista vacia
            print("La lista esta vacia")
            return
        if self.head.data == dato:           # el dato esta en el primero
            self.head = self.head.next
            return
        anterior = self.head
        actual = self.head.next
        while actual is not None:
            if actual.data == dato:
                anterior.next = actual.next  # saltarse el nodo
                return
            anterior = actual
            actual = actual.next
        print(f"El dato {dato} no existe")   # dato inexistente

    def eliminar_posicion(self, pos):
        if self.head is None:
            print("La lista esta vacia")
            return
        if pos < 0:
            print("Posicion invalida")
            return
        if pos == 0:
            self.head = self.head.next
            return
        anterior = self.head
        for _ in range(pos - 1):             # llegar al nodo ANTERIOR a la posicion
            anterior = anterior.next
            if anterior is None:
                print("Posicion fuera de rango")
                return
        if anterior.next is None:
            print("Posicion fuera de rango")
            return
        anterior.next = anterior.next.next

    # ---------------- ORDENAR (burbuja, intercambiando los datos) ----------------
    def ordenar_ascendente(self):
        if self.head is None or self.head.next is None:
            return
        cambio = True
        while cambio:
            cambio = False
            actual = self.head
            while actual.next is not None:
                if actual.data > actual.next.data:      # mal orden: intercambiar
                    actual.data, actual.next.data = actual.next.data, actual.data
                    cambio = True
                actual = actual.next

    def ordenar_descendente(self):
        if self.head is None or self.head.next is None:
            return
        cambio = True
        while cambio:
            cambio = False
            actual = self.head
            while actual.next is not None:
                if actual.data < actual.next.data:      # unico cambio: < en vez de >
                    actual.data, actual.next.data = actual.next.data, actual.data
                    cambio = True
                actual = actual.next
    # Para ordenar TEXTO A-Z es el mismo metodo ascendente:
    # los strings tambien se comparan con > y <  (ojo: las mayusculas van primero)


# =====================================================================
# 2. LISTA CIRCULAR
# =====================================================================
class ListaCircular:
    def __init__(self):
        self.head = None

    def agregar_al_final(self, data):
        nuevo = Nodo(data)
        if self.head is None:
            self.head = nuevo
            nuevo.next = nuevo               # se apunta a si mismo
            return
        ultimo = self.head
        while ultimo.next is not self.head:  # el ultimo apunta a head
            ultimo = ultimo.next
        ultimo.next = nuevo
        nuevo.next = self.head               # cerrar el circulo

    def length(self):
        if self.head is None:
            return 0
        contador = 1
        actual = self.head
        while actual.next is not self.head:
            actual = actual.next
            contador += 1
        return contador

    def imprimir(self):
        if self.head is None:
            print("(lista vacia)")
            return
        actual = self.head
        texto = ""
        while True:
            texto += str(actual.data) + " --> "
            actual = actual.next
            if actual is self.head:          # dio la vuelta: parar
                break
        print(texto + "(vuelve a " + str(self.head.data) + ")")

    # ---------------- ELIMINAR ----------------
    def eliminar_dato(self, dato):
        if self.head is None:                        # 1) vacia
            print("La lista esta vacia")
            return
        if self.head.next is self.head:              # 2) un solo nodo
            if self.head.data == dato:
                self.head = None
            else:
                print(f"El dato {dato} no existe")
            return
        if self.head.data == dato:                   # 3) es el head: el ultimo debe apuntar al nuevo head
            ultimo = self.head
            while ultimo.next is not self.head:
                ultimo = ultimo.next
            ultimo.next = self.head.next
            self.head = self.head.next
            return
        anterior = self.head                         # 4) cualquier otro (UNA sola vuelta)
        actual = self.head.next
        while actual is not self.head:
            if actual.data == dato:
                anterior.next = actual.next
                return
            anterior = actual
            actual = actual.next
        print(f"El dato {dato} no existe")

    # ---------------- ORDENAR (burbuja con length) ----------------
    def ordenar_ascendente(self):
        n = self.length()
        if n < 2:
            return
        for _ in range(n - 1):                       # n-1 pasadas
            actual = self.head
            for _ in range(n - 1):                   # n-1 comparaciones
                if actual.data > actual.next.data:
                    actual.data, actual.next.data = actual.next.data, actual.data
                actual = actual.next

    def ordenar_descendente(self):
        n = self.length()
        if n < 2:
            return
        for _ in range(n - 1):
            actual = self.head
            for _ in range(n - 1):
                if actual.data < actual.next.data:
                    actual.data, actual.next.data = actual.next.data, actual.data
                actual = actual.next


# =====================================================================
# 3. NODO CON UN ATRIBUTO DE TIPO LISTA
# =====================================================================
"""
IDEA: el DATO del nodo es un objeto (Estudiante) y ese objeto tiene un
atributo que es una LISTA de Python (sus notas).

    head --> [ Estudiante("Ana",  notas=[4.0, 3.5]) ] --> [ Estudiante("Luis", notas=[2.0]) ] --> None
                    nodo.data.notas  es la lista de Python

COMO SE ACCEDE (de afuera hacia adentro):
    nodo                      -> el nodo
    nodo.data                 -> el Estudiante
    nodo.data.nombre          -> "Ana"
    nodo.data.notas           -> [4.0, 3.5]          (una lista normal)
    nodo.data.notas.append(5) -> agrega una nota (metodos de lista de Python)
    nodo.data.notas[0]        -> 4.0

OJO (error clasico): NO uses  notas=[]  como valor por defecto en __init__
  def __init__(self, nombre, notas=[]):      # MAL: todos comparten la MISMA lista
  def __init__(self, nombre, notas=None):    # BIEN
      self.notas = notas if notas is not None else []
"""


class Estudiante:
    def __init__(self, nombre, notas=None):
        self.nombre = nombre
        self.notas = notas if notas is not None else []   # cada estudiante, su propia lista

    def promedio(self):
        if len(self.notas) == 0:             # evitar dividir entre cero
            return 0
        return sum(self.notas) / len(self.notas)

    def __str__(self):
        return f"{self.nombre} {self.notas}"


class ListaEstudiantes:
    def __init__(self):
        self.head = None

    def agregar_estudiante(self, nombre, notas=None):
        nuevo = Nodo(Estudiante(nombre, notas))
        if self.head is None:
            self.head = nuevo
            return
        actual = self.head
        while actual.next is not None:
            actual = actual.next
        actual.next = nuevo

    def imprimir(self):
        if self.head is None:
            print("(lista vacia)")
            return
        actual = self.head
        while actual is not None:
            print(f"  {actual.data}  promedio={actual.data.promedio():.2f}")
            actual = actual.next

    def buscar(self, nombre):
        """Devuelve el NODO del estudiante (o None si no existe)."""
        actual = self.head
        while actual is not None:
            if actual.data.nombre == nombre:
                return actual
            actual = actual.next
        return None

    def agregar_nota(self, nombre, nota):
        nodo = self.buscar(nombre)
        if nodo is None:
            print(f"El estudiante {nombre} no existe")
            return
        if not isinstance(nota, (int, float)) or isinstance(nota, bool) or not 0 <= nota <= 5:
            print(f"Nota invalida: {nota!r} (debe estar entre 0 y 5)")
            return
        nodo.data.notas.append(nota)                        # metodo de lista de Python

    def eliminar_nota(self, nombre, nota):
        nodo = self.buscar(nombre)
        if nodo is None:
            print(f"El estudiante {nombre} no existe")
            return
        if nota not in nodo.data.notas:
            print(f"{nombre} no tiene la nota {nota}")
            return
        nodo.data.notas.remove(nota)                        # elimina la primera aparicion

    def eliminar_estudiante(self, nombre):
        """Eliminar el NODO completo (igual que eliminar_dato, pero comparando el nombre)."""
        if self.head is None:
            print("La lista esta vacia")
            return
        if self.head.data.nombre == nombre:
            self.head = self.head.next
            return
        anterior = self.head
        actual = self.head.next
        while actual is not None:
            if actual.data.nombre == nombre:
                anterior.next = actual.next
                return
            anterior = actual
            actual = actual.next
        print(f"El estudiante {nombre} no existe")

    def ordenar_por_promedio(self):
        """Burbuja: se compara el PROMEDIO (calculado desde la lista de notas)."""
        if self.head is None or self.head.next is None:
            return
        cambio = True
        while cambio:
            cambio = False
            actual = self.head
            while actual.next is not None:
                if actual.data.promedio() < actual.next.data.promedio():   # mayor promedio primero
                    actual.data, actual.next.data = actual.next.data, actual.data
                    cambio = True
                actual = actual.next

    def mejor_nota_de_todos(self):
        """Recorrer la lista de nodos Y la lista de notas de cada uno (dos recorridos anidados)."""
        mejor = None
        actual = self.head
        while actual is not None:
            for nota in actual.data.notas:                  # for sobre la lista de Python
                if mejor is None or nota > mejor:
                    mejor = nota
            actual = actual.next
        return mejor


# =====================================================================
# EJEMPLOS
# =====================================================================
def armar_simple(*datos):
    lista = ListaSimple()
    for d in datos:
        lista.agregar_al_final(d)
    return lista


def armar_circular(*datos):
    lista = ListaCircular()
    for d in datos:
        lista.agregar_al_final(d)
    return lista


def mostrar(titulo, lista, accion):
    print(f"\n{titulo}")
    print("  Antes:   ", end="")
    lista.imprimir()
    accion(lista)
    print("  Despues: ", end="")
    lista.imprimir()


if __name__ == "__main__":
    print("=" * 62)
    print("1. ELIMINAR - LISTA SIMPLE")
    print("=" * 62)
    mostrar("Eliminar el primero", armar_simple(1, 2, 3), lambda l: l.eliminar_inicio())
    mostrar("Eliminar el ultimo", armar_simple(1, 2, 3), lambda l: l.eliminar_final())
    mostrar("Eliminar un dato del medio (el 2)", armar_simple(1, 2, 3), lambda l: l.eliminar_dato(2))
    mostrar("Eliminar el dato que esta de primero (el 1)", armar_simple(1, 2, 3), lambda l: l.eliminar_dato(1))
    mostrar("Eliminar el dato que esta de ultimo (el 3)", armar_simple(1, 2, 3), lambda l: l.eliminar_dato(3))
    mostrar("Eliminar la posicion 1", armar_simple("a", "b", "c"), lambda l: l.eliminar_posicion(1))
    mostrar("Dato inexistente", armar_simple(1, 2, 3), lambda l: l.eliminar_dato(99))
    mostrar("Lista vacia", armar_simple(), lambda l: l.eliminar_dato(1))
    mostrar("Un solo nodo (eliminar final)", armar_simple(7), lambda l: l.eliminar_final())
    mostrar("Posicion fuera de rango", armar_simple(1, 2), lambda l: l.eliminar_posicion(5))

    print("\n" + "=" * 62)
    print("2. ORDENAR - LISTA SIMPLE")
    print("=" * 62)
    mostrar("Ascendente (numeros)", armar_simple(4, 1, 5, 3, 2), lambda l: l.ordenar_ascendente())
    mostrar("Descendente (numeros)", armar_simple(4, 1, 5, 3, 2), lambda l: l.ordenar_descendente())
    mostrar("Texto A-Z", armar_simple("pera", "mango", "uva", "banano"), lambda l: l.ordenar_ascendente())
    mostrar("Lista vacia", armar_simple(), lambda l: l.ordenar_ascendente())
    mostrar("Un solo dato", armar_simple(9), lambda l: l.ordenar_ascendente())

    print("\n" + "=" * 62)
    print("3. ELIMINAR Y ORDENAR - LISTA CIRCULAR")
    print("=" * 62)
    mostrar("Eliminar el head (el 1)", armar_circular(1, 2, 3, 4), lambda l: l.eliminar_dato(1))
    mostrar("Eliminar el ultimo (el 4)", armar_circular(1, 2, 3, 4), lambda l: l.eliminar_dato(4))
    mostrar("Eliminar uno del medio (el 3)", armar_circular(1, 2, 3, 4), lambda l: l.eliminar_dato(3))
    mostrar("Dato inexistente (no se cuelga)", armar_circular(1, 2, 3), lambda l: l.eliminar_dato(99))
    mostrar("Un solo nodo", armar_circular(5), lambda l: l.eliminar_dato(5))
    mostrar("Lista vacia", armar_circular(), lambda l: l.eliminar_dato(1))
    mostrar("Ordenar ascendente", armar_circular(9, 3, 7, 1, 5), lambda l: l.ordenar_ascendente())
    mostrar("Ordenar descendente", armar_circular(9, 3, 7, 1, 5), lambda l: l.ordenar_descendente())

    print("\n" + "=" * 62)
    print("4. NODO CON UN ATRIBUTO DE TIPO LISTA (estudiante con notas)")
    print("=" * 62)
    curso = ListaEstudiantes()
    curso.agregar_estudiante("Ana", [4.0, 3.5])
    curso.agregar_estudiante("Luis", [2.0])
    curso.agregar_estudiante("Marta")                      # sin notas: lista propia y vacia
    print("\nLista inicial:")
    curso.imprimir()

    print("\nAgregar notas (Marta recibe 5.0 y 4.5, Luis recibe 3.0):")
    curso.agregar_nota("Marta", 5.0)
    curso.agregar_nota("Marta", 4.5)
    curso.agregar_nota("Luis", 3.0)
    curso.imprimir()

    print("\nErrores controlados:")
    curso.agregar_nota("Zoe", 4.0)                          # estudiante inexistente
    curso.agregar_nota("Ana", 9)                            # nota fuera de rango
    curso.agregar_nota("Ana", "cinco")                      # nota que no es numero
    curso.eliminar_nota("Ana", 1.0)                         # nota que no tiene

    print("\nEliminar la nota 3.5 de Ana:")
    curso.eliminar_nota("Ana", 3.5)
    curso.imprimir()

    print("\nOrdenar por promedio (mayor primero):")
    curso.ordenar_por_promedio()
    curso.imprimir()

    print(f"\nMejor nota de todos: {curso.mejor_nota_de_todos()}")

    print("\nAcceder directo a la lista de un nodo:")
    nodo_luis = curso.buscar("Luis")
    print(f"  nodo_luis.data.notas = {nodo_luis.data.notas}")
    print(f"  Primera nota de Luis = {nodo_luis.data.notas[0]}")

    print("\nEliminar al estudiante Luis (el nodo completo):")
    curso.eliminar_estudiante("Luis")
    curso.imprimir()

    print("\nPrueba del error clasico: cada estudiante tiene su PROPIA lista")
    a, b = Estudiante("A"), Estudiante("B")
    a.notas.append(5.0)
    print(f"  A.notas = {a.notas}   B.notas = {b.notas}   (B sigue vacia: correcto)")
