import json
import re
import random as rd 
from barco import Barco
from tablero import Tablero
from datetime import datetime as dt
import os

def elegir_una_casilla(jugador):
    """
    La función pide al jugador que se pasa como argumento que introduzca 
    una casilla y comprueba que el formato sea el correcto. Si es así
    devuelve la cacailla introducida. 
    """
    print('\n')
    jugada = input(f"""
{jugador}, teclea las coordenadas para atacar. 
El formato es \"0x8\" con 0 para las filas y 8 para las columnas: """)
    patron_casilla = r'^([1-9]|10)x([1-9]|10)$'  
    
    while True:
        try:
            assert(re.search(patron_casilla, jugada))
            break
        except AssertionError:
            print('\n')
            print('La casilla introducida no está en el formato solicitado. Por favor introduce un valor tipo \"5x6\".')
            jugada = input ('Teclea las coordenadas para atacar: ')

    return jugada


def atacar(nombre, tablero_comprobar, tablero_mostrar):
    """
    La función pide por pantalla las coordenadas de una casilla a atacar, 
    compruebasu estado y muestra el resultado del ataque tanto en un tablero 
    a mostrar por pantallacomo en en el tablero donde se ubican los barcos. 
    """
    patron_numeros = r'\d\d|\d'
    jugada = elegir_una_casilla(nombre)
    casilla = [int(i) for i in re.findall(patron_numeros, jugada)]

    acierto = tablero_comprobar.comprobar_jugada(casilla)
    tablero_mostrar = tablero_mostrar.actualizar_jugada(acierto, casilla)
    tablero_comprobar = tablero_comprobar.actualizar_jugada(acierto, casilla)

    return tablero_comprobar, tablero_mostrar


def sortear_turno(jugador, contrincante):
    """
    La función genera dos números al azar, para dos jugadores que 
    se pasan como parámetro, y devuelve cuál de los dos ha sacado
    el número mayor.
    """
    while True:
        comienzo1 = rd.randint(1, 7)
        comienzo2 = rd.randint(1, 7)
        print(f'{jugador} ha sacado un {comienzo1}')
        print(f'{contrincante} ha sacado un {comienzo2}')
        if comienzo1 > comienzo2:
            primer_jugador = True
            print('\n')
            print(f'¡{jugador} empieza!')
            return primer_jugador
        elif comienzo1 < comienzo2:
            primer_jugador = False
            print('\n')
            print(f'¡{contrincante} empieza!')
            return primer_jugador
        else:
            print('\n')
            print('Los judadores han sacado el mismo número. Se vuelve a sortear')


def elegir_quien_sortea_turno(nombre_1, nombre_2):
    """
    La función sorte el inicio del turno y devuleve el resltado del sorteo.
    """
    while True:
        print('\n')
        print('Hay que sortear el comienzo del juego')
        lanzamiento = input('El que quiera lanzar el sorteo que escriba su nombre: ')
        if lanzamiento == nombre_1:
            print('\n')
            print(f'{nombre_1} lo lanza. ¡La suerte está echada!')
            primer_jugador = sortear_turno(nombre_1, nombre_2)
            return lanzamiento, primer_jugador
        elif lanzamiento == nombre_2:
            print('\n')
            print(f'{nombre_2} lo lanza. ¡La suerte está echada!')
            primer_jugador = sortear_turno(nombre_1, nombre_2)
            return lanzamiento, primer_jugador
        else:
            print('\n')
            print('El nombre introducido no es correcto')


def coloca_barco(barco, tablero):
    """
    La función pide que se coloque un barco por pantalla y devuelve el 
    tablero con el barco colocado.
    """
    while True:
        print(f'Elige la posición del {barco.nombre} {barco.casillas}')
        tabla, errores = barco.colocar_barco(tablero)
        if not errores: 
            tablero = tabla
            break
        else:
            print('\n')
            print(f'Has elegido una posición que ya tiene un barco. Tienes que volver a introducirla')
    
    return tablero


def colocar_todos_barcos(tablero):
    """
    La función coloca en el tablero pasado como argumento todos los 
    barcos con el imput de cada uno de ellos con coordenadas.
    """
    barcos_de_2 = [Barco(2, f'barco{i}') for i in range(1, 5)]
    barcos_de_3 = [Barco(3, f'barco{i}') for i in range(5, 9)]
    barcos_de_4 = [Barco(4, f'barco{i}') for i in range(9, 11)]
    barco_de_5 = [Barco(5, 'barco10')]
    todos_barcos = barcos_de_2 + barcos_de_3 + barcos_de_4 + barco_de_5

    for barco in todos_barcos:
        coloca_barco(barco, tablero)
        tablero.comprobar_tablero()


def elegir_opciones(jugador):
    """
    La función pregunta al jugador, que se pasa como argumento,
    qué opición prefiere para elegir el tablero de juego. Una
    vez elegida se devuelve el tablero.
    """
    print('\n')
    print(f"""Qué opción eliges, {jugador}:
        1. Elegir la posición de los barcos
        2. Cargar una configuración de barcos ya guardada
        3. Coloca todos los barcos de manera aleatoria""")

    while True:
        print('\n')
        opcion = input('Introduce la opicón que prefieres: ')

        if opcion == '1':
            print('\n')
            print(f"""   
{jugador}, has de escribir "4h9:10" si quieres insertar en la 4a fila, en horizontal y ocupando las dos últimas columnas.
Has de escribir "8h1:2" si quieres insertar en la 8a fila, en horizontal y ocupando las dos primeras columnas.
Siempre se colocarán las coordenadas de irquierda a derecha y de arriba abajo""")
            print('\n')
            tablero = Tablero(10, 10, jugador)
            colocar_todos_barcos(tablero)
            tablero.guarda_json(f'{jugador}_tablero_actual')
            now = dt.now()
            tablero.guarda_json(f'Estado_inicial_{jugador}_{now.day}_{now.hour}_{now.minute}')
            return tablero

        elif opcion == '2':
            while True:
                print('\n')
                ruta = os.path.dirname(__file__) + os.sep + 'Partidas_Batalla_naval'
                print(os.listdir(ruta))
                print('\n')
                archivo = input('Introduce el nombre del archivo que quieres cargar: ')
                try:
                    tablero = Tablero(10, 10, jugador)
                    tablero.abrir_json(archivo, jugador)
                    tablero.guarda_json(f'{jugador}_tablero_actual')
                    tablero.comprobar_tablero()
                    return tablero
                except Exception:
                    print('El archivo no está en la lista')

        elif opcion == '3':
            tablero = Tablero(10, 10, jugador)
            colocar_todos_barcos_aleatorios(tablero)
            tablero.guarda_json(f'{jugador}_tablero_actual')
            now = dt.now()
            tablero.guarda_json(f'Estado_inicial_{jugador}_{now.day}_{now.hour}_{now.minute}')
            tablero.comprobar_tablero()
            return tablero

        else:
            print('La opción introducida no está en la lista')


def colocar_todos_barcos_aleatorios(tablero):
    """
    Coloca todos los barcos de manera aleatoria
    """
    barcos_de_2 = [Barco(2, f'barco{i}') for i in range(1, 5)]
    barcos_de_3 = [Barco(3, f'barco{i}') for i in range(5, 9)]
    barcos_de_4 = [Barco(4, f'barco{i}') for i in range(9, 11)]
    barco_de_5 = [Barco(5, 'barco10')]
    todos_barcos = barcos_de_2 + barcos_de_3 + barcos_de_4 + barco_de_5

    for barco in todos_barcos:
        barco.colocar_barco_aleatorio(tablero)


def generar_titulo():
    """
    La función genera el título del juego por pantalla.
    """
    os.system('clear')
    print('############################################################')
    print('#                                                          #')
    print('#      Comienza la batalla de barcos: HUNDIR LA FLOTA      #')
    print('#                                                          #')
    print('############################################################')
    print('\n')


def generar_ganador(jugador):
    """
    La función genera el título de ganador del final del juego.
    """
    print('\n')
    jugador = jugador.upper()
    print(f""" 
#############################################################
#                  ¡¡{jugador} GANA!!                       #
#############################################################""")
    print('\n')
    print('\n')

