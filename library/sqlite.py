import sqlite3
import pandas as pd

def conectar_bbdd(path):
    """
    Crea una conexión con una base de datos y su cursor para
    una ruta dada como argumento.
    """
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    return connection, cursor


def sql_query(query, cursor):
    """
    Devuelve el dataframe de una consulta a la base de datos.
    Se pasa como como argumentos la consulta y el cursor.
    """
    cursor.execute(query)
    datos_query = cursor.fetchall()
    col_names = [description[0] for description in cursor.description]
    return pd.DataFrame(datos_query, columns=col_names)