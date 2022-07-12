import re
import random as rd 


class Barco:
    """
    Pasada la longitud y nombre del jugador que lo va a usar,
    genera un barco con el número de casillas que ocupa.
    Posee los métodos para pedir una posición, para comprobar
    que esa posición coincide con su longitud y para colocarse
    tanto por coordenadas como aleatoriamente.
    """
    def __init__(self, longitud, nombre):
        self.longitud = longitud
        self.nombre = nombre
        self.casillas = f'({longitud}x1)'


    def posicion_barco(self):
        """
        Pide la posición del barco por pantalla y comprueba que tenga el formato adecuado.
        Devuelve la posición del barco:
        """
        barco = input ('Teclea la posición elegida: ')
        patron= r'^([1-9]|10)[vh][1-9]:([1-9]|10)$'
    
        while True:
            try:
                assert(re.search(patron, barco))
                break
            except AssertionError:
                print('\n')
                print('La posición introducida no está en el formato solicitado. Por favor introduce un valor tipo \"4h9:10\".')
                barco = input ('Teclea la posición elegida: ')

        return barco


    def posicion_y_logitud_barco(self):
        """
        La función recoge los números de una entrada por pantalla(fila o columna y las casillas)
        Cálcula la longitud para comprobar que coincide con la solicitada como parámetro y devuelve 
        las posiciones del tablero y si se colocar en horizontal o vertical.
        """
        patron_numeros = r'\d\d|\d'

        while True:
            barco = self.posicion_barco()

            posiciones_numericas = [int(i) for i in re.findall(patron_numeros, barco)]  
            longitud_barco = len(range(posiciones_numericas[1], posiciones_numericas[2] + 1))  

            if longitud_barco == self.longitud:                 
                patron_v_vs_h = r'v|h'
                v_vs_h = re.findall(patron_v_vs_h, barco)
                return posiciones_numericas, v_vs_h
            else:
                print('\n')
                print(f'El barco no tiene la longitud necesaria. Tiene que ocupar {self.longitud} casillas. Introduce el barco de nuevo')


    def colocar_barco(self, tablero):
        """
        Pide que se coloque un barco en el tablero, representándolo con * en el lugar dónde se
        encuentra, en vez de agua (~). Si coincide con otro barco en alguna casilla devuelve una
        bandera con el error. Devuelve también el tablero, modificado si ha sido posible.
        """
        posiciones_numericas, v_vs_h = self.posicion_y_logitud_barco()
        
        if v_vs_h[0] == 'v':
            filas = range(posiciones_numericas[1], posiciones_numericas[2] + 1)
            columnas = posiciones_numericas[0]
            casillas = [(i, columnas) for i in filas]
            tablero, errores = tablero.actualizar_barco(casillas)
            if not errores:
                print(casillas)
                print('\n')
                print('Tu barco se situa en el tablero.')

        elif v_vs_h[0] == 'h':
            filas = posiciones_numericas[0]
            columnas = range(posiciones_numericas[1], posiciones_numericas[2] + 1)
            casillas = [(filas, i) for i in columnas]   
            tablero, errores = tablero.actualizar_barco(casillas)
            if not errores:
                print(casillas)
                print('\n')
                print('Tu barco se situa en el tablero.')
        
        return tablero, errores


    def colocar_barco_aleatorio(self, tablero):
        """
        Coloca un barco aleatoriamente en el tablero
        """
        while True:
            inicio = list((rd.randint(1, 10), rd.randint(1,10)))
            posibles_orientaciones = ['n', 's', 'e', 'o']
            orientacion = rd.choice(posibles_orientaciones)
            if orientacion == 'v':
                filas = range(inicio[0], inicio[0] + self.longitud)
                if filas[-1] > 10:
                    continue
                columnas = inicio[1]
                casillas = [(i, columnas) for i in filas]
                tabla, errores = tablero.actualizar_barco(casillas)
                if not errores:
                    tablero.tablero = tabla
                    return tablero

            elif orientacion == 'n':
                filas = range(inicio[0] - self.longitud, inicio[0])
                if filas[0] < 1:
                    continue
                columnas = inicio[1]
                casillas = [(i, columnas) for i in filas]
                tabla, errores = tablero.actualizar_barco(casillas)
                if not errores:
                    tablero.tablero = tabla
                    return tablero

            elif orientacion == 'h':
                filas = inicio[0]
                columnas = range(inicio[1], inicio[1] + self.longitud)
                if columnas[-1] > 10:
                    continue
                casillas = [(filas, i) for i in columnas]
                tabla, errores = tablero.actualizar_barco(casillas)
                if not errores:
                    tablero.tablero = tabla
                    return tablero

            else: 
                filas = inicio[0]
                columnas = range(inicio[1] - self.longitud, inicio[1])
                if columnas[0] < 1:
                    continue
                casillas = [(filas, i) for i in columnas]
                tabla, errores = tablero.actualizar_barco(casillas)
                if not errores:
                    tablero.tablero = tabla
                    return tablero