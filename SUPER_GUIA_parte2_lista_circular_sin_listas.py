"""
=====================================================================
SUPER GUIA - ESTRUCTURAS DE DATOS 1
PARTE 2: LISTA CIRCULAR + JUEGOS POR TURNOS + MENUS
=====================================================================

COMO USAR ESTE ARCHIVO
  Igual que la Parte 1: lee los conceptos una vez, y en el parcial copia el
  metodo (o la variante) que necesites. Al ejecutarlo corre pruebas con assert.

INDICE
  1. Conceptos de la lista circular
  2. Los 5 patrones de recorrido circular
  3. Clase Lista_circular
       A. Basicos (length, ultimo, a_lista, nodo_en, avanzar...)
       B. Agregar / insertar
       C. Buscar y consultar
       D. Filtrar
       E. Eliminar (por dato, por nodo, por condicion, duplicados)
       F. Ordenar
       G. Mover (al final, al inicio, N posiciones, rotar, invertir)
       H. Ayudas para juegos (ganador por menor/mayor, recorrido seguro)
  4. Plantilla de juego por turnos (eliminar, mover al final, acumular)
  5. Plantilla de menu
  6. Pruebas automaticas
"""

import random


# =====================================================================
# 1. CONCEPTOS DE LA LISTA CIRCULAR
# =====================================================================
"""
    head --> [A] --> [B] --> [C] --+
              ^                    |
              +--------------------+      el ultimo apunta a head

REGLA DE ORO
    En la circular NO existe None. Si recorres con  while actual is not None
    el programa NUNCA termina. Se para cuando se da la vuelta: actual is head.

ESTADOS ESPECIALES (pruebalos siempre)
    Vacia ............ head is None
    Un solo nodo ..... nodo.next is nodo   (se apunta a si mismo)
    Dos o mas ........ caso normal

EL ULTIMO NODO
    Es el que cumple  nodo.next is self.head.
    "Mover al final" = dejarlo justo antes de head.

CUANDO CAMBIA HEAD
    Al eliminar el head, al mover el head, al agregar al inicio.
    Cualquier codigo que dependa de 'actual is self.head' para PARAR se
    rompe si head cambia a mitad del recorrido. Por eso, si vas a eliminar
    o mover nodos mientras recorres, cuenta los nodos antes (n = length())
    y usa un for de n visitas (PATRON C3).

VENTAJA: se puede avanzar para siempre sin llegar a None. Es perfecta para
    turnos de juegos, ruletas, tableros (monopolio) y rondas.
"""


# =====================================================================
# 2. LOS 5 PATRONES DE RECORRIDO CIRCULAR
# =====================================================================
"""
PATRON C1 - UNA VUELTA (do-while: primero hacer, luego preguntar)
    if self.head is None:
        return
    actual = self.head
    while True:
        ...usar actual.data...
        actual = actual.next
        if actual is self.head:
            break

PATRON C2 - PARAR EN EL ULTIMO NODO
    actual = self.head
    while actual.next is not self.head:
        actual = actual.next
    # aqui actual es el ultimo

PATRON C3 - EXACTAMENTE n VISITAS (la lista cambia mientras recorres)
    n = self.length()
    actual = self.head
    for _ in range(n):
        siguiente = actual.next        # guardar ANTES de eliminar/mover
        ...eliminar o mover actual...
        actual = siguiente

PATRON C4 - TURNOS SIN FIN (no hay vueltas que contar)
    turno = self.head
    while hay_juego:
        ...jugar con turno...
        turno = turno.next             # al llegar al final vuelve solo al inicio

PATRON C5 - BUSCAR EN UNA VUELTA (no dar mas de una)
    actual = self.head
    while True:
        if actual.data == buscado:
            return actual
        actual = actual.next
        if actual is self.head:        # dio la vuelta y no estaba
            return None
"""


# =====================================================================
# FUNCIONES AUXILIARES
# =====================================================================
def _identidad(x):
    return x


