# =====================================================
# SOLUCIONES DE LAS PRÁCTICAS 01, 02 y 05
# Úsalo solo para comparar DESPUÉS de intentar los ejercicios.
# =====================================================


# #####################################################
# SOLUCIONES 01: FUNCIONES
# #####################################################

# ---------- Recordatorio: el ciclo for ----------
for numero in [10, 20, 30]:
    print("numero vale", numero)

for i in range(3):          # range(3) da 0, 1, 2
    print("vuelta", i)


# ---------- EJEMPLO ----------
def doble(n):
    return n * 2

print("doble(5) =", doble(5))


# ---------- EJERCICIO 1 ----------
# Escribe 'triple': devuelve n * 3
def triple(n):
    return n * 3

print("1) triple(4) =", triple(4), " -> debe dar 12")


# ---------- EJERCICIO 2 ----------
# 'es_par': devuelve True si n es par, False si no.
# Pista: n % 2 es el residuo de dividir entre 2 (si da 0, es par).
def es_par(n):
    return n % 2 == 0

print("2) es_par(8) =", es_par(8), " -> debe dar True")
print("2) es_par(7) =", es_par(7), " -> debe dar False")


# ---------- EJERCICIO 3 ----------
# 'mayor': recibe dos números y devuelve el más grande (usa if).
def mayor(a, b):
    if a > b:
        return a
    else:
        return b

print("3) mayor(3, 9) =", mayor(3, 9), " -> debe dar 9")


# ---------- EJERCICIO 4 ----------
# 'saludo': devuelve el saludo + un espacio + el nombre.
# El saludo por defecto es "Hola".
def saludo(nombre, texto = "Hola"):
    return texto + " " + nombre

print("4) saludo('Ana') =", saludo("Ana"), " -> debe dar Hola Ana")
print("4) saludo('Ana', 'Buenas') =", saludo("Ana", "Buenas"), " -> debe dar Buenas Ana")


# ---------- EJERCICIO 5 ----------
# 'suma_lista': devuelve la suma de todos los números de una lista.
# Pista: empieza con total = 0 y recorre con for.
def suma_lista(lista):
    total = 0
    for numero in lista:
        total = total + numero
    return total

print("5) suma_lista([4, 8, 32]) =", suma_lista([4, 8, 32]), " -> debe dar 44")


# ---------- EJERCICIO 6 ----------
# 'contar_pares': cuántos números pares hay en la lista (usa es_par).
def contar_pares(lista):
    cantidad = 0
    for numero in lista:
        if es_par(numero):
            cantidad = cantidad + 1
    return cantidad

print("6) contar_pares([1, 2, 3, 4, 6]) =", contar_pares([1, 2, 3, 4, 6]), " -> debe dar 3")


# ---------- EJERCICIO 7 ----------
# 'promedio': suma / cantidad. Si la lista está vacía devuelve 0
# (así evitas dividir entre cero). Pista: len(lista) da la cantidad.
def promedio(lista):
    if len(lista) == 0:
        return 0
    return suma_lista(lista) / len(lista)

print("7) promedio([2, 4, 6]) =", promedio([2, 4, 6]), " -> debe dar 4.0")
print("7) promedio([]) =", promedio([]), " -> debe dar 0")


# ---------- EJERCICIO 8 ----------
# 'es_numero': True si el dato es int o float. False si es texto u otra cosa.
# Pista: isinstance(dato, (int, float)). Ojo: True/False de Python también
# cuentan como int, así que descarta los booleanos con isinstance(dato, bool).
def es_numero(dato):
    return isinstance(dato, (int, float)) and not isinstance(dato, bool)

print("8) es_numero(5) =", es_numero(5), " -> debe dar True")
print("8) es_numero(3.5) =", es_numero(3.5), " -> debe dar True")
print("8) es_numero('hola') =", es_numero("hola"), " -> debe dar False")
print("8) es_numero(True) =", es_numero(True), " -> debe dar False")


# ---------- EJERCICIO 9 ----------
# 'contar_valor': cuántas veces aparece 'valor' en la lista.
# (Es la misma idea del método 'contar' de la lista enlazada.)
def contar_valor(lista, valor):
    veces = 0
    for dato in lista:
        if dato == valor:
            veces = veces + 1
    return veces

print("9) contar_valor([8, 3, 8, 8], 8) =", contar_valor([8, 3, 8, 8], 8), " -> debe dar 3")


# ---------- EJERCICIO 10 (usa input) ----------
# 'pedir_numero': pide un número con input() y repite la pregunta
# mientras lo que escriba el usuario no sea un número entero (usa isdigit()).
# Devuelve el número ya convertido con int().
def pedir_numero():
    texto = input("Escriba un número entero: ")
    while not texto.isdigit():
        print("Dato errado, intente de nuevo")
        texto = input("Escriba un número entero: ")
    return int(texto)

# Cuando lo termines, quita el # de la línea de abajo para probarlo:
# print("10) escribiste:", pedir_numero())



# #####################################################
# SOLUCIONES 02: CLASES
# #####################################################

# ---------- EJEMPLO: una clase ----------
class Perro:
    def __init__(self, nombre):
        self.nombre = nombre            # guarda el dato DENTRO del objeto

    def ladrar(self):
        print(self.nombre, "dice: guau")

p1 = Perro("Rex")
p2 = Perro("Luna")
p1.ladrar()      # self es p1
p2.ladrar()      # self es p2
print("El nombre de p1 es", p1.nombre)


# ---------- EJERCICIO 1 ----------
# Clase 'Estudiante' con nombre y nota.
#   __init__(self, nombre, nota): guarda ambos con self.
#   aprobo(self): devuelve True si la nota es >= 3.0
#   presentar(self): imprime "Soy Ana y mi nota es 4.5"
class Estudiante:
    def __init__(self, nombre, nota):
        self.nombre = nombre
        self.nota = nota

    def aprobo(self):
        return self.nota >= 3.0

    def presentar(self):
        print("Soy", self.nombre, "y mi nota es", self.nota)

e1 = Estudiante("Ana", 4.5)
e2 = Estudiante("Luis", 2.0)
e1.presentar()
print("1) Ana aprobó:", e1.aprobo(), " -> debe dar True")
print("1) Luis aprobó:", e2.aprobo(), " -> debe dar False")


# ---------- EJERCICIO 2 ----------
# Clase 'Contador'.
#   __init__: self.valor empieza en 0
#   sumar(self): le suma 1 a self.valor
class Contador:
    def __init__(self):
        self.valor = 0

    def sumar(self):
        self.valor = self.valor + 1

c = Contador()
c.sumar()
c.sumar()
print("2) valor =", c.valor if hasattr(c, "valor") else "(aún no existe)", " -> debe dar 2")


# ---------- EJERCICIO 3: enlazar nodos a mano ----------
class Nodo:
    def __init__(self, data = None, next = None):
        self.data = data
        self.next = next

n1 = Nodo(10)
n2 = Nodo(20)
n3 = Nodo(30)

# Quita los # y completa:
n1.next = n2
n2.next = n3
actual = n1
while actual != None:
    print(actual.data)
    actual = actual.next
# Debe imprimir 10, 20 y 30.


# ---------- EJERCICIO 4: una mini lista ----------
#   agregar_al_inicio(data): el nodo nuevo apunta a la cabeza vieja
#                            y pasa a ser la cabeza.
#   print_list(): imprime todos los datos recorriendo desde la cabeza.
class Lista_simple:
    def __init__(self):
        self.head = None

    def agregar_al_inicio(self, data):
        self.head = Nodo(data, self.head)

    def print_list(self):
        actual = self.head
        while actual != None:
            print(actual.data, end=" --> ")
            actual = actual.next
        print()

mi_lista = Lista_simple()
mi_lista.agregar_al_inicio(3)
mi_lista.agregar_al_inicio(2)
mi_lista.agregar_al_inicio(1)
mi_lista.print_list()     # debe imprimir 1 --> 2 --> 3 -->



# #####################################################
# SOLUCIONES 05: MÉTODOS EN LA LISTA ENLAZADA
# #####################################################

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

    # EJERCICIO 1
    def sumar(self):
        total = 0
        actual = self.head
        while actual != None:
            total += actual.data
            actual = actual.next
        return total

    # EJERCICIO 2
    def mayor(self):
        if self.head is None:
            return None
        el_mayor = self.head.data
        actual = self.head.next
        while actual != None:
            if actual.data > el_mayor:
                el_mayor = actual.data
            actual = actual.next
        return el_mayor

    # EJERCICIO 3
    def eliminar_primero(self):
        if self.is_empty():
            print("La lista está vacía")
            return
        self.head = self.head.next

    # EJERCICIO 4
    def eliminar_ultimo(self):
        if self.is_empty():
            print("La lista está vacía")
            return
        if self.head.next is None:          # un solo nodo
            self.head = None
            return
        actual = self.head
        while actual.next.next != None:     # se detiene en el penúltimo
            actual = actual.next
        actual.next = None

    # EJERCICIO 5
    def insertar_despues(self, buscado, nuevo):
        actual = self.head
        while actual != None and actual.data != buscado:
            actual = actual.next
        if actual is None:
            print("El dato", buscado, "no existe en la lista")
            return
        actual.next = Nodo(nuevo, actual.next)

    # EJERCICIO 6
    def eliminar_todos(self, valor):
        # primero los que estén al inicio (cambia la cabeza)
        while self.head != None and self.head.data == valor:
            self.head = self.head.next
        # luego los del resto de la lista
        actual = self.head
        while actual != None and actual.next != None:
            if actual.next.data == valor:
                actual.next = actual.next.next
            else:
                actual = actual.next


# ---------- PRUEBAS (ejecuta con F5 y compara) ----------
l = Lista_enlazada()
for d in [4, 8, 32, 8, 7]:
    l.agregar_al_final(d)
l.print_list()
print("1) sumar =", l.sumar(), " -> debe dar 59")
print("2) mayor =", l.mayor(), " -> debe dar 32")

l.eliminar_primero()
print("3) sin el primero (debe ser 8 --> 32 --> 8 --> 7):")
l.print_list()

l.eliminar_ultimo()
print("4) sin el último (debe ser 8 --> 32 --> 8):")
l.print_list()

l.insertar_despues(32, 99)
print("5) insertar 99 después del 32 (debe ser 8 --> 32 --> 99 --> 8):")
l.print_list()
l.insertar_despues(1000, 5)          # debe avisar que no existe

l.eliminar_todos(8)
print("6) sin los 8 (debe ser 32 --> 99):")
l.print_list()

print("Casos especiales con lista vacía (deben dar mensaje, no error):")
vacia = Lista_enlazada()
vacia.eliminar_primero()
vacia.eliminar_ultimo()
print("mayor de vacía:", vacia.mayor(), " -> debe dar None")
