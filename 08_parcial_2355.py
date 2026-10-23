# =====================================================
# II PARCIAL 2355
#  Parte 1: Lista enlazada -> eliminar repetidos y secuencia
#  Parte 2: Lista circular -> juego de la ruleta
# =====================================================
import random


# ---------------- PARTE 1: LISTA ENLAZADA ----------------

def es_numero(dato):
    # True si es int o float (y no un booleano ni un texto)
    return isinstance(dato, (int, float)) and not isinstance(dato, bool)


class Nodo:
    def __init__(self, data = None, next = None):
        self.data = data
        self.next = next


class Lista_enlazada:
    def __init__(self):
        self.head = None

    # ¿La lista está vacía?
    def is_empty(self):
        return self.head == None

    # Agregar un dato al inicio
    def agregar_al_inicio(self, data):
        self.head = Nodo(data=data, next=self.head)

    # Agregar un dato al final
    def agregar_al_final(self, data):
        if not self.head:
            self.head = Nodo(data=data)
            return
        temporal = self.head
        while temporal.next:
            temporal = temporal.next
        temporal.next = Nodo(data=data)

    # Agregar al final, pero solo si es un número (validación de dato errado)
    def agregar_numero(self, data):
        if not es_numero(data):
            print("Dato errado, solo se permiten números:", data)
            return
        self.agregar_al_final(data)

    # Eliminar el primer nodo que tenga ese dato
    def delete_node(self, key):
        if self.is_empty():
            print("La lista está vacía")
            return
        actual = self.head
        previo = None
        while actual and actual.data != key:
            previo = actual
            actual = actual.next
        if actual is None:
            print("El dato", key, "no existe en la lista")
            return
        if previo is None:          # era la cabeza
            self.head = actual.next
        else:
            previo.next = actual.next

    # ¿Existe el valor en la lista? (True / False)
    def buscar(self, valor):
        actual = self.head
        while actual != None:
            if actual.data == valor:
                return True
            actual = actual.next
        return False

    # Posición (0, 1, 2...) del valor. Devuelve -1 si no existe
    def indice_de(self, valor):
        actual = self.head
        indice = 0
        while actual != None:
            if actual.data == valor:
                return indice
            actual = actual.next
            indice += 1
        return -1

    # Insertar un dato en la posición 'indice' (0 = al inicio)
    def insertar_en(self, indice, data):
        if indice <= 0 or self.head is None:
            self.agregar_al_inicio(data)
            return
        actual = self.head
        for i in range(indice - 1):
            if actual.next == None:
                break
            actual = actual.next
        actual.next = Nodo(data=data, next=actual.next)

    # Cuántas veces aparece un valor
    def contar(self, valor):
        veces = 0
        actual = self.head
        while actual != None:
            if actual.data == valor:
                veces += 1
            actual = actual.next
        return veces

    # Cuántos nodos tiene la lista
    def longitud(self):
        cantidad = 0
        actual = self.head
        while actual != None:
            cantidad += 1
            actual = actual.next
        return cantidad

    # Promedio de los datos (lista numérica). Devuelve 0 si está vacía
    def promedio(self):
        suma = 0
        cantidad = 0
        actual = self.head
        while actual != None:
            suma += actual.data
            cantidad += 1
            actual = actual.next
        if cantidad == 0:
            return 0
        return suma / cantidad

    # Dato del último nodo
    def get_last_node(self):
        if self.is_empty():
            return None
        temp = self.head
        while temp.next is not None:
            temp = temp.next
        return temp.data

    # Imprimir la lista
    def print_list(self):
        if self.is_empty():
            print("La lista está vacía")
            return
        node = self.head
        while node != None:
            print(node.data, end=" --> ")
            node = node.next
        print("None")

    # ===== PARCIAL 2355 - 1a =====
    # Elimina los datos con más de 2 repeticiones y deja solo uno
    def eliminar_repetidos(self):
        if self.is_empty():
            print("La lista está vacía")
            return
        eliminados = 0
        actual = self.head
        while actual != None:
            if self.contar(actual.data) > 2:
                # se borran las apariciones que están DESPUÉS de este nodo
                anterior = actual
                while anterior.next != None:
                    if anterior.next.data == actual.data:
                        anterior.next = anterior.next.next
                        eliminados += 1
                    else:
                        anterior = anterior.next
            actual = actual.next
        if eliminados == 0:
            print("No hay datos con más de 2 repeticiones")

    # ===== PARCIAL 2355 - 1b =====
    # Elimina una secuencia ascendente (datos contiguos que suben de 1 en 1)
    def eliminar_secuencia(self):
        if self.is_empty():
            print("La lista está vacía")
            return
        encontrada = False
        anterior = None
        actual = self.head
        while actual != None:
            fin = actual
            while fin.next != None and fin.next.data == fin.data + 1:
                fin = fin.next
            if fin is not actual:                # hay secuencia (2 o más nodos)
                encontrada = True
                if anterior == None:             # empieza en la cabeza
                    self.head = fin.next
                else:
                    anterior.next = fin.next
                actual = fin.next
            else:
                anterior = actual
                actual = actual.next
        if not encontrada:
            print("No hay secuencias ascendentes")


