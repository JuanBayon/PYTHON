import pandas as pd

class Estadistico():
    """
    Objeto estdístico que calcula los outliers y el propiod Dataframe
    sin ellos como argumentos propios.
    EL CRITERIO GENERALIZADO DE 1,5 EL RANGO INTERCUARTILÍTICO POR ENCIMA 
    Y POR DEBAJO ES EL QUE TOMO COMO REFERENCIA PARA REPRESENTARLOS. 
    """

    def __init__(self, df):
        self.df = df
        self.outliers, self.df_sin_outliers = self._get_outliers_and_not(df)


    def solo_numericas(self):
        """
        Se queda con las columnas que son númericas y devuelve el
        dataframe.
        """
        df_solo_numericas = self.df.select_dtypes(include='number')
        return df_solo_numericas


    def _get_outliers_and_not(self, df):
        """
        Dado un dataframe devuelve los otliers separados
        y el dataframe sin ellos. 
        """
        df_solo_numericas = self.solo_numericas()

        Q1 = df_solo_numericas.quantile(0.25)
        Q3 = df_solo_numericas.quantile(0.75)
        IQR_RIC = Q3 - Q1
        limite_inferior = (Q1 - 1.5 * IQR_RIC)
        limite_superior = (Q3 + 1.5 * IQR_RIC)

        outliers = df_solo_numericas[((df_solo_numericas < limite_inferior) | (df_solo_numericas > limite_superior)).any(axis=1)]
        df_sin_outliers = df[~((df_solo_numericas < limite_inferior) | (df_solo_numericas > limite_superior)).any(axis=1)]

        return outliers, df_sin_outliers



class Calculadora_estadistica(Estadistico):

    def __init__(self, df):
        super().__init__(df)
        

    def calcula_daframe_opcion(self, columna, opcion, mask=None):
        if isinstance(mask, pd.Series):
            df = self.df[mask]
        else:
            df = self.df
        return df[df[f'{columna}'].astype(str).str.contains(f'\w*{opcion}\w*')]


    def calcula_ratio_ganancias(self, columna, opcion, mask=None):
        elemento = self.calcula_daframe_opcion(columna, opcion, mask)
        return int(elemento['worlwide_gross_income'].mean())

    
    def calcula_votacion_media(self, columna, opcion, mask=None):
        elemento = self.calcula_daframe_opcion(columna, opcion, mask)
        return round(elemento['imdb_ratings'].mean(), 1)


    def calcula_frecuencia_absoluta(self, columna, opcion, mask=None):
        elemento = self.calcula_daframe_opcion(columna, opcion, mask)
        return int(elemento.shape[0])


    def calcula_todos_ratios_ganancias(self, columna, dummie=False, valoracion=False, conteo=False, mask=None):
        if dummie and isinstance(mask, pd.Series):
            df = self.df[mask]
            lista = list(df[f'{columna}'].str.get_dummies().sum().index)
        elif dummie:
            lista = list(self.df[f'{columna}'].str.get_dummies().sum().index)
        elif isinstance(mask, pd.Series):
            df = self.df[mask]
            lista = list(df[f'{columna}'].unique())
        else:
            lista = list(self.df[f'{columna}'].unique())
        
        dict = {}
        for opcion in lista:
            ratio = self.calcula_ratio_ganancias(columna, opcion, mask)
            if (conteo and valoracion):
                val = self.calcula_votacion_media(columna, opcion, mask)
                casos = self.calcula_frecuencia_absoluta(columna, opcion, mask)
                dict[opcion] = list((ratio, val, casos))
            elif valoracion:
                val = self.calcula_votacion_media(columna, opcion, mask)
                dict[opcion] = list((ratio, val))
            elif conteo:
                casos = self.calcula_frecuencia_absoluta(columna, opcion, mask)
                dict[opcion] = list((ratio, casos))
            else:  
                dict[opcion] = ratio

        return dict


    def agrupado_ganancias(self, columna, dummie=False, valoracion=False, conteo=False, mask=None):
        dict = self.calcula_todos_ratios_ganancias(columna, dummie, valoracion, conteo, mask)
        if (valoracion and conteo):
            return pd.DataFrame(dict, index=['worlwide_gross_income', 'imdb_mean_vote', 'quantity']).T.sort_values(by='worlwide_gross_income', ascending=False)
        elif valoracion:
            return pd.DataFrame(dict, index=['worlwide_gross_income', 'imdb_mean_vote']).T.sort_values(by='worlwide_gross_income', ascending=False)
        elif conteo:
            return pd.DataFrame(dict, index=['worlwide_gross_income', 'quantity']).T.sort_values(by='worlwide_gross_income', ascending=False)
        
        else:
            return pd.DataFrame(dict, index=['worlwide_gross_income']).T.sort_values(by='worlwide_gross_income', ascending=False)


    def valores_unicos_columnas(self):
        for column in list(self.df.columns):
            unicos = self.df[column].nunique()
            print(f'La columna {column} tiene {unicos} valores no repetidos')