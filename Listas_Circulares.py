# Ejemplo de lista circular

# --- Celda 2 ---
class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None

# --- Celda 3 ---
class Lista_Circular(object):

    def __init__(self):
        self.head = None

    def is_empty(self):

        return self.head is None

    def length(self):

      cur = self.head
      count = 0
      while cur is not None:
          count += 1
                  # Si el siguiente nodo del nodo actual es el nodo principal, significa que este nodo es el nodo de cola
                  # Si no, mueva el puntero hacia atrás
          if cur.next == self.head:
              break
          else:
              cur = cur.next
      return count

    def imprimir(self):

      if self.is_empty():
          return
      cur = self.head
      print(cur.data)
      while cur.next != self.head:
          cur = cur.next
          print(cur.data, end = "-->")


    def add_first(self, data):

      node = Node(data)
      if self.is_empty():
          self.head = node
          node.next = self.head
      else:
          cur = self.head
                  # Mueva el puntero al nodo de cola
          while cur.next is not self.head:
              cur = cur.next
                  # El nodo de cola apunta al nuevo nodo
          cur.next = node
                  # El nuevo nodo apunta al nodo principal original
          node.next = self.head
                  # Luego dele el título del nodo principal al nuevo nodo
          self.head = node


    def add_last(self, data):

      node = Node(data)
      if self.is_empty():
          self.head = node
          node.next = self.head
      else:
          cur = self.head
                  # Mueve el puntero al final
          while cur.next is not self.head:
              cur = cur.next
                  # El nodo de cola apunta al nuevo nodo
          cur.next = node
                  # El nuevo nodo apunta al nodo principal
          node.next = self.head


    def insert_node(self, index, data):

      node = Node(data)
      if index < 0 or index > self.length():
          print ("Posición de inserción incorrecta")
          return False
      elif index == 0:
          self.add_first(data)
      elif index == self.length:
          self.add_last()
      else:
          cur = self.head
          pre = None # pre es el nodo anterior del nodo señalado por el puntero actual
          count = 0
                  # Mueva el puntero a la posición para insertar
          while count < index:
              pre = cur
              cur = cur.next
              count += 1
          pre.next = node
          node.next = cur

    def remove_node(self, data):

      if self.is_empty():
          return
          # Si el nodo que se va a eliminar es el nodo principal
      elif data == self.head.data:
          cur = self.head
          while cur.next != self.head:
              cur = cur.next
          cur.next = self.head.next
          self.head = self.head.next
      else:
          cur = self.head
          pre = None
                  # Mover a la posición del nodo que se va a eliminar
          while cur.data != data:
              pre = cur
              cur = cur.next
                  # Apunte el nodo precursor del nodo que se va a eliminar al nodo posterior, de modo que se omita el nodo central
          pre.next = cur.next


    def remove2_node(self, data):

      if self.is_empty():
          return
          # Si el nodo que se va a eliminar es el nodo principal
      elif data == self.head.data:
          cur = self.head
          while cur.next != self.head:
              cur = cur.next
          cur.next = self.head.next
          self.head = self.head.next
      else:
        cur = self.head
        pre = None
        while cur.data != data:
            pre = cur
            cur = cur.next
        #pre.next = cur.next
        pre.next = pre.next.next

# --- Celda 4 ---
Lista1=Lista_Circular()
Lista1.add_last(2)
Lista1.add_first('Hola')
Lista1.add_first(0)
Lista1.add_last(3)
Lista1.imprimir()

# --- Celda 5 ---
Lista1.insert_node(2, 'Mundo')
Lista1.imprimir()

# --- Celda 6 ---
Lista1.remove2_node(2)
Lista1.imprimir()