def es_numero(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def es_entero(x):
    return isinstance(x, int) and not isinstance(x, bool)


def clave_mixta(x):
    """Numeros primero (menor a mayor) y luego textos (a-z). Para listas mezcladas."""
    if isinstance(x, str):
        return (1, x.lower())
    return (0, x)


def pedir_entero(leer, mensaje, minimo=None, maximo=None):
    """Pide un entero hasta que sea valido. 'leer' es input (parametro para poder probar)."""
    while True:
        texto = leer(mensaje)
        try:
            n = int(texto)
        except ValueError:
            print("  Entrada invalida: escribe un numero entero.")
            continue
        if minimo is not None and n < minimo:
            print(f"  Debe ser mayor o igual a {minimo}.")
            continue
        if maximo is not None and n > maximo:
            print(f"  Debe ser menor o igual a {maximo}.")
            continue
        return n


def lanzar_dado(caras=6):
    return random.randint(1, caras)


def lanzar_dos_dados():
    """Devuelve (dado1, dado2, suma, es_doble)."""
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    return d1, d2, d1 + d2, d1 == d2


# =====================================================================
# 3. CLASES
# =====================================================================
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class Jugador:
    """Dato de ejemplo para juegos: nombre + acumulado de puntos."""
    def __init__(self, nombre, acumulado=0):
        self.nombre = nombre
        self.acumulado = acumulado

    def __str__(self):
        return f"{self.nombre}({self.acumulado})"

    __repr__ = __str__


class Lista_circular:
    def __init__(self):
        self.head = None

    # =================================================================
    # A. BASICOS
    # =================================================================
    def is_empty(self):
        return self.head is None

    def length(self):
        if self.head is None:
            return 0
        actual = self.head
        contador = 1                                   # head ya cuenta
        while actual.next is not self.head:
            actual = actual.next
            contador += 1
        return contador

    def ultimo(self):
        """Devuelve el NODO ultimo (el que apunta a head)."""
        if self.head is None:
            return None
        actual = self.head
        while actual.next is not self.head:            # PATRON C2
            actual = actual.next
        return actual

    def mostrar_datos(self):
        """Muestra una vuelta del circulo sin crear una lista de Python."""
        if self.head is None:
            print()
            return
        actual = self.head
        while True:
            print(actual.data, end=" ")
            actual = actual.next
            if actual is self.head:
                break
        print()

    @classmethod
    def desde_lista(cls, datos):
        lista = cls()
        cola = None
        for dato in datos:
            nuevo = Node(dato)
            if cola is None:
                lista.head = nuevo
            else:
                cola.next = nuevo
            cola = nuevo
        if cola is not None:
            cola.next = lista.head                     # cerrar el circulo
        return lista

    def copiar(self):
        copia = Lista_circular()
        actual = self.head
        if actual is None:
            return copia
        while True:
            copia.agregar_al_final(actual.data)
            actual = actual.next
            if actual is self.head:
                break
        return copia

    def vaciar(self):
        self.head = None

    def __str__(self):
        if self.head is None:
            return "(lista vacia)"
        texto = ""
        actual = self.head
        while True:
            texto += str(actual.data) + " --> "
            actual = actual.next
            if actual is self.head:
                break
        return texto + f"(vuelve a {self.head.data})"

    def imprimir(self):
        print(self)

    def recorrer(self, accion):
        """PATRON C1 como metodo: aplica accion(dato) una vuelta. NO elimina/mueve nodos."""
        if self.head is None:
            return
        actual = self.head
        while True:
            accion(actual.data)
            actual = actual.next
            if actual is self.head:
                break

    def recorrer_vueltas(self, vueltas, accion):
        """Da 'vueltas' vueltas completas (n * vueltas visitas)."""
        n = self.length()
        actual = self.head
        for _ in range(n * vueltas):
            accion(actual.data)
            actual = actual.next

    def nodo_en(self, indice):
        """
        Nodo en la posicion 'indice'. Es CIRCULAR: si indice >= length, da vueltas
        (indice 7 en una lista de 5 = indice 2).
        """
        if self.head is None:
            return None
        actual = self.head
        for _ in range(indice % self.length()):
            actual = actual.next
        return actual

    def numero_de_nodo(self, nodo):
        """Posicion (1, 2, 3...) del nodo; 0 si no esta. Util para mostrar 'casilla #8'."""
        if self.head is None:
            return 0
        actual = self.head
        numero = 1
        while True:
            if actual is nodo:
                return numero
            actual = actual.next
            numero += 1
            if actual is self.head:
                return 0

    def avanzar(self, nodo, pasos):
        """
        Nodo al que llegas si avanzas 'pasos' desde 'nodo' (ruletas, dados, tableros).
        Si estabas en la casilla #3 y sacas 5, llegas a la #8 (y da la vuelta si hace falta).
        """
        for _ in range(pasos % self.length()):
            nodo = nodo.next
        return nodo

    def avanzar_contando_vueltas(self, nodo, pasos):
        """
        Igual que avanzar, pero tambien cuenta cuantas veces PASO por head ("Salida"
        del monopolio). Devuelve (nodo_final, veces_que_paso_por_head).
        """
        veces = 0
        for _ in range(pasos):
            nodo = nodo.next
            if nodo is self.head:
                veces += 1
        return nodo, veces

    # =================================================================
    # B. AGREGAR / INSERTAR
    # =================================================================
    def add_first(self, data):
        nuevo = Node(data)
        if self.head is None:
            self.head = nuevo
            nuevo.next = nuevo                         # se apunta a si mismo
            return
        ultimo = self.ultimo()
        nuevo.next = self.head                         # nuevo -> head viejo
        ultimo.next = nuevo                            # el ultimo -> nuevo
        self.head = nuevo                              # nuevo es el head

    def add_last(self, data):
        nuevo = Node(data)
        if self.head is None:
            self.head = nuevo
            nuevo.next = nuevo
            return
        ultimo = self.ultimo()
        ultimo.next = nuevo                            # ultimo -> nuevo
        nuevo.next = self.head                         # nuevo -> head (cierra el circulo)

    def add_sin_repetir(self, data, clave=None):
        if self.existe(data, clave):
            print(f"'{data}' ya existe, no se agrego.")
            return False
        self.add_last(data)
        return True

    def insert_node(self, index, data):
        """0 = inicio, length = final (el insert_node de clase, ya corregido)."""
        if index < 0 or index > self.length():
            print("Posicion de insercion incorrecta")
            return False
        if index == 0:
            self.add_first(data)
        elif index == self.length():
            self.add_last(data)
        else:
            anterior = self.nodo_en(index - 1)
            nuevo = Node(data)
            nuevo.next = anterior.next
            anterior.next = nuevo
        return True

    def insertar_despues_de(self, referencia, data, clave=None):
        k = clave or _identidad
        nodo = self.buscar_nodo(lambda d: k(d) == referencia)
        if nodo is None:
            print(f"No existe '{referencia}' en la lista.")
            return False
        nuevo = Node(data)
        nuevo.next = nodo.next
        nodo.next = nuevo
        return True

    def insertar_ordenado(self, data, clave=None, descendente=False):
        """Inserta manteniendo el orden (la lista ya debe estar ordenada igual)."""
        k = clave or _identidad

        def va_antes(a, b):
            return k(a) > k(b) if descendente else k(a) < k(b)

        if self.head is None or va_antes(data, self.head.data):
            self.add_first(data)
            return
        actual = self.head
        while actual.next is not self.head and not va_antes(data, actual.next.data):
            actual = actual.next
        nuevo = Node(data)
        nuevo.next = actual.next
        actual.next = nuevo

    # =================================================================
    # C. BUSCAR Y CONSULTAR
    # =================================================================
    def buscar_nodo(self, condicion):
        """Primer NODO que cumpla condicion(dato) en UNA vuelta, o None (PATRON C5)."""
        if self.head is None:
            return None
        actual = self.head
        while True:
            if condicion(actual.data):
                return actual
            actual = actual.next
            if actual is self.head:
                return None

    def posicion_de(self, data, clave=None):
        """Indice de la primera aparicion, o -1, recorriendo nodos."""
        k = clave or _identidad
        indice = 0
        actual = self.head
        if actual is None:
            return -1
        while True:
            if k(actual.data) == data:
                return indice
            actual = actual.next
            indice += 1
            if actual is self.head:
                break
        return -1

    def existe(self, data, clave=None):
        return self.posicion_de(data, clave) != -1

    def contar(self, data, clave=None):
        k = clave or _identidad
        contador = 0
        actual = self.head
        if actual is None:
            return 0
        while True:
            if k(actual.data) == data:
                contador += 1
            actual = actual.next
            if actual is self.head:
                break
        return contador

    def obtener(self, indice):
        """Dato en la posicion indice (sin dar vueltas): None si esta fuera de rango."""
        if indice < 0 or indice >= self.length():
            return None
        return self.nodo_en(indice).data

    def buscar_todos(self, condicion):
        """Devuelve una Lista_circular con los indices encontrados."""
        encontrados = Lista_circular()
        if self.head is None:
            return encontrados
        actual = self.head
        indice = 0
        while True:
            if condicion(actual.data):
                encontrados.agregar_al_final(indice)
            actual = actual.next
            indice += 1
            if actual is self.head:
                break
        return encontrados

    def promedio(self, clave=None):
        n = self.length()
        return None if n == 0 else self.suma(clave) / n

    def maximo(self, clave=None):
        nodo = self.nodo_con_mayor(clave)
        return None if nodo is None else nodo.data

    def minimo(self, clave=None):
        nodo = self.nodo_con_menor(clave)
        return None if nodo is None else nodo.data

    # =================================================================
    # D. FILTRAR  (devuelven una Lista_circular NUEVA)
    # =================================================================
    def filtrar(self, condicion):
        """Crea otra Lista_circular sin usar listas de Python."""
        nueva = Lista_circular()
        if self.head is None:
            return nueva
        actual = self.head
        while True:
            if condicion(actual.data):
                nueva.agregar_al_final(actual.data)
            actual = actual.next
            if actual is self.head:
                break
        return nueva

    def filtrar_por_nombre(self, nombre, clave=None, ignorar_mayusculas=True):
        k = clave or _identidad
        buscado = str(nombre).lower() if ignorar_mayusculas else str(nombre)

        def cumple(d):
            valor = str(k(d))
            return (valor.lower() if ignorar_mayusculas else valor) == buscado
        return self.filtrar(cumple)

    def filtrar_por_prefijo(self, prefijo, clave=None):
        k = clave or _identidad
        return self.filtrar(lambda d: str(k(d)).lower().startswith(str(prefijo).lower()))

    def filtrar_que_contiene(self, texto, clave=None):
        k = clave or _identidad
        return self.filtrar(lambda d: str(texto).lower() in str(k(d)).lower())

    def filtrar_por_rango(self, minimo, maximo, clave=None):
        k = clave or _identidad
        return self.filtrar(lambda d: es_numero(k(d)) and minimo <= k(d) <= maximo)

    # =================================================================
    # E. ELIMINAR
    # =================================================================
    def eliminar_nodo(self, nodo):
        """
        Elimina ESE nodo (por identidad, no por valor). Es el metodo mas seguro
        porque funciona aunque haya datos repetidos. Devuelve True/False.
        Casos: vacia, un solo nodo, head, cualquier otro.
        OJO: despues de eliminar un nodo, no sigas usandolo como parte de la lista;
        si estas recorriendo, guarda 'siguiente' ANTES (PATRON C3).
        """
        if self.head is None:
            return False
        if self.head.next is self.head:                # un solo nodo
            if self.head is nodo:
                self.head = None
                return True
            return False
        if self.head is nodo:                          # borrar el head
            ultimo = self.ultimo()
            ultimo.next = self.head.next               # el ultimo apunta al nuevo head
            self.head = self.head.next
            return True
        anterior = self.head                           # cualquier otro (una sola vuelta)
        actual = self.head.next
        while actual is not self.head:
            if actual is nodo:
                anterior.next = actual.next
                return True
            anterior = actual
            actual = actual.next
        return False

    def remove_node(self, data, clave=None):
        """Elimina la PRIMERA aparicion del dato (o de la clave, p.ej. el nombre)."""
        k = clave or _identidad
        nodo = self.buscar_nodo(lambda d: k(d) == data)
        if nodo is None:
            print(f"El dato '{data}' no existe en la lista.")
            return False
        return self.eliminar_nodo(nodo)

    def eliminar_primero(self):
        if self.head is None:
            print("La lista esta vacia.")
            return False
        return self.eliminar_nodo(self.head)

    def eliminar_ultimo(self):
        if self.head is None:
            print("La lista esta vacia.")
            return False
        return self.eliminar_nodo(self.ultimo())

    def eliminar_posicion(self, indice):
        if indice < 0 or indice >= self.length():
            print("Posicion invalida o fuera de rango.")
            return False
        return self.eliminar_nodo(self.nodo_en(indice))

    def eliminar_si(self, condicion):
        """
        Elimina TODOS los datos que cumplan condicion(dato). Devuelve cuantos elimino.
        Usa el PATRON C3 (n visitas + guardar siguiente), por eso es seguro.
        """
        if self.head is None:
            return 0
        eliminados = 0
        n = self.length()
        actual = self.head
        for _ in range(n):
            siguiente = actual.next
            if condicion(actual.data):
                self.eliminar_nodo(actual)
                eliminados += 1
            actual = siguiente
        return eliminados

    def eliminar_todas(self, data, clave=None):
        k = clave or _identidad
        return self.eliminar_si(lambda d: k(d) == data)

    def eliminar_duplicados(self):
        """Deja solo la primera aparicion usando dos recorridos de nodos."""
        eliminados = 0
        actual = self.head
        if actual is None:
            return 0
        n = self.length()
        for _ in range(n):
            siguiente_actual = actual.next
            revisar = actual.next
            while revisar is not actual:
                siguiente = revisar.next
                if revisar.data == actual.data:
                    self.eliminar_nodo(revisar)
                    eliminados += 1
                revisar = siguiente
                if self.head is None:
                    return eliminados
            actual = siguiente_actual
            if self.head is None:
                break
        return eliminados

    # =================================================================
    # F. ORDENAR
    # =================================================================
    """
    clave y descendente funcionan igual que en la Parte 1:
        clave=None | str.lower | lambda j: j.nombre | lambda j: (-j.acumulado, j.nombre)
    En la circular NO hay None para saber cuando parar, asi que se hacen
    exactamente n-1 pasadas con n-1 comparaciones (cada una sobre los datos).
    """

    def ordenar_datos(self, clave=None, descendente=False):
        n = self.length()
        if n < 2:
            return
        k = clave or _identidad
        for pasada in range(n - 1):
            actual = self.head
            cambiado = False
            for _ in range(n - 1 - pasada):
                siguiente = actual.next
                a, b = k(actual.data), k(siguiente.data)
                mal_orden = (a < b) if descendente else (a > b)
                if mal_orden:
                    actual.data, siguiente.data = siguiente.data, actual.data
                    cambiado = True
                actual = siguiente
            if not cambiado:
                break

    def ordenar_texto(self, descendente=False):
        self.ordenar_datos(clave=lambda x: str(x).lower(), descendente=descendente)

    def ordenar_por_insercion(self, clave=None, descendente=False):
        """Version segura para el parcial: ordena directamente los datos."""
        self.ordenar_datos(clave, descendente)

    def esta_ordenada(self, clave=None, descendente=False):
        k = clave or _identidad
        if self.head is None or self.head.next is self.head:
            return True
        actual = self.head
        while True:
            siguiente = actual.next
            a = k(actual.data)
            b = k(siguiente.data)
            if (a < b) if descendente else (a > b):
                return False
            actual = siguiente
            if actual.next is self.head:
                break
        return True

    # =================================================================
    # G. MOVER Y REORGANIZAR
    # =================================================================
    def _desconectar(self, nodo):
        """Saca el nodo del circulo (sin perderlo) y deja nodo.next = None."""
        if self.head is None:
            return
        if self.head.next is self.head:
            if self.head is nodo:
                self.head = None
            nodo.next = None
            return
        if nodo is self.head:
            ultimo = self.ultimo()
            ultimo.next = nodo.next
            self.head = nodo.next
        else:
            anterior = self.head
            while anterior.next is not nodo:
                anterior = anterior.next
            anterior.next = nodo.next
        nodo.next = None

    def _insertar_nodo_en(self, indice, nodo):
        """Mete un nodo ya desconectado para que quede en la posicion 'indice'."""
        if self.head is None:
            self.head = nodo
            nodo.next = nodo
            return
        if indice <= 0:
            ultimo = self.ultimo()
            nodo.next = self.head
            ultimo.next = nodo
            self.head = nodo
            return
        anterior = self.head
        for _ in range(min(indice - 1, self.length() - 1)):
            anterior = anterior.next
        nodo.next = anterior.next
        anterior.next = nodo

    def mover_nodo_al_final(self, nodo):
        """
        Mueve ESE nodo al final (justo antes de head).
        Vacia o un solo nodo: nada. Ya es el ultimo: nada.
        El HEAD se mueve al final con solo rotar el inicio (head = head.next).
        """
        if self.head is None or self.head.next is self.head:
            return
        if nodo.next is self.head:                     # ya es el ultimo
            return
        if nodo is self.head:                          # caso especial: head
            self.head = self.head.next
            return
        anterior = self.head                           # PASO 1: desconectar
        while anterior.next is not nodo:
            anterior = anterior.next
        anterior.next = nodo.next
        ultimo = self.ultimo()                         # PASO 2: llegar al ultimo
        ultimo.next = nodo                             # PASO 3: enganchar y cerrar
        nodo.next = self.head

    def mover_al_final(self, data, clave=None):
        k = clave or _identidad
        nodo = self.buscar_nodo(lambda d: k(d) == data)
        if nodo is None:
            print(f"El dato '{data}' no existe en la lista.")
            return False
        self.mover_nodo_al_final(nodo)
        return True

    def mover_nodo_al_inicio(self, nodo):
        """Lo deja como nuevo head (no es lo mismo que rotar: aqui el orden de los demas se conserva)."""
        if self.head is None or self.head.next is self.head or nodo is self.head:
            return
        self._desconectar(nodo)
        self._insertar_nodo_en(0, nodo)

    def mover_al_inicio(self, data, clave=None):
        k = clave or _identidad
        nodo = self.buscar_nodo(lambda d: k(d) == data)
        if nodo is None:
            print(f"El dato '{data}' no existe en la lista.")
            return False
        self.mover_nodo_al_inicio(nodo)
        return True

    def mover_posiciones(self, nombre, posiciones, direccion, limitar=True, envolver=False, clave=None):
        """
        Version circular de Mover_dato.
        direccion: "adelante" (hacia head) o "atras" (hacia el final).
        limitar=True : si se pasa, queda en el extremo.   limitar=False: no mueve y avisa.
        envolver=True: en vez de limitar, da la vuelta (usa % n): ideal si el enunciado
                       dice que la lista es circular y puede "salirse" por un lado.
        """
        k = clave or _identidad
        if self.head is None:
            print("La lista esta vacia.")
            return False
        if not es_entero(posiciones) or posiciones < 0:
            print("Las posiciones deben ser un entero mayor o igual a 0.")
            return False
        direccion = str(direccion).strip().lower()
        if direccion in ("adelante", "cabeza", "inicio", "head"):
            sentido = -1
        elif direccion in ("atras", "final", "fin", "cola"):
            sentido = 1
        else:
            print(f"Direccion '{direccion}' invalida (use 'adelante' o 'atras').")
            return False
        nodo = self.buscar_nodo(lambda d: k(d) == nombre)
        if nodo is None:
            print(f"El jugador '{nombre}' no existe en la lista.")
            return False
        n = self.length()
        indice = self.numero_de_nodo(nodo) - 1
        nuevo = indice + sentido * posiciones
        if envolver:
            nuevo %= n
        elif nuevo < 0 or nuevo > n - 1:
            if not limitar:
                print(f"No se puede mover {nombre}: se sale de la lista.")
                return False
            nuevo = 0 if nuevo < 0 else n - 1
        if nuevo == indice:
            return True
        self._desconectar(nodo)
        self._insertar_nodo_en(nuevo, nodo)
        return True

    def intercambiar_posiciones(self, i, j):
        n = self.length()
        if not (0 <= i < n and 0 <= j < n):
            print("Posiciones fuera de rango.")
            return False
        a, b = self.nodo_en(i), self.nodo_en(j)
        a.data, b.data = b.data, a.data
        return True

    def rotar(self, k=1):
        """
        Rotar en circular es TRIVIAL: solo cambias head. 1-2-3-4-5 rotar(2) -> 3-4-5-1-2.
        (En la lista simple habia que reconectar nodos.)
        """
        if self.head is not None:
            self.head = self.nodo_en(k)

    def invertir(self):
        n = self.length()
        if n < 2:
            return
        anterior = self.ultimo()
        actual = self.head
        for _ in range(n):
            siguiente = actual.next
            actual.next = anterior
            anterior = actual
            actual = siguiente
        self.head = anterior                           # el viejo ultimo es el nuevo head

    # =================================================================
    # H. AYUDAS PARA JUEGOS
    # =================================================================
    def nodo_con_menor(self, clave=None):
        """Nodo con la menor clave (None si vacia). 'Gana el que tenga menos puntos'."""
        if self.head is None:
            return None
        k = clave or _identidad
        mejor = self.head
        actual = self.head.next
        while actual is not self.head:
            if k(actual.data) < k(mejor.data):
                mejor = actual
            actual = actual.next
        return mejor

    def nodo_con_mayor(self, clave=None):
        if self.head is None:
            return None
        k = clave or _identidad
        mejor = self.head
        actual = self.head.next
        while actual is not self.head:
            if k(actual.data) > k(mejor.data):
                mejor = actual
            actual = actual.next
        return mejor

    def empatados_en_menor(self, clave=None):
        """Devuelve una Lista_circular con los datos empatados en el menor."""
        resultado = Lista_circular()
        nodo = self.nodo_con_menor(clave)
        if nodo is None:
            return resultado
        k = clave or _identidad
        minimo = k(nodo.data)
        actual = self.head
        while True:
            if k(actual.data) == minimo:
                resultado.agregar_al_final(actual.data)
            actual = actual.next
            if actual is self.head:
                break
        return resultado

    def empatados_en_mayor(self, clave=None):
        resultado = Lista_circular()
        nodo = self.nodo_con_mayor(clave)
        if nodo is None:
            return resultado
        k = clave or _identidad
        maximo = k(nodo.data)
        actual = self.head
        while True:
            if k(actual.data) == maximo:
                resultado.agregar_al_final(actual.data)
            actual = actual.next
            if actual is self.head:
                break
        return resultado

    def recorrer_seguro(self, accion):
        """
        Visita exactamente n nodos y le pasa cada NODO a accion(nodo).
        La accion PUEDE eliminar o mover ese nodo con self.eliminar_nodo(nodo) o
        self.mover_nodo_al_final(nodo): el recorrido no se pierde (PATRON C3).
        """
        if self.head is None:
            return
        n = self.length()
        actual = self.head
        for _ in range(n):
            siguiente = actual.next
            accion(actual)
            actual = siguiente


# =====================================================================
# 4. PLANTILLA DE JUEGO POR TURNOS
# =====================================================================
def ejemplo_juego_por_turnos(nombres, dado=lanzar_dado):
    """Plantilla sin listas: guarda jugadores y eliminados en listas circulares."""
    jugadores = Lista_circular()
    for nombre in nombres:
        jugadores.agregar_al_final(Jugador(nombre))
    eliminados = Lista_circular()
    turno = jugadores.head
    while jugadores.length() > 1:
        siguiente = turno.next
        jugador = turno.data
        tirada = dado()
        if tirada == 6:
            eliminados.agregar_al_final(jugador.nombre)
            jugadores.eliminar_nodo(turno)
        elif tirada == 1:
            jugadores.mover_nodo_al_final(turno)
        else:
            jugador.acumulado += tirada
        turno = siguiente
    if turno is None:
        return None, eliminados
    return turno.data.nombre, eliminados

# =====================================================================
# 5. PLANTILLA DE MENU
# =====================================================================
def menu_ejemplo(leer=input):
    """Menu que guarda las opciones elegidas en una Lista_circular."""
    elegidas = Lista_circular()
    while True:
        print("\n1. Lanzar  2. Ver estado  3. Salir")
        opcion = str(leer("Opcion: ")).strip()
        if opcion == "1":
            print("  (aqui lanzas)")
            elegidas.agregar_al_final(opcion)
        elif opcion == "2":
            print("  (aqui muestras el estado)")
            elegidas.agregar_al_final(opcion)
        elif opcion == "3":
            print("  Hasta luego")
            break
        else:
            print("  Opcion invalida, intenta de nuevo.")
    return elegidas


# =====================================================================


# =====================================================================
# NOTA PARA EL PARCIAL
# =====================================================================
# Esta version evita listas nativas de Python en los metodos de la
# estructura. Cuando un metodo necesita devolver varios resultados,
# devuelve otra Lista_circular.
