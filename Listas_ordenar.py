# Ejemplo Lista

# --- Celda 2 ---
class Nodo:
    def __init__(self, data = None, next = None):
        self.data = data
        self.next = next

# --- Celda 3 ---
class Lista_enlazada:
    def __init__(self):
        self.head = None

    # Método para agregar elementos en el frente de la linked list
    def agregar_al_inicio(self, data):
        #self.head = Nodo(data=data, next=self.head)
        nuevo_nodo = Nodo(data)
        nuevo_nodo.next = self.head
        self.head = nuevo_nodo
        #return nuevo_nodo

    # Método para verificar si la estructura de datos esta vacia
    def is_empty(self):
        return self.head == None

    # Método para agregar elementos al final de la lista enlazada
    def agregar_al_final(self, data):
      #Si la lista no existe, entonces se crea
        if not self.head:
            self.head = Nodo(data=data)
            return
        #recorre toda la lista hasta llegar al final,
        #cuando temporal.next=None
        temporal = self.head
        while temporal.next:
            temporal = temporal.next
        #Cuando llega al final de la lista, enlaza el último nodo con
        #el nuevo nodo que se crea
        temporal.next = Nodo(data=data)

    # Método para eleminar nodos
    def delete_node(self, key):
        actual = self.head
        previo = None
        #Se busca el dato a eliminar en la lista
        while actual and actual.data != key:
            previo = actual
            actual = actual.next
        #Si el dato a eliminar es el primero,
        #entonces se reasigna la cabeza de la lista
        if previo is None:
            self.head = actual.next
        elif actual:
            previo.next = actual.next
            actual.next = None

    # Método para obtener el ultimo nodo
    def get_last_node(self):
        temp = self.head
        while(temp.next is not None):
            temp = temp.next
        return temp.data

    # Método para imprimir la lista de nodos
    def print_list( self ):
        node = self.head
        while node != None:
            print(node.data, end =" --> ")
            node = node.next

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
                if actual.data < siguiente.data:
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

# --- Celda 4 ---
Lista1 =  Lista_enlazada()
Lista1.agregar_al_inicio(3)
Lista1.agregar_al_final(4)
Lista1.agregar_al_final(5)
Lista1.agregar_al_final(2)
Lista1.print_list()

# --- Celda 5 ---
Lista1.ordenar_lista()
Lista1.print_list()

# --- Celda 6 ---
Lista1.delete_node("BAQ")
Lista1.print_list()
Lista1.agregar_al_inicio("123")
Lista1.print_list()

# --- Celda 7 ---
Lista1.agregar_al_inicio("123")
Lista1.print_list()
