import os, sys
import pandas as pd 

ruta = __file__
for i in range (3):
    ruta = os.path.dirname(ruta)

sys.path.append(ruta)

from scr.utils.apis_tb import Gestor_json

class Gestor_archivos(Gestor_json):
    """

    """
    def cargar_df(self, ruta):
            return pd.read_csv(ruta)
    

    def guardar_csv(self, df, ruta, nombre):
        df.to_csv(ruta + os.sep + 'data' + os.sep + nombre, index=False)

