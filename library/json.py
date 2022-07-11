import os
import re
import json


def abrir_archivo_json(archivo, ruta=None):
    """
    Te permite abrir un archivo json desde el mismo nivel
    o en niveles por debajo del archivo acutal
    Se le pasa por parámetro el archivo y opcionalmente la ruta
    de bajada.
    """
    ruta = os.path.dirname(__file__) + os.sep + ruta + os.sep + archivo
    with open(ruta, 'r+') as outfile:
            archivo_abierto = json.load(outfile)

    return archivo_abierto


def abrir_archivo_json_subiendo_primero(archivo, ruta_hacia_arriba=None):
    """
    Te permite abrir un archivo json en una carpeta hacia arriba en el arbol
    dándole como parámetro la ruta desde la caperta a la que tienes que subir y 
    el archivo que quieres abrir.
    """
    patron = '/'
    subir = len(re.findall(patron, ruta_hacia_arriba))

    ruta = __file__
    for i in range(subir + 1):
        ruta = os.path.dirname(ruta)
    
    abrir_archivo_json(archivo, ruta)

    return archivo_abierto


def guarda_json(nombre_archivo):
    """
    La función guarda un diccionario como argumento
    en archivo json con el mismo nombre.
    """
    ruta = os.path.dirname(__file__) + os.sep + nombre_archivo

    with open(ruta, 'w+') as outfile:
        json.dump(nombre_archivo, outfile, indent=4)