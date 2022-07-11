import pandas as pd 

class Conversor:

    def __init__(self):
        self.unidad = 'EUR'
        self.tipo = type(str)


    def prepara_divisa_para_conversion(self, x):
        return str.split(x) if pd.notnull(x) else x


    def cambio_divisa(self, lista_divisa):
        """
        Convierte de una lista de divisa y cantidad a dolares
        todas las cantidades.
        NOTA: PARA LOS CAMBIOS DE DIVISA SE CONSIDERA EL CAMBIO 
        ACTUAL A DÍA 21 DE MAYO.
        """
        if lista_divisa[0] == 'KRW':  # won surcoreano
            lista_divisa[1] = int(int(lista_divisa[1]) * 0.00073)  
            return lista_divisa[1]
        elif lista_divisa[0] == '$': # dolar estadounidense
            lista_divisa[1] = int(int(lista_divisa[1]) * 0.82)
            return lista_divisa[1]
        elif lista_divisa[0] == 'RUR': # rublo ruso
            lista_divisa[1] = int(int(lista_divisa[1]) * 0.011)
            return lista_divisa[1]
        elif lista_divisa[0] == 'GBP': # libra esterlina
            lista_divisa[1] = int(int(lista_divisa[1]) * 1.16)
            return lista_divisa[1]
        elif lista_divisa[0] == 'SGD': # dolar de singapur
            lista_divisa[1] = int(int(lista_divisa[1]) * 0.62)
            return lista_divisa[1]
        elif lista_divisa[0] == 'NOK': # corona noruega
            lista_divisa[1] = int(int(lista_divisa[1]) * 0.099)
            return lista_divisa[1]
        elif lista_divisa[0] == 'BRL': # real brasileño
            lista_divisa[1] = int(int(lista_divisa[1]) * 0.15)
            return lista_divisa[1]
        elif lista_divisa[0] == 'JPY': # yen
            lista_divisa[1] = int(int(lista_divisa[1]) * 0.0075)
            return lista_divisa[1]
        elif lista_divisa[0] == 'INR': # rupia india
            lista_divisa[1] = int(int(lista_divisa[1]) * 0.011)
            return lista_divisa[1]
        elif lista_divisa[0] == 'HKD': # dólar honkonés
            lista_divisa[1] = int(int(lista_divisa[1]) * 0.11)
            return lista_divisa[1]
        elif lista_divisa[0] == 'FRF': # franco francés
            lista_divisa[1] = int(int(lista_divisa[1]) * 0.15245)
            return lista_divisa[1]
        elif lista_divisa[0] == 'CAD': # dólar canadiense
            lista_divisa[1] = int(int(lista_divisa[1]) * 0.68)
            return lista_divisa[1]
        elif lista_divisa[0] == 'AUD': # dólar australiano
            lista_divisa[1] = int(int(lista_divisa[1]) * 0.64)
            return lista_divisa[1]
        elif lista_divisa[0] == self.unidad:
            lista_divisa[1] = int(lista_divisa[1])
            return lista_divisa[1]


    def cambiar_divisa(self, x):
        lista_divisa = self.prepara_divisa_para_conversion(x)
        return x if not isinstance(lista_divisa, list) else self.cambio_divisa(lista_divisa)

    
    def conversion_columna(self, df, columna):
        df[columna] = df[columna].apply(self.cambiar_divisa)

    
    def columna_a_entero(self, df, columna):
        df[columna] = df[columna].astype(int)