"""
=====================================================================
SUPER GUIA - ESTRUCTURAS DE DATOS 1
PARTE 1: CONCEPTOS + LISTA ENLAZADA SIMPLE (ARSENAL DE METODOS)
=====================================================================

COMO USAR ESTE ARCHIVO
  1. Lee las secciones 0, 1 y 2 una sola vez (estrategia, conceptos, patrones).
  2. En el parcial, busca en la seccion 3 el metodo (o la variante) que
     mejor encaje y copialo. Casi todos tienen variantes: por valor, por
     nombre (clave), ascendente/descendente, que devuelve lista nueva o
     modifica la misma.
  3. Ejecuta el archivo (python SUPER_GUIA_parte1_lista_simple.py).
     Al final hay pruebas con assert: si todo esta bien imprime OK.

INDICE
  0. Estrategia para resolver un parcial
  1. Conceptos clave
  2. Los 5 patrones de recorrido
  3. Clases Nodo y Lista_enlazada
       A. Basicos (length, imprimir, a_lista, desde_lista, copiar...)
       B. Agregar / insertar (inicio, final, posicion, antes/despues, ordenado, por signo)
       C. Buscar y consultar (existe, posicion, contar, suma, promedio, max, min...)
       D. Filtrar (por nombre, prefijo, contiene, rango, condicion cualquiera)
       E. Eliminar (inicio, final, dato, posicion, condicion, duplicados, exceso, secuencias)
       F. Ordenar (datos, nodos, por texto, por clave, varios criterios, mezcla de tipos)
       G. Mover y reorganizar (al final, al inicio, N posiciones, invertir, rotar...)
       H. Validaciones y entrada del usuario
       I. Datos aleatorios (numeros, contrasenas)
  4. Pruebas automaticas
"""

import random


# =====================================================================
# 0. ESTRATEGIA PARA RESOLVER UN PARCIAL
# =====================================================================
"""
PASO A PASO (hazlo siempre en este orden):

1. LEE TODO EL ENUNCIADO y subraya los verbos: agregar, eliminar, mover,
   filtrar, ordenar, buscar, retornar, mostrar. Cada verbo es un metodo
   (o una parte del metodo).

2. LISTA LOS CASOS ESPECIALES. Los parciales siempre los piden:
      - lista vacia
      - dato al inicio de la lista
      - dato al final de la lista
      - dato inexistente
      - dato errado por el usuario (string en vez de numero, numero negativo
        donde no corresponde, direccion invalida, etc.)
   Cada metodo debe EMPEZAR validando esto y avisando con un print.

3. DIBUJA EN PAPEL la lista antes y despues. Cada flecha que cambia es una
   linea de codigo que cambia un .next.

4. ESQUELETO DE CASI TODO METODO:
        validar  ->  buscar  ->  modificar enlaces  ->  mostrar / retornar

5. ORDEN DE LOS ENLACES: primero conecta lo nuevo, luego desconecta lo viejo.
   Si sueltas una referencia antes de guardarla, pierdes el resto de la lista.

6. ESCRIBE UN EJEMPLO (demo) QUE PRUEBE TODOS LOS CASOS. El enunciado lo exige:
   "se debe elaborar un ejemplo para todos los casos". Es parte de la nota.

7. SI EL ENUNCIADO ES AMBIGUO: elige la interpretacion mas razonable,
   escribela en un comentario y, si puedes, hazla un parametro.

8. PRUEBA SIEMPRE con 0, 1 y 2 nodos. Ahi se rompe el 90% del codigo.
"""


# =====================================================================
# 1. CONCEPTOS CLAVE
# =====================================================================
"""
NODO
    Una "caja" con dos cosas: el DATO y una FLECHA (next) al siguiente nodo.

        [ dato | next ] --> [ dato | next ] --> [ dato | None ]

HEAD (cabeza)
    La unica referencia que guarda la lista: apunta al primer nodo.
    Si pierdes head, pierdes toda la lista. Lista vacia: head is None.

LISTA SIMPLE vs CIRCULAR vs DOBLE
    Simple:    el ultimo nodo apunta a None.        Se recorre en un solo sentido.
    Circular:  el ultimo nodo apunta a head.        No hay None: cuidado con el bucle infinito.
    Doble:     cada nodo tiene next y prev (no entra en estos parciales).

DIFERENCIA CLAVE ENTRE  actual = actual.next  Y  actual.next = algo
    actual = actual.next   -> solo MUEVE tu puntero local. La lista no cambia.
    actual.next = algo     -> SI cambia la lista (reconecta una flecha).

is  vs  ==
    a is b    -> son EXACTAMENTE el mismo objeto (el mismo nodo en memoria).
    a == b    -> tienen el mismo valor.
    Para comparar NODOS usa 'is'. Para comparar DATOS usa '=='.
    (None siempre se compara con 'is None' / 'is not None'.)

COSTOS (cuantos pasos hace)
    agregar al inicio ........ 1 paso (O(1))
    agregar al final ......... recorre toda la lista (O(n)) si no guardas la cola
    buscar / contar / borrar . O(n)
    ordenar con burbuja ...... O(n^2)

TIPOS Y COMPARACIONES (errores que cuestan nota)
    - 3 < "Hola" lanza TypeError: no se pueden ordenar tipos mezclados
      (a menos que uses una clave: ver clave_mixta mas abajo).
    - Los strings se ordenan por codigo, asi que "Zoe" < "ana" es True
      (las mayusculas van antes). Usa clave=str.lower para ignorar mayusculas.
    - Como texto "10" < "9" es True. Si son numeros, guardalos como int.
    - bool es subclase de int: isinstance(True, int) es True. Si validas
      numeros, excluye bool explicitamente (ver es_numero).
    - input() siempre devuelve str: conviertelo con int() dentro de try/except.

REFERENCIAS
    b = a   NO copia la lista, solo crea otro nombre para la misma.
    Para copiar de verdad usa el metodo copiar().
"""


# =====================================================================
# 2. LOS 5 PATRONES DE RECORRIDO (con ellos haces casi todo)
# =====================================================================
"""
PATRON 1 - RECORRER TODO
    actual = self.head
    while actual is not None:
        ...usar actual.data...
        actual = actual.next            # NUNCA olvides avanzar

PATRON 2 - CON ANTERIOR (para eliminar o insertar antes de algo)
    anterior = None
    actual = self.head
    while actual is not None:
        if <se cumple>:
            if anterior is None:        # era el primero
                self.head = actual.next
            else:
                anterior.next = actual.next
            break
        anterior = actual
        actual = actual.next

PATRON 3 - CON CONTADOR / INDICE (para posiciones)
    indice = 0
    actual = self.head
    while actual is not None:
        if indice == buscado: ...
        actual = actual.next
        indice += 1

PATRON 4 - PARAR EN EL ULTIMO (para agregar al final)
    actual = self.head
    while actual.next is not None:      # ojo: .next, no actual
        actual = actual.next
    # aqui actual es el ultimo nodo

PATRON 5 - ELIMINAR / MOVER MIENTRAS RECORRES
    siguiente = actual.next             # GUARDAR ANTES de tocar actual
    ...eliminar o mover actual...
    actual = siguiente                  # avanzar con lo guardado
"""


# =====================================================================
# FUNCIONES AUXILIARES (validaciones y claves de ordenamiento)
# =====================================================================
def _identidad(x):
    """Clave por defecto: el dato se compara tal cual."""
    return x


def es_numero(x):
    """True si x es int o float (y NO bool)."""
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def es_entero(x):
    """True si x es int (y NO bool)."""
    return isinstance(x, int) and not isinstance(x, bool)


def clave_mixta(x):
    """
    Permite ordenar una lista con numeros Y textos mezclados:
    primero todos los numeros (de menor a mayor), luego los textos (a-z).
        lista.ordenar_datos(clave=clave_mixta)
    """
    if isinstance(x, str):
        return (1, x.lower())
    return (0, x)


def pedir_entero(leer, mensaje, minimo=None, maximo=None):
    """
    Pide un entero hasta que el usuario escriba uno valido.
    'leer' es input normalmente (se recibe como parametro para poder probar).
    """
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


def pedir_opcion(leer, mensaje, opciones):
    """Pide un texto hasta que sea una de las 'opciones' validas."""
    while True:
        texto = str(leer(mensaje)).strip().lower()
        if texto in opciones:
            return texto
        print(f"  Opcion invalida. Opciones: {', '.join(opciones)}")


def generar_contrasena(longitud=8, alfabeto=None):
    """Contrasena aleatoria. Con un alfabeto corto se generan repetidas (util para pruebas)."""
    if alfabeto is None:
        alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(alfabeto) for _ in range(longitud))


# =====================================================================
# 3. CLASES
# =====================================================================
class Nodo:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class Jugador:
    """Dato de ejemplo (objeto) para mostrar como filtrar/ordenar por atributo."""
    def __init__(self, nombre, puntos=0):
        self.nombre = nombre
        self.puntos = puntos

    def __str__(self):
        return f"{self.nombre}({self.puntos})"

    __repr__ = __str__


class Lista_enlazada:
    def __init__(self):
        self.head = None

    # =================================================================
    # A. BASICOS
    # =================================================================
    def is_empty(self):
        return self.head is None

    def length(self):
        contador = 0
        actual = self.head
        while actual is not None:
            contador += 1
            actual = actual.next
        return contador

    def mostrar_datos(self):
        """Muestra los datos recorriendo los nodos. No crea una lista de Python."""
        actual = self.head
        while actual is not None:
            print(actual.data, end=" ")
            actual = actual.next
        print()

    @classmethod
    def desde_lista(cls, datos):
        """Construye una Lista_enlazada desde una lista de Python (guardando la cola: O(n))."""
        lista = cls()
        cola = None
        for dato in datos:
            nuevo = Nodo(dato)
            if cola is None:
                lista.head = nuevo
            else:
                cola.next = nuevo
            cola = nuevo
        return lista

    def copiar(self):
        """Copia independiente (nodos nuevos)."""
        copia = Lista_enlazada()
        actual = self.head
        while actual is not None:
            copia.agregar_al_final(actual.data)
            actual = actual.next
        return copia

    def vaciar(self):
        self.head = None

    def __str__(self):
        if self.head is None:
            return "(lista vacia)"
        texto = ""
        actual = self.head
        while actual is not None:
            texto += str(actual.data) + " --> "
            actual = actual.next
        return texto + "None"

    def print_list(self):
        print(self)

    def recorrer(self, accion):
        """PATRON 1 como metodo generico: aplica 'accion' a cada dato."""
        actual = self.head
        while actual is not None:
            accion(actual.data)
            actual = actual.next

    def recorrer_con_indice(self, accion):
        """PATRON 3: accion(indice, dato)."""
        indice = 0
        actual = self.head
        while actual is not None:
            accion(indice, actual.data)
            actual = actual.next
            indice += 1

    # =================================================================
    # B. AGREGAR / INSERTAR
    # =================================================================
    def agregar_al_inicio(self, data):
        self.head = Nodo(data, self.head)

    def agregar_al_final(self, data):
        nuevo = Nodo(data)
        if self.head is None:
            self.head = nuevo
            return
        actual = self.head
        while actual.next is not None:      # PATRON 4
            actual = actual.next
        actual.next = nuevo

    def agregar_sin_repetir(self, data):
        """Variante: no agrega si el dato ya existe."""
        if self.existe(data):
            print(f"El dato {data} ya existe, no se agrego.")
            return False
        self.agregar_al_final(data)
        return True

    def insertar_en_posicion(self, indice, data):
        """0 = inicio, length = final."""
        if indice < 0 or indice > self.length():
            print("Posicion de insercion incorrecta")
            return False
        if indice == 0:
            self.agregar_al_inicio(data)
            return True
        anterior = self.head
        for _ in range(indice - 1):         # llegar al nodo anterior
            anterior = anterior.next
        anterior.next = Nodo(data, anterior.next)
        return True

    def insertar_despues_de(self, referencia, data, clave=None):
        """Inserta 'data' despues del primer nodo cuya clave sea 'referencia'."""
        k = clave or _identidad
        actual = self.head
        while actual is not None and k(actual.data) != referencia:
            actual = actual.next
        if actual is None:
            print(f"No existe '{referencia}' en la lista.")
            return False
        actual.next = Nodo(data, actual.next)
        return True

    def insertar_antes_de(self, referencia, data, clave=None):
        """Inserta 'data' antes del primer nodo cuya clave sea 'referencia'."""
        k = clave or _identidad
        if self.head is None:
            print("La lista esta vacia.")
            return False
        if k(self.head.data) == referencia:
            self.agregar_al_inicio(data)
            return True
        anterior = self.head
        while anterior.next is not None and k(anterior.next.data) != referencia:
            anterior = anterior.next
        if anterior.next is None:
            print(f"No existe '{referencia}' en la lista.")
            return False
        anterior.next = Nodo(data, anterior.next)
        return True

    def insertar_ordenado(self, data, clave=None, descendente=False):
        """Inserta manteniendo el orden (la lista ya debe estar ordenada igual)."""
        k = clave or _identidad

        def va_antes(a, b):                 # True si 'a' debe ir antes que 'b'
            return k(a) > k(b) if descendente else k(a) < k(b)

        nuevo = Nodo(data)
        if self.head is None or va_antes(data, self.head.data):
            nuevo.next = self.head
            self.head = nuevo
            return
        actual = self.head
        while actual.next is not None and not va_antes(data, actual.next.data):
            actual = actual.next
        nuevo.next = actual.next
        actual.next = nuevo

    def insertar_segun_signo(self, dato):
        """
        (Parcial 2354) Negativo -> inicio. Positivo -> final.
        Cero -> entre los negativos y los positivos.
        Rechaza strings y repetidos. Muestra la lista y retorna el promedio.
        """
        if isinstance(dato, str):
            print(f"'{dato}' es un string, no se inserta.")
        elif not es_numero(dato):
            print(f"{dato!r} no es un numero valido, no se inserta.")
        elif self.existe(dato):
            print(f"El numero {dato} ya esta en la lista, no se inserta.")
        elif dato < 0:
            self.agregar_al_inicio(dato)
        elif dato > 0:
            self.agregar_al_final(dato)
        else:                                # dato == 0
            if self.head is None or self.head.data >= 0:
                self.agregar_al_inicio(0)    # vacia, o solo hay positivos
            else:
                ultimo_negativo = self.head
                while ultimo_negativo.next is not None and ultimo_negativo.next.data < 0:
                    ultimo_negativo = ultimo_negativo.next
                # si solo hay negativos, next es None y el 0 queda al final
                ultimo_negativo.next = Nodo(0, ultimo_negativo.next)
        self.print_list()
        return self.promedio()

    # =================================================================
    # C. BUSCAR Y CONSULTAR
    # =================================================================
    def posicion_de(self, data, clave=None):
        """Indice de la primera aparicion, o -1 si no esta."""
        k = clave or _identidad
        indice = 0
        actual = self.head
        while actual is not None:
            if k(actual.data) == data:
                return indice
            actual = actual.next
            indice += 1
        return -1

    def existe(self, data, clave=None):
        return self.posicion_de(data, clave) != -1

    def contar(self, data, clave=None):
        """Cuantas veces aparece 'data'."""
        k = clave or _identidad
        veces = 0
        actual = self.head
        while actual is not None:
            if k(actual.data) == data:
                veces += 1
            actual = actual.next
        return veces

    def obtener(self, indice):
        """Dato en la posicion 'indice' (o None si no existe)."""
        if indice < 0:
            return None
        contador = 0
        actual = self.head
        while actual is not None:
            if contador == indice:
                return actual.data
            actual = actual.next
            contador += 1
        return None

    def get_last_node(self):
        """Dato del ultimo nodo (None si esta vacia)."""
        if self.head is None:
            return None
        actual = self.head
        while actual.next is not None:
            actual = actual.next
        return actual.data

    def buscar_nodo(self, condicion):
        """Devuelve el PRIMER nodo (no el dato) que cumpla condicion(dato), o None."""
        actual = self.head
        while actual is not None:
            if condicion(actual.data):
                return actual
            actual = actual.next
        return None

    def buscar_todos(self, condicion):
        """Devuelve una Lista_enlazada con los indices encontrados."""
        indices = Lista_enlazada()
        indice = 0
        actual = self.head
        while actual is not None:
            if condicion(actual.data):
                indices.agregar_al_final(indice)
            actual = actual.next
            indice += 1
        return indices

    def suma(self, clave=None):
        k = clave or _identidad
        total = 0
        actual = self.head
        while actual is not None:
            total += k(actual.data)
            actual = actual.next
        return total

    def promedio(self, clave=None):
        """None si la lista esta vacia (evita dividir entre cero)."""
        n = self.length()
        if n == 0:
            return None
        return self.suma(clave) / n

    def maximo(self, clave=None):
        """Dato con mayor clave (None si vacia)."""
        if self.head is None:
            return None
        k = clave or _identidad
        mejor = self.head.data
        actual = self.head.next
        while actual is not None:
            if k(actual.data) > k(mejor):
                mejor = actual.data
            actual = actual.next
        return mejor

    def minimo(self, clave=None):
        if self.head is None:
            return None
        k = clave or _identidad                      # mismo patron que maximo, pero con <
        mejor = self.head.data
        actual = self.head.next
        while actual is not None:
            if k(actual.data) < k(mejor):
                mejor = actual.data
            actual = actual.next
        return mejor

    # =================================================================
    # D. FILTRAR  (devuelven una Lista_enlazada NUEVA; la original no cambia)
    # =================================================================
    def filtrar(self, condicion):
        """
        Filtro universal: conserva los datos donde condicion(dato) sea True.
            lista.filtrar(lambda x: x > 10)
            lista.filtrar(lambda j: j.puntos >= 50)
        """
        nueva = Lista_enlazada()
        cola = None
        actual = self.head
        while actual is not None:
            if condicion(actual.data):
                nuevo = Nodo(actual.data)
                if cola is None:
                    nueva.head = nuevo
                else:
                    cola.next = nuevo
                cola = nuevo
            actual = actual.next
        return nueva

    def filtrar_por_nombre(self, nombre, clave=None, ignorar_mayusculas=True):
        """Coincidencia EXACTA de nombre. clave=lambda j: j.nombre si son objetos."""
        k = clave or _identidad
        buscado = str(nombre).lower() if ignorar_mayusculas else str(nombre)

        def cumple(d):
            valor = str(k(d))
            return (valor.lower() if ignorar_mayusculas else valor) == buscado
        return self.filtrar(cumple)

    def filtrar_por_prefijo(self, prefijo, clave=None):
        """Los que EMPIEZAN con 'prefijo' (sin importar mayusculas)."""
        k = clave or _identidad
        return self.filtrar(lambda d: str(k(d)).lower().startswith(str(prefijo).lower()))

    def filtrar_que_contiene(self, texto, clave=None):
        """Los que CONTIENEN 'texto' en cualquier parte."""
        k = clave or _identidad
        return self.filtrar(lambda d: str(texto).lower() in str(k(d)).lower())

    def filtrar_por_rango(self, minimo, maximo, clave=None):
        """Los que cumplen minimo <= valor <= maximo (valores numericos)."""
        k = clave or _identidad
        return self.filtrar(lambda d: es_numero(k(d)) and minimo <= k(d) <= maximo)

    def solo_numeros(self):
        return self.filtrar(es_numero)

    def solo_textos(self):
        return self.filtrar(lambda d: isinstance(d, str))

    # =================================================================
    # E. ELIMINAR
    # =================================================================
    def eliminar_inicio(self):
        if self.head is None:
            print("La lista esta vacia.")
            return False
        self.head = self.head.next
        return True

    def eliminar_final(self):
        if self.head is None:
            print("La lista esta vacia.")
            return False
        if self.head.next is None:           # un solo nodo
            self.head = None
            return True
        anterior = self.head
        while anterior.next.next is not None:    # parar en el PENULTIMO
            anterior = anterior.next
        anterior.next = None
        return True

    def eliminar_dato(self, data, clave=None):
        """
        Elimina la PRIMERA aparicion. Devuelve True/False.
        (El delete_node de clase se rompe si el dato no existe: aqui se valida.)
        """
        k = clave or _identidad
        anterior = None
        actual = self.head
        while actual is not None and k(actual.data) != data:     # PATRON 2
            anterior = actual
            actual = actual.next
        if actual is None:
            print(f"El dato '{data}' no existe en la lista.")
            return False
        if anterior is None:
            self.head = actual.next
        else:
            anterior.next = actual.next
        return True

    def eliminar_posicion(self, indice):
        if indice < 0 or self.head is None:
            print("Posicion invalida o lista vacia.")
            return False
        if indice == 0:
            self.head = self.head.next
            return True
        anterior = self.head
        for _ in range(indice - 1):
            if anterior.next is None:
                break
            anterior = anterior.next
        if anterior.next is None:
            print("Posicion fuera de rango.")
            return False
        anterior.next = anterior.next.next
        return True

    def eliminar_si(self, condicion):
        """
        Elimina TODOS los datos que cumplan condicion(dato). Devuelve cuantos elimino.
        Es la herramienta mas general: casi cualquier "elimine los..." sale de aqui.
            lista.eliminar_si(lambda x: x < 0)           # negativos
            lista.eliminar_si(lambda x: x % 2 == 0)      # pares
            lista.eliminar_si(lambda j: j.puntos == 0)   # objetos
        """
        eliminados = 0
        anterior = None
        actual = self.head
        while actual is not None:
            siguiente = actual.next                  # PATRON 5
            if condicion(actual.data):
                if anterior is None:
                    self.head = siguiente
                else:
                    anterior.next = siguiente
                eliminados += 1
            else:
                anterior = actual                    # solo avanza si NO elimino
            actual = siguiente
        return eliminados

    def conservar_si(self, condicion):
        """Inverso de eliminar_si: deja SOLO los que cumplen."""
        return self.eliminar_si(lambda d: not condicion(d))

    def eliminar_todas(self, data, clave=None):
        """Elimina TODAS las apariciones de 'data'."""
        k = clave or _identidad
        return self.eliminar_si(lambda d: k(d) == data)

    def eliminar_duplicados(self):
        """Deja solo la PRIMERA aparicion de cada dato (version clasica con 2 punteros)."""
        actual = self.head
        eliminados = 0
        while actual is not None:
            anterior = actual
            revisar = actual.next
            while revisar is not None:
                if revisar.data == actual.data:
                    anterior.next = revisar.next     # saltar el repetido
                    eliminados += 1
                else:
                    anterior = revisar
                revisar = revisar.next
            actual = actual.next
        return eliminados

    def eliminar_duplicados_v2(self):
        """Version simple: usa dos punteros, igual que eliminar_duplicados."""
        return self.eliminar_duplicados()

    def eliminar_exceso(self, limite=2):
        """
        (Parcial 2355-a) Si un dato aparece MAS de 'limite' veces, deja solo UNO
        (el primero) y elimina los demas. Los que aparecen 'limite' veces o menos
        NO se tocan. Ej: 4-8-32-8-7-8-94 -> 4-8-32-7-94. Devuelve cuantos elimino.
        """
        if self.head is None:
            print("La lista esta vacia.")
            return 0
        eliminados = 0
        actual = self.head
        while actual is not None:
            if self.contar(actual.data) > limite:
                anterior = actual
                revisar = actual.next
                while revisar is not None:
                    if revisar.data == actual.data:
                        anterior.next = revisar.next
                        eliminados += 1
                    else:
                        anterior = revisar
                    revisar = revisar.next
            actual = actual.next
        return eliminados

    def eliminar_secuencia_ascendente(self, repetir=False):
        """
        (Parcial 2355-b) Elimina grupos de nodos CONTIGUOS cuyos datos suben de 1 en 1
        (minimo 2 datos). Ej: 4-8-32-6-7-8-94 -> 4-8-32-94.
        repetir=True: vuelve a pasar mientras el borrado deje nuevas secuencias.
        Devuelve cuantos datos elimino.
        """
        if self.head is None:
            print("La lista esta vacia.")
            return 0
        solo_numeros = True
        revisar_tipo = self.head
        while revisar_tipo is not None:
            if not es_numero(revisar_tipo.data):
                solo_numeros = False
                break
            revisar_tipo = revisar_tipo.next
        if not solo_numeros:
            print("La lista tiene datos no numericos: no se puede buscar secuencias.")
            return 0
        total = 0
        while True:
            eliminados = 0
            anterior = None
            actual = self.head
            while actual is not None:
                fin = actual
                largo = 1
                while fin.next is not None and fin.next.data == fin.data + 1:
                    fin = fin.next
                    largo += 1
                if largo >= 2:                       # secuencia: desconectar actual..fin
                    siguiente = fin.next
                    if anterior is None:
                        self.head = siguiente
                    else:
                        anterior.next = siguiente
                    eliminados += largo
                    actual = siguiente               # anterior no avanza
                else:
                    anterior = actual
                    actual = actual.next
            total += eliminados
            if not repetir or eliminados == 0:
                break
        return total

    def eliminar_repetidos_consecutivos(self):
        """1-1-2-2-2-3-1 -> 1-2-3-1 (solo colapsa los repetidos que estan pegados)."""
        eliminados = 0
        actual = self.head
        while actual is not None and actual.next is not None:
            if actual.next.data == actual.data:
                actual.next = actual.next.next
                eliminados += 1
            else:
                actual = actual.next
        return eliminados

    # =================================================================
    # F. ORDENAR
    # =================================================================
    """
    TODAS reciben:
        clave=None       funcion que saca el valor por el que se ordena
        descendente=False   True = de mayor a menor

    Ejemplos de clave:
        clave=None                          numeros o textos simples
        clave=str.lower                     textos ignorando mayusculas
        clave=lambda j: j.nombre            objetos por nombre
        clave=lambda j: j.puntos            objetos por puntaje
        clave=lambda j: (-j.puntos, j.nombre)   puntos de mayor a menor y, si
                                                empatan, por nombre A-Z
        clave=clave_mixta                   numeros y textos mezclados
        clave=len                           por longitud de texto
    """

    def ordenar_datos(self, clave=None, descendente=False):
        """Burbuja intercambiando los DATOS (la mas facil y segura en un parcial)."""
        if self.head is None or self.head.next is None:
            return
        k = clave or _identidad
        cambiado = True
        while cambiado:
            cambiado = False
            actual = self.head
            while actual.next is not None:
                siguiente = actual.next
                a, b = k(actual.data), k(siguiente.data)
                mal_orden = (a < b) if descendente else (a > b)
                if mal_orden:
                    actual.data, siguiente.data = siguiente.data, actual.data
                    cambiado = True
                actual = siguiente

    def ordenar_nodos(self, clave=None, descendente=False):
        """Burbuja intercambiando NODOS (cambia enlaces; la version 'dificil')."""
        if self.head is None or self.head.next is None:
            return
        k = clave or _identidad
        cambiado = True
        while cambiado:
            cambiado = False
            anterior = None
            actual = self.head
            while actual.next is not None:
                siguiente = actual.next
                a, b = k(actual.data), k(siguiente.data)
                mal_orden = (a < b) if descendente else (a > b)
                if mal_orden:
                    cambiado = True
                    if anterior is None:
                        self.head = siguiente
                    else:
                        anterior.next = siguiente
                    actual.next = siguiente.next
                    siguiente.next = actual
                    anterior = siguiente             # actual NO avanza
                else:
                    anterior = actual
                    actual = actual.next

    def ordenar_por_insercion(self, clave=None, descendente=False):
        """Construye el orden insertando cada dato en su lugar (usa insertar_ordenado)."""
        nueva = Lista_enlazada()
        actual = self.head
        while actual is not None:
            nueva.insertar_ordenado(actual.data, clave, descendente)
            actual = actual.next
        self.head = nueva.head

    def ordenar_texto(self, descendente=False):
        """A-Z ignorando mayusculas (sirve aunque haya numeros: los trata como texto)."""
        self.ordenar_datos(clave=lambda x: str(x).lower(), descendente=descendente)

    def ordenar_numeros(self, descendente=False):
        """Atajo para numeros."""
        self.ordenar_datos(descendente=descendente)

    def esta_ordenada(self, clave=None, descendente=False):
        k = clave or _identidad
        actual = self.head
        while actual is not None and actual.next is not None:
            a, b = k(actual.data), k(actual.next.data)
            if (a < b) if descendente else (a > b):
                return False
            actual = actual.next
        return True

    # =================================================================
    # G. MOVER Y REORGANIZAR
    # =================================================================
    def mover_nodo_al_final(self, nodo):
        """Mueve ESE nodo (por identidad) al final. 3 pasos: desconectar, llegar al ultimo, enganchar."""
        if self.head is None or nodo.next is None:     # vacia o ya es el ultimo
            return
        if self.head is nodo:                          # PASO 1: desconectar
            self.head = nodo.next
        else:
            anterior = self.head
            while anterior.next is not nodo:
                anterior = anterior.next
            anterior.next = nodo.next
        ultimo = nodo.next                             # PASO 2: llegar al ultimo
        while ultimo.next is not None:
            ultimo = ultimo.next
        ultimo.next = nodo                             # PASO 3: enganchar
        nodo.next = None

    def mover_al_final(self, data, clave=None):
        """Busca por dato (o por clave) y lo manda al final."""
        k = clave or _identidad
        nodo = self.buscar_nodo(lambda d: k(d) == data)
        if nodo is None:
            print(f"El dato '{data}' no existe en la lista.")
            return False
        self.mover_nodo_al_final(nodo)
        return True

    def mover_al_inicio(self, data, clave=None):
        k = clave or _identidad
        anterior = None
        actual = self.head
        while actual is not None and k(actual.data) != data:
            anterior = actual
            actual = actual.next
        if actual is None:
            print(f"El dato '{data}' no existe en la lista.")
            return False
        if anterior is None:                           # ya es el primero
            return True
        anterior.next = actual.next
        actual.next = self.head
        self.head = actual
        return True

    def Mover_dato(self, nombre, posiciones, direccion, limitar=True, clave=None):
        """
        (Parcial 23531) Mueve el dato 'nombre' N posiciones.
        direccion: "adelante" = hacia la cabeza | "atras" = hacia el final.
        Mover_dato("Juan", 3, "adelante") -> Juan sube 3 lugares hacia head.
        limitar=True : si se pasa del limite, queda en el extremo (y avisa).
        limitar=False: si se pasa del limite, NO mueve y avisa.
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

        anterior = None                                # buscar al jugador (con su indice)
        actual = self.head
        indice = 0
        while actual is not None and k(actual.data) != nombre:
            anterior = actual
            actual = actual.next
            indice += 1
        if actual is None:
            print(f"El jugador '{nombre}' no existe en la lista.")
            return False

        n = self.length()
        nuevo = indice + sentido * posiciones
        if nuevo < 0 or nuevo > n - 1:
            if not limitar:
                print(f"No se puede mover {nombre}: se sale de la lista.")
                return False
            nuevo = 0 if nuevo < 0 else n - 1
            print(f"{nombre} llego al limite de la lista (posicion {nuevo}).")
        if nuevo == indice:
            print(f"{nombre} ya esta en esa posicion, no se mueve.")
            return True

        if anterior is None:                           # 1) desconectar
            self.head = actual.next
        else:
            anterior.next = actual.next
        if nuevo == 0:                                 # 2) insertar en 'nuevo'
            actual.next = self.head
            self.head = actual
        else:
            pre = self.head
            for _ in range(nuevo - 1):
                pre = pre.next
            actual.next = pre.next
            pre.next = actual
        return True

    def intercambiar_posiciones(self, i, j):
        """Intercambia los DATOS de las posiciones i y j."""
        n = self.length()
        if not (0 <= i < n and 0 <= j < n):
            print("Posiciones fuera de rango.")
            return False
        if i == j:
            return True
        nodo_i = nodo_j = None
        indice = 0
        actual = self.head
        while actual is not None:
            if indice == i:
                nodo_i = actual
            if indice == j:
                nodo_j = actual
            actual = actual.next
            indice += 1
        nodo_i.data, nodo_j.data = nodo_j.data, nodo_i.data
        return True

    def invertir(self):
        """Da la vuelta a la lista cambiando los enlaces."""
        anterior = None
        actual = self.head
        while actual is not None:
            siguiente = actual.next
            actual.next = anterior
            anterior = actual
            actual = siguiente
        self.head = anterior

    def rotar(self, k):
        """Los primeros k datos pasan al final: 1-2-3-4-5 rotar(2) -> 3-4-5-1-2."""
        n = self.length()
        if n < 2:
            return
        k %= n
        if k == 0:
            return
        nuevo_ultimo = self.head
        for _ in range(k - 1):
            nuevo_ultimo = nuevo_ultimo.next
        nuevo_head = nuevo_ultimo.next
        nuevo_ultimo.next = None
        cola = nuevo_head
        while cola.next is not None:
            cola = cola.next
        cola.next = self.head
        self.head = nuevo_head

    def concatenar(self, otra):
        """Pega 'otra' al final (comparten nodos; usa otra.copiar() si no quieres eso)."""
        if otra.head is None:
            return
        if self.head is None:
            self.head = otra.head
            return
        actual = self.head
        while actual.next is not None:
            actual = actual.next
        actual.next = otra.head

    def dividir(self):
        """Corta por la mitad: esta lista conserva la 1ra mitad y devuelve la 2da."""
        n = self.length()
        segunda = Lista_enlazada()
        if n < 2:
            return segunda
        mitad = (n + 1) // 2
        anterior = self.head
        for _ in range(mitad - 1):
            anterior = anterior.next
        segunda.head = anterior.next
        anterior.next = None
        return segunda

    # =================================================================
    # I. DATOS ALEATORIOS
    # =================================================================
    def llenar_aleatoria(self, cantidad, minimo, maximo, sin_repetidos=False):
        """Agrega enteros aleatorios sin usar listas de Python."""
        if cantidad < 0 or minimo > maximo:
            return False
        if sin_repetidos and cantidad > maximo - minimo + 1:
            print("No hay suficientes numeros distintos en ese rango.")
            return False
        agregados = 0
        while agregados < cantidad:
            numero = random.randint(minimo, maximo)
            if sin_repetidos and self.existe(numero):
                continue
            self.agregar_al_final(numero)
            agregados += 1
        return True

    def llenar_contrasenas(self, cantidad, longitud=8, alfabeto=None):
        """Agrega 'cantidad' contrasenas aleatorias (strings)."""
        for _ in range(cantidad):
            self.agregar_al_final(generar_contrasena(longitud, alfabeto))


# =====================================================================


# =====================================================================
# NOTA PARA EL PARCIAL
# =====================================================================
# Esta version evita listas nativas de Python en los metodos de la
# estructura. Cuando un metodo necesita devolver varios resultados,
# devuelve otra Lista_enlazada.
