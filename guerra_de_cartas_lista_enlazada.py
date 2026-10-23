"""
GUERRA DE CARTAS / CARTA MAYOR
Practica con las clases Lista_enlazada y Lista_circular de las guias del curso.

IMPORTANTE:
- Coloca este archivo en la MISMA carpeta que:
    SUPER_GUIA_parte1_lista_simple_sin_listas.py
    SUPER_GUIA_parte2_lista_circular_sin_listas.py
- La guia circular define la clase como Lista_circular (minuscula en circular).
- No se usan listas nativas de Python para guardar jugadores ni cartas.
- Se usan listas enlazadas para los mazos y una lista circular para los turnos.

Reglas implementadas:
- 3 jugadores, 5 cartas aleatorias (1..10) por jugador.
- La maquina tiene su propio mazo enlazado.
- Cada jugador puede robar/agregar hasta 3 cartas durante toda la partida.
- Si el jugador gana la batalla, suma los valores de todas las cartas empatadas
  en esa batalla mas las dos cartas de la batalla ganada.
- Si la maquina gana, el jugador no obtiene puntos.
- Si hay empate, se siguen jugando cartas hasta romper el empate.
- Si una batalla no empatada suma exactamente 10 y la carta del jugador es menor,
  el jugador pierde su siguiente turno.
- La partida puede detenerse al final de una ronda o termina cuando alguien
  se queda sin cartas (o la maquina no tiene cartas).
"""

import random

from SUPER_GUIA_parte1_lista_simple_sin_listas import Lista_enlazada
from SUPER_GUIA_parte2_lista_circular_sin_listas import Lista_circular


class JugadorGuerra:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mazo = Lista_enlazada()
        self.puntos = 0
        self.robos_usados = 0
        self.perder_proximo_turno = False

    def __str__(self):
        return (self.nombre + " | Puntos: " + str(self.puntos)
                + " | Cartas: " + str(self.mazo.length())
                + " | Robos usados: " + str(self.robos_usados) + "/3")


def agregar_cartas_aleatorias(mazo, cantidad):
    for _ in range(cantidad):
        mazo.agregar_al_final(random.randint(1, 10))


def obtener_carta_por_posicion(mazo, posicion):
    """Devuelve el dato de una posicion, o None si no existe."""
    actual = mazo.head
    indice = 0
    while actual is not None:
        if indice == posicion:
            return actual.data
        actual = actual.next
        indice += 1
    return None


def mostrar_mazo(mazo):
    """Muestra las cartas numeradas sin convertir el mazo a una lista Python."""
    actual = mazo.head
    indice = 0
    if actual is None:
        print("  (sin cartas)")
        return
    while actual is not None:
        print("  " + str(indice + 1) + ". Carta " + str(actual.data))
        actual = actual.next
        indice += 1


def quitar_carta_por_posicion(mazo, posicion):
    """Elimina y devuelve la carta indicada por una posicion que empieza en 0."""
    if posicion < 0 or posicion >= mazo.length():
        return None
    carta = obtener_carta_por_posicion(mazo, posicion)
    mazo.eliminar_posicion(posicion)
    return carta


def pedir_entero(mensaje, minimo, maximo):
    while True:
        texto = input(mensaje).strip()
        try:
            numero = int(texto)
        except ValueError:
            print("Escribe un numero entero.")
            continue
        if numero < minimo or numero > maximo:
            print("Elige un numero entre " + str(minimo) + " y " + str(maximo) + ".")
            continue
        return numero


def preparar_jugadores():
    jugadores = Lista_circular()
    nombres = ("Jugador 1", "Jugador 2", "Jugador 3")
    for nombre in nombres:
        jugador = JugadorGuerra(nombre)
        agregar_cartas_aleatorias(jugador.mazo, 5)
        jugadores.add_last(jugador)
    return jugadores


def preparar_mazo_maquina():
    mazo = Lista_enlazada()
    # 15 cartas iniciales: la maquina tiene recursos para jugar varias rondas.
    agregar_cartas_aleatorias(mazo, 15)
    return mazo


def mostrar_estado(jugadores, mazo_maquina):
    print("\n========== ESTADO DE LA PARTIDA ==========")
    actual = jugadores.head
    if actual is not None:
        while True:
            jugador = actual.data
            print(jugador)
            actual = actual.next
            if actual is jugadores.head:
                break
    print("Cartas de la maquina: " + str(mazo_maquina.length()))
    print("==========================================\n")


def robar_carta(jugador):
    if jugador.robos_usados >= 3:
        print("Ya utilizaste los 3 robos permitidos.")
        return False
    carta = random.randint(1, 10)
    jugador.mazo.agregar_al_final(carta)
    jugador.robos_usados += 1
    print(jugador.nombre + " robo la carta " + str(carta) + ".")
    print("Robos usados: " + str(jugador.robos_usados) + "/3")
    return True


def escoger_carta_jugador(jugador):
    while True:
        print("\nMazo de " + jugador.nombre + ":")
        mostrar_mazo(jugador.mazo)
        print("0. Robar/agregar una carta (si quedan robos)")
        opcion = pedir_entero("Elige la carta por numero, o 0 para robar: ",
                              0, jugador.mazo.length())
        if opcion == 0:
            if robar_carta(jugador):
                continue
            print("Debes escoger una de tus cartas actuales.")
            continue
        return quitar_carta_por_posicion(jugador.mazo, opcion - 1)


def jugar_batalla(jugador, mazo_maquina):
    """Juega una batalla. Los empates encadenan otra jugada."""
    puntos_posibles = 0
    numero_batalla = 1

    while jugador.mazo.length() > 0 and mazo_maquina.length() > 0:
        print("\n--- " + jugador.nombre + " | Batalla " + str(numero_batalla) + " ---")
        carta_jugador = escoger_carta_jugador(jugador)
        carta_maquina = quitar_carta_por_posicion(mazo_maquina, 0)

        if carta_jugador is None or carta_maquina is None:
            print("No quedan cartas suficientes para continuar la batalla.")
            return

        suma = carta_jugador + carta_maquina
        puntos_posibles += suma
        print(jugador.nombre + " juega " + str(carta_jugador))
        print("La maquina juega " + str(carta_maquina))
        print("Suma de esta pareja: " + str(suma))

        if carta_jugador > carta_maquina:
            jugador.puntos += puntos_posibles
            print("¡Gana " + jugador.nombre + " esta batalla!")
            print("Puntos obtenidos en la batalla: " + str(puntos_posibles))
            if suma == 10 and carta_jugador < carta_maquina:
                jugador.perder_proximo_turno = True
            return

        if carta_maquina > carta_jugador:
            print("Gana la maquina. El jugador no suma puntos.")
            if suma == 10 and carta_jugador < carta_maquina:
                jugador.perder_proximo_turno = True
                print(jugador.nombre + " perdera su proximo turno porque las cartas sumaron 10.")
            return

        print("¡Empate! Se acumula la suma y se juega otra carta.")
        numero_batalla += 1

    print("La batalla termina porque uno de los mazos se quedo sin cartas.")
    # Si no se rompe el empate, no se asignan puntos automáticamente.
    # Esto evita declarar un ganador sin una carta superior.


def mostrar_ganador(jugadores):
    if jugadores.head is None:
        print("No hay jugadores.")
        return
    mayor = jugadores.head.data.puntos
    actual = jugadores.head
    while True:
        if actual.data.puntos > mayor:
            mayor = actual.data.puntos
        actual = actual.next
        if actual is jugadores.head:
            break

    print("\n========== RESULTADO FINAL ==========")
    actual = jugadores.head
    ganadores = Lista_circular()
    while True:
        jugador = actual.data
        print(jugador.nombre + ": " + str(jugador.puntos) + " puntos")
        if jugador.puntos == mayor:
            ganadores.add_last(jugador.nombre)
        actual = actual.next
        if actual is jugadores.head:
            break

    if ganadores.length() == 1:
        print("GANADOR: " + str(ganadores.head.data))
    else:
        print("EMPATE entre los jugadores con " + str(mayor) + " puntos:")
        ganadores.mostrar_datos()
    print("=====================================")


def main():
    print("=" * 52)
    print("             GUERRA DE CARTAS")
    print("=" * 52)
    print("Cada jugador empieza con 5 cartas entre 1 y 10.")
    print("En cada turno puedes jugar una carta o robar una carta.")
    print("Cada jugador puede robar hasta 3 cartas durante toda la partida.")
    print("La maquina juega la primera carta de su mazo.")
    print("")

    jugadores = preparar_jugadores()
    mazo_maquina = preparar_mazo_maquina()
    mostrar_estado(jugadores, mazo_maquina)

    ronda = 1
    while jugadores.head is not None and mazo_maquina.length() > 0:
        print("\n" + "#" * 52)
        print("RONDA " + str(ronda))
        print("#" * 52)

        turno = jugadores.head
        # Se fija la cantidad de jugadores al iniciar la ronda.
        cantidad_jugadores = jugadores.length()
        for _ in range(cantidad_jugadores):
            jugador = turno.data
            siguiente_jugador = turno.next
            print("\nTURNO DE: " + jugador.nombre)

            if jugador.mazo.length() == 0:
                print(jugador.nombre + " no tiene cartas y no puede jugar.")
            elif jugador.perder_proximo_turno:
                print(jugador.nombre + " pierde este turno por la regla de la suma 10.")
                jugador.perder_proximo_turno = False
            else:
                jugar_batalla(jugador, mazo_maquina)

            print("Puntaje actual de " + jugador.nombre + ": " + str(jugador.puntos))
            turno = siguiente_jugador

        mostrar_estado(jugadores, mazo_maquina)

        # El juego termina si un jugador se queda sin cartas.
        actual = jugadores.head
        alguien_sin_cartas = False
        if actual is not None:
            while True:
                if actual.data.mazo.length() == 0:
                    alguien_sin_cartas = True
                actual = actual.next
                if actual is jugadores.head:
                    break

        if alguien_sin_cartas:
            print("La partida termina porque un jugador se quedo sin cartas.")
            break
        if mazo_maquina.length() == 0:
            print("La partida termina porque la maquina se quedo sin cartas.")
            break

        continuar = input("¿Desean jugar otra ronda? (s/n): ").strip().lower()
        if continuar != "s" and continuar != "si":
            print("La partida se detuvo por decision del usuario.")
            break
        ronda += 1

    mostrar_ganador(jugadores)


if __name__ == "__main__":
    main()
