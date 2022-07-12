import json
import pandas as pd
import numpy as np 
import random as rd 
import os


class Tablero:
    """
    La clase tablero genera un tablero con un numero de filas y 
    columnas pasados como argumentos, así como el nombre del 
    jugador asociado. Posee los métodos para comprobar su estado, 
    comprobar una jugada introducida, actualizar un barco o una
    jugada, comprobar la evolución de los aciertos o del juego y
    abrir y guardar su estado en un archivo json.
    """
    def __init__(self, columnas, filas, nombre):
        self.columnas = columnas
        self.filas = filas
        self.nombre = nombre

        fila = ['~'] * self.filas
        tablero = {i: fila for i in range(1, self.columnas + 1)}
        index = list(range(1,11))
        tablero = pd.DataFrame(tablero, index=index)

        self.tablero = tablero


    def comprobar_tablero(self):
        """
        Muestra por pantalla el estado del tablero.
        """
        print('\n')
        print(f'El estado actual de {self.nombre} es: \n')
        print(self.tablero, '\n')


    def comprobar_jugada(self, casilla):
        """
        Comprueba si una jugada es acertada o no y devuelve el reslutado.
        """
        if self.tablero.loc[casilla[0]][casilla[1]] == '#':
            acierto = 'barco'
            print('\n')
            print('¡Acierto! El disparo ha dado en un barco')
        elif self.tablero.loc[casilla[0]][casilla[1]] == '~':
            acierto = 'agua'
            print('\n')
            print('El disparo ha dado en agua')
        else:
            acierto = 'ya atacado'
            print('\n')
            print('La casilla elegida ya se había bombardeado')

        return acierto


    def actualizar_jugada(self, acierto, casilla):
        """
        El tablero actualiza el tablero con el resultado de la 
        jugada, ambos como argumentos.
        """
        if acierto == 'barco':
            self.tablero.loc[casilla[0]][casilla[1]] = 'x'
        elif acierto == 'agua':
            self.tablero.loc[casilla[0]][casilla[1]] = 'o'

        return self.tablero


    def actualizar_barco(self, casillas):
        """
        La función actualiza el tablero con la posición del barco si 
        no había uno previamente, y devulve un estado de error por 
        si ya había un barco en alguna de las casillas pasadas como 
        argumento.
        """
        errores = False
        for casilla in casillas:
            if self.tablero.loc[casilla[0]][casilla[1]] == '#':
                errores = True
                break
        if not errores:
            for casilla in casillas:
                self.tablero.loc[casilla[0]][casilla[1]] = '#'  
        
        return self.tablero, errores

    
    def guarda_json(self, nombre_archivo):
        """
        La función guarda en un archivo json su estado.
        """
        ruta = os.path.dirname(__file__) + os.sep + 'Partidas_Batalla_naval' + os.sep + nombre_archivo

        with open(ruta, 'w+') as outfile:
            tablero_json= self.tablero.to_dict(orient='list')
            json.dump(tablero_json, outfile, indent=4)


    def abrir_json(self, archivo, jugador):
        """
        La función carga como estado una judagada previa
        desde un archivo json.
        """
        ruta = os.path.dirname(__file__) + os.sep + 'Partidas_Batalla_naval' + os.sep + archivo
        with open(ruta, 'r+') as outfile:
            partida = json.load(outfile)
        tablero_guardado = pd.DataFrame.from_dict(partida)
        tablero_guardado.rename(index=dict(zip(range(0,10), range(1,11))), inplace=True)
        self.tablero = tablero_guardado

        return self.tablero


    def comprobar_estado_aciertos(self):
        """
        Cuenta el número de aciertos del tablero
        y los devuelve.
        """
        aciertos =  self.tablero[self.tablero == 'x'].count().sum()
        return aciertos


    def comprobar_evolucion_juego(self, tablero_contrincante):
        """
        Dado el tablero del cotrincante como argumento muestra
        por pantalla la evolución de tu tablero y de tus aciertos.
        """
        print(f"""
###################################################
#                                                 #
#     AQUI TIENES EL RESUMEN DE TU JUGADA         #
#                                                 #""")
        aciertos = self.comprobar_estado_aciertos()
        self.comprobar_tablero()
        print(f"""
Llevas {aciertos} aciertos""")
        aciertos = tablero_contrincante.comprobar_estado_aciertos()
        tablero_contrincante.comprobar_tablero()
        print(f"""
{self.nombre} lleva {aciertos} aciertos""")

        print("""
###################################################""")