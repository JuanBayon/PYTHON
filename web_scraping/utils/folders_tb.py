import os
import pandas as pd 
import pickle
import json


class Gestor_archivos():

    def read_json(self, fullpath):
        """
        The function reads a json given the full path with the file
        at the end and returns a variable wiht the dictionary
        """
        with open(fullpath, "r") as json_file_readed:
            json_readed = json.load(json_file_readed)
        return json_readed


    def load_json(self, name, fullpath):
        """
        The function writes a json file given a dictironary and
        the full path where you want to save it. 
        """
        with open(fullpath, 'w+') as outfile:
            json.dump(name, outfile, indent=4)

    
    def cargar_df(self, ruta):
            return pd.read_csv(ruta)
    

    def guardar_csv(self, df, ruta, nombre):
        df.to_csv(ruta + os.sep + 'data' + os.sep + nombre, index=False)


    def guarda_pickle(self, variable, path, nombre):
        full_path = path + os.sep + nombre
        pickle.dump( variable, open(full_path, "wb" ))


    def carga_pickle(self, path, nombre):
        full_path = path + os.sep + nombre
        return pickle.load(open(full_path, "rb" ))


