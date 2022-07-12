from barco import Barco
from tablero import Tablero
import acciones as acciones
from datetime import datetime as dt 


acciones.generar_titulo()

nombre_1 = input('Introduce el nombre del primer jugador: ')
nombre_2 = input('Introduce el nombre del segundo jugador: ')


tablero_1 = acciones.elegir_opciones(nombre_1)
tablero_2 = acciones.elegir_opciones(nombre_2)


tablero_comprobar_1 = Tablero(10, 10, f'{nombre_2}')
tablero_comprobar_1.abrir_json(f'{nombre_2}_tablero_actual', nombre_2)

tablero_comprobar_2 = Tablero(10, 10, f'{nombre_1}')
tablero_comprobar_2.abrir_json(f'{nombre_1}_tablero_actual', nombre_1)


tablero_mostrar_1 = Tablero(10, 10, f'{nombre_2}')
tablero_mostrar_2 = Tablero(10, 10, f'{nombre_1}')


lanzamiento, primer_jugador = acciones.elegir_quien_sortea_turno(nombre_1, nombre_2)


while True:
    if (lanzamiento == nombre_1 and primer_jugador) or (lanzamiento == nombre_2 and not primer_jugador):
        acciones.atacar(nombre_1, tablero_comprobar_1, tablero_mostrar_1)
        now = dt.now()
        tablero_comprobar_1.guarda_json(f'{nombre_1}_{now.day}_{now.hour}_{now.minute}')
        tablero_mostrar_1.comprobar_evolucion_juego(tablero_comprobar_2)
        aciertos = tablero_comprobar_1.comprobar_estado_aciertos()
        if aciertos < 33:
            acciones.atacar(nombre_2, tablero_comprobar_2, tablero_mostrar_2)
            now = dt.now()
            tablero_comprobar_2.guarda_json(f'{nombre_2}_{now.day}_{now.hour}_{now.minute}')
            tablero_mostrar_2.comprobar_evolucion_juego(tablero_comprobar_1)
            aciertos = tablero_comprobar_2.comprobar_estado_aciertos()
            if aciertos >=33:
                acciones.generar_ganador(nombre_2)
                break
        else:
            acciones.generar_ganador(nombre_1)
            break
    else:
        acciones.atacar(nombre_2, tablero_comprobar_2, tablero_mostrar_2)
        now = dt.now()
        tablero_comprobar_2.guarda_json(f'{nombre_2}_{now.day}_{now.hour}_{now.minute}')
        tablero_mostrar_2.comprobar_evolucion_juego(tablero_comprobar_1)
        aciertos = tablero_comprobar_2.comprobar_estado_aciertos()
        if aciertos < 33:
            acciones.atacar(nombre_1, tablero_comprobar_1, tablero_mostrar_1)
            now = dt.now()
            tablero_comprobar_1.guarda_json(f'{nombre_1}_{now.day}_{now.hour}_{now.minute}')
            tablero_mostrar_1.comprobar_evolucion_juego(tablero_comprobar_2)
            aciertos = tablero_comprobar_1.comprobar_estado_aciertos()
            if aciertos >= 33:
                acciones.generar_ganador(nombre_1)
                break
        else:
            acciones.generar_ganador(nombre_2)
            break
