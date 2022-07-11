import argparse
import sys


class Parser():

    def __init__(self):
        self.parser = self.crear_parser()

    def crear_parser(self):
        """
        Crea un parser para definir argumentos a pasar por
        consola al ejecutar el programa y lo retorna.
        """
        parser = argparse.ArgumentParser()
        return parser


    def agregar_argumento(self, numero, tipo:list):
        """
        Añade el número de argumentos que se quiera, pasado además el parser
        y la lista con los tipos de cada argumento.
        """
        for i in range(numero):
            self.parser.add_argument("-x", "--x", type=tipo[i], help="Password")


    def recoger_argumentos(self):
        """
        Recoge los argumentos pasados por consola al ejecutar
        el programa y los retorna.
        """
        args = vars(self.parser.parse_args())
        return args

    
    def recoger_argumentos_sys(self, numero):
        """
        Recoge los argumentos pasados por la consola, pasado como argumento
        su número. Devuelve la rura del archivo y los argumentos. 
        """
        ruta = sys.argv[0]
        variables = [sys.argv[i] for i in range(1, numero)]
        return ruta, variables