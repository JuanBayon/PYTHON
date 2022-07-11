import pandas as pd

class Organizador_dataframe():


    def cambios_previos(self, df, nombre_col_pelicula):
        df.rename(columns={nombre_col_pelicula: 'film'}, inplace=True)
        df['film'] = df[['film']].applymap(str.lower)


    def union_dataframe(self, df1, df2):
        df_unido = pd.merge(df1, df2)
        return df_unido


    def eliminar_columnas(self, df, columnas):
        df.drop(columns=columnas, inplace=True)


    def renombra_columnas(self, df, cambios):
        df.rename(columns=cambios, inplace=True)


    def eliminar_nan_columnas(self, df, columnas):
        for i in columnas:
            df = df[df[i].notna()]
        return df

    
    def rellena_nan(self, df, columna=False, toado=None, median=False, mean=False):
        if columna:
            if median:
                df[columna].fillna(df[columna].median(), inplace=True)
            elif mean:
                df[columna].fillna(df[columna].mean(), inplace=True)
        elif todo:
            if median:
                df.fillna(round(df.median(), 1), inplace=True)
            elif mean:
                df.fillna(round(df.mean(), 1), inplace=True)


    def convierte_dummies(self, df, columna, sep):
        df[columna] = df[columna].apply(lambda x: x.replace(sep, '|'))


    def comprueba_valores_raros(self, x):
        """
        Muestra por pantalla si hay algún valor raro
        que no se pueda convertir.
        """
        try:
            int(x)
        except:             
            print("Rare value:", x) 


    def sustitucion_valor_raro(self, df, valor, valor_sustitucion, columna=None, dummie=False):
        if not columna:
            df.replace(valor, valor_sustitucion, inplace=True)
        else:
            if dummie:
                df[columna] = df[columna].str.replace(valor, valor_sustitucion, regex=False)
            else:
                df[columna].replace(valor, valor_sustitucion, inplace=True)

    
    def valores_repetidos(self, df, estudio=False, elimina=False, columna=None):
        if estudio:
            if columna:
                unicos = df[columna].nunique()
                repetidos = df.shape[0] - unicos
                print(f'El dataframe tiene {repetidos} entradas repetidas en la columna {columna}')
            else:
                repetidos = df[df.duplicated()].shape
                print(f'El dataframe tiene {repetidos[0]} entradas repetidas')
        if elimina:
            if columna:
                peliculas_repetidas = df[columna].value_counts()[df[columna].value_counts() != 1].index
                df = df[df[columna].apply(lambda x: x not in peliculas_repetidas)]
                return df
            else:
                df = df[~df.duplicated()]
                return df


    def retira_valores_extremos(self, df, columna, limite, superior=True):
        if superior:
            df = df[df[columna] < limite]
            return df
        else: 
            df = df[df[columna] > limite]
            return df
    
    def agrupa_columnas(self, df, col_inicio, col_final, *args, separadas=False):
        if not separadas:
            return df.loc[:, col_inicio: col_final]
        else:
            return df[[col_inicio, col_final, *args]]


    def agrupa_dummies(self, df, columna):
        return df[columna].str.get_dummies().sum().sort_values(ascending=False)

    
    def consulta_valor_concreto(self, df, columna, valor):
        cantidad = df[df[columna] == valor][columna].count()
        print(f'En la muestra hay {cantidad} entradas con el valor {valor}')


    def elimina_valores_longitud(self, df, columna, longitud):
        return df[~(df[columna].apply(len) > longitud)]


    def agrupa(self, df, columna):
        df.gropby(columna).mean()