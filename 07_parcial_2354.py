# =====================================================
# II PARCIAL 2354
#  Parte 1: Lista enlazada -> método agregar (según el signo)
#  Parte 2: Lista circular -> juego de dados
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

    # ===== PARCIAL 2354 - ejercicio 1 =====
    # Inserta un dato según su signo y devuelve el promedio de la lista
    def agregar(self, data):
        # d. Si es un texto (dato errado): no se inserta
        if not es_numero(data):
            print("Solo se permiten números, no se insertó:", data)
            return None

        # e. Si ya existe: no se inserta
        if self.buscar(data):
            print("El número", data, "ya está en la lista, no se insertó")
            return None

        nuevo = Nodo(data)

        if data < 0:                                   # a. negativo: al inicio
            nuevo.next = self.head
            self.head = nuevo

        elif data > 0:                                 # b. positivo: al final
            if self.head is None:
                self.head = nuevo
            else:
                actual = self.head
                while actual.next is not None:
                    actual = actual.next
                actual.next = nuevo

        else:                                          # c. cero: entre negativos y positivos
            if self.head is None or self.head.data >= 0:
                # lista vacía o sin negativos: el cero va de primero
                nuevo.next = self.head
                self.head = nuevo
            else:
                # se avanza mientras el SIGUIENTE sea negativo
                actual = self.head
                while actual.next is not None and actual.next.data < 0:
                    actual = actual.next
                nuevo.next = actual.next               # si solo hay negativos, queda al final
                actual.next = nuevo

        # f. Mostrar la lista final y retornar el promedio
        self.print_list()
        return self.promedio()


def ejemplos_agregar():
    print("===== Método agregar =====")
    lista = Lista_enlazada()

    print("\n-- Texto (dato errado) --")
    print("Promedio:", lista.agregar("Hola"))

    print("\n-- Cero en lista vacía --")
    print("Promedio:", lista.agregar(0))

    print("\n-- Positivo (al final) --")
    print("Promedio:", lista.agregar(5))

    print("\n-- Negativo (al inicio) --")
    print("Promedio:", lista.agregar(-3))

    print("\n-- Repetido --")
    print("Promedio:", lista.agregar(5))

    print("\n-- Otro negativo --")
    print("Promedio:", lista.agregar(-7))

    print("\n-- Cero con negativos y positivos --")
    lista2 = Lista_enlazada()
    for d in [-2, 6, -9, 4]:
        lista2.agregar(d)
    print("Promedio:", lista2.agregar(0))

    print("\n-- Cero con solo negativos (queda al final) --")
    lista3 = Lista_enlazada()
    lista3.agregar(-1)
    lista3.agregar(-5)
    print("Promedio:", lista3.agregar(0))

    print("\n-- Cero con solo positivos (queda al inicio) --")
    lista4 = Lista_enlazada()
    lista4.agregar(3)
    lista4.agregar(8)
    print("Promedio:", lista4.agregar(0))


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


def jugar_dados():
    # a. Lista circular con 5 jugadores
    nombres = ["Ana", "Luis", "Marta", "Pedro", "Sofia"]
    jugadores = Lista_Circular()
    acumulado = {}                    # d. acumulado de cada jugador
    for n in nombres:
        jugadores.add_last(n)
        acumulado[n] = 0

    eliminados = []
    turno = jugadores.head            # nodo del jugador que tiene el turno

    while True:
        # Si solo queda un jugador, es el ganador
        if jugadores.length() == 1:
            print("\nSolo queda un jugador. El ganador es:", turno.data)
            break

        nombre = turno.data
        print("\nTurno de:", nombre)
        print("1. Lanzar los dados")
        print("2. Finalizar el juego")
        opcion = input("Elija una opción: ")

        # e. Finalizar: gana el que tenga menos puntos acumulados
        if opcion == "2":
            print("\nJuego finalizado. Acumulado de cada jugador:")
            menor = nombres[0]
            for n in nombres:
                print(n, ":", acumulado[n])
                if acumulado[n] < acumulado[menor]:
                    menor = n
            print("Gana el que tiene menos puntos:", menor)
            break
        elif opcion != "1":
            print("Opción no válida, intente de nuevo")
            continue

        # b. Lanzamiento con 2 dados
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        suma = d1 + d2
        acumulado[nombre] += suma
        print(nombre, "sacó", d1, "y", d2, "(suma", suma, "). Acumulado:", acumulado[nombre])

        if d1 == d2:                                   # dobles: gana
            print("¡Sacó dobles! El ganador es:", nombre)
            break
        elif suma >= 10:                               # se elimina al jugador
            siguiente = turno.next                     # se guarda antes de borrar
            jugadores.remove_node(nombre)
            eliminados.append(nombre)
            print(nombre, "fue eliminado del juego")
            turno = siguiente
        elif suma == 7:                                # c. se mueve al final
            siguiente = turno.next
            jugadores.mover_al_final(nombre)
            print(nombre, "se mueve al final de la lista")
            turno = siguiente
        else:
            turno = turno.next

    print("\nJugadores eliminados:", eliminados)


# ---------------- EJECUCIÓN ----------------
ejemplos_agregar()
print("\n===== Juego de dados =====")
jugar_dados()