def ejemplos_lista_enlazada():
    print("===== 1a: eliminar repetidos =====")

    print("\n-- Lista vacía --")
    vacia = Lista_enlazada()
    vacia.eliminar_repetidos()

    print("\n-- Dato errado --")
    vacia.agregar_numero("hola")

    print("\n-- Ejemplo del enunciado (4-8-32-8-7-8-94) --")
    l1 = Lista_enlazada()
    for d in [4, 8, 32, 8, 7, 8, 94]:
        l1.agregar_numero(d)
    l1.print_list()
    l1.eliminar_repetidos()
    l1.print_list()

    print("\n-- Repetido al inicio y al final (5-1-5-2-5) --")
    l2 = Lista_enlazada()
    for d in [5, 1, 5, 2, 5]:
        l2.agregar_numero(d)
    l2.eliminar_repetidos()
    l2.print_list()

    print("\n-- Sin datos con más de 2 repeticiones (3-3-9) --")
    l3 = Lista_enlazada()
    for d in [3, 3, 9]:
        l3.agregar_numero(d)
    l3.eliminar_repetidos()
    l3.print_list()

    print("\n===== 1b: eliminar secuencia ascendente =====")

    print("\n-- Lista vacía --")
    vacia.eliminar_secuencia()

    print("\n-- Ejemplo del enunciado (4-8-32-6-7-8-94) --")
    l4 = Lista_enlazada()
    for d in [4, 8, 32, 6, 7, 8, 94]:
        l4.agregar_numero(d)
    l4.print_list()
    l4.eliminar_secuencia()
    l4.print_list()

    print("\n-- Secuencia al inicio y al final (1-2-50-9-10) --")
    l5 = Lista_enlazada()
    for d in [1, 2, 50, 9, 10]:
        l5.agregar_numero(d)
    l5.eliminar_secuencia()
    l5.print_list()

    print("\n-- Sin secuencias (5-20-40) --")
    l6 = Lista_enlazada()
    for d in [5, 20, 40]:
        l6.agregar_numero(d)
    l6.eliminar_secuencia()
    l6.print_list()


# ---------------- PARTE 2: LISTA CIRCULAR ----------------

class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None


class Lista_Circular(object):

    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    # Cuántos nodos tiene (se detiene al volver a la cabeza)
    def length(self):
        cur = self.head
        count = 0
        while cur is not None:
            count += 1
            if cur.next == self.head:
                break
            else:
                cur = cur.next
        return count

    # Agregar al inicio
    def add_first(self, data):
        node = Node(data)
        if self.is_empty():
            self.head = node
            node.next = self.head
        else:
            cur = self.head
            while cur.next is not self.head:   # busca la cola
                cur = cur.next
            cur.next = node                    # la cola apunta al nuevo
            node.next = self.head              # el nuevo apunta a la cabeza vieja
            self.head = node                   # el nuevo es la cabeza

    # Agregar al final
    def add_last(self, data):
        node = Node(data)
        if self.is_empty():
            self.head = node
            node.next = self.head
        else:
            cur = self.head
            while cur.next is not self.head:   # busca la cola
                cur = cur.next
            cur.next = node                    # la cola apunta al nuevo
            node.next = self.head              # el nuevo apunta a la cabeza

    # Eliminar el nodo con ese dato
    def remove_node(self, data):
        if self.is_empty():
            print("La lista está vacía")
            return
        if self.length() == 1:                 # único nodo
            if self.head.data == data:
                self.head = None
            else:
                print("El dato", data, "no existe en la lista")
            return
        if data == self.head.data:             # se elimina la cabeza
            cur = self.head
            while cur.next != self.head:
                cur = cur.next
            cur.next = self.head.next
            self.head = self.head.next
        else:
            pre = self.head
            cur = self.head.next
            while cur != self.head and cur.data != data:
                pre = cur
                cur = cur.next
            if cur == self.head:               # dio la vuelta completa sin encontrarlo
                print("El dato", data, "no existe en la lista")
                return
            pre.next = cur.next

    # ¿Existe el dato? (True / False)
    def buscar(self, data):
        if self.is_empty():
            return False
        cur = self.head
        while True:
            if cur.data == data:
                return True
            cur = cur.next
            if cur == self.head:
                return False

    # Dato que está en la casilla 'posicion' (1, 2, 3...)
    def obtener(self, posicion):
        cur = self.head
        for i in range(posicion - 1):
            cur = cur.next
        return cur.data

    # Mover un dato al final de la lista
    def mover_al_final(self, data):
        if not self.buscar(data):
            print("El dato", data, "no existe en la lista")
            return
        self.remove_node(data)
        self.add_last(data)

    # Imprimir todos los nodos (una vuelta completa)
    def imprimir(self):
        if self.is_empty():
            print("La lista está vacía")
            return
        cur = self.head
        while True:
            print(cur.data, end=" --> ")
            cur = cur.next
            if cur == self.head:
                break
        print("(vuelve a", self.head.data, ")")


def jugar_ruleta():
    # a. Lista circular de jugadores y lista circular de premios (10 casillas)
    jugadores = Lista_Circular()
    for nombre in ["Ana", "Luis", "Marta"]:
        jugadores.add_last(nombre)

    premios = Lista_Circular()
    for p in ["Un viaje a San Andrés", "Lanza de nuevo", "Una pizza",
              "Un celular", "Entradas al cine", "Eliminado del juego",
              "Un libro", "Bono de $100.000", "Un televisor", "Un peluche"]:
        premios.add_last(p)

    posiciones = {"Ana": 0, "Luis": 0, "Marta": 0}    # última casilla (0 = aún no lanza)
    turno = jugadores.head

    while True:
        if jugadores.length() == 1:
            print("\nQueda un solo jugador. El ganador es:", turno.data)
            break

        # b. Menú y jugador en turno
        print("\nTurno de:", turno.data)
        print("1. Lanzar la ruleta")
        print("2. Salir")
        opcion = input("Elija una opción: ")

        if opcion == "2":
            print("Juego terminado")
            break
        elif opcion != "1":
            print("Opción no válida, intente de nuevo")
            continue

        # d. Nueva casilla: última posición + número aleatorio (si pasa de 10, da la vuelta)
        aleatorio = random.randint(1, 10)
        nueva = posiciones[turno.data] + aleatorio
        if nueva > 10:
            nueva = nueva - 10
        posiciones[turno.data] = nueva
        premio = premios.obtener(nueva)

        # e. Mostrar el premio
        print("Salió el", aleatorio, "-> casilla", nueva)
        print(turno.data, "obtuvo:", premio)

        # c. Casillas especiales
        if premio == "Lanza de nuevo":
            print(turno.data, "lanza de nuevo")
            continue                              # el turno no cambia
        elif premio == "Eliminado del juego":
            siguiente = turno.next                # se guarda antes de borrar
            jugadores.remove_node(turno.data)
            print(turno.data, "fue eliminado del juego")
            turno = siguiente
        else:
            turno = turno.next


# ---------------- EJECUCIÓN ----------------
ejemplos_lista_enlazada()
print("\n===== Juego de la ruleta =====")
jugar_ruleta()
