from sklearn import preprocessing
import pandas as pd


def encoder(data):
    le = preprocessing.LabelEncoder()
    le.fit_transform(data) 
    return le


def decoder(data, le):
    t = le.inverse_transform(data)
    return list(t)


"""
SOLUCIONES PARA EVITAR LAS CORRELACIONES 
Y QUE CONSIDERE QUE UNO ES EL DOBLE QUE EL OTRO:


- VALORES MUY PEQUEÑOS O MUY GRANDES!!

- SIEMPRE DIFERENTE ENTE DIFERENTES ENCODERS SI NO 
ENCONTRARÁ PATRONES ENTRE LAS COLUMNAS!!

"""


def encoder_dummies(df):
    """
    Convierte todas las columnas categóricas a una 
    matriz(columnas) de ceros y unos para cada opción.
    """
    df = pd.get_dummies(df)



class MyLabelEncoder(LabelEncoder):
    """
    Ejemplo:
    le = MyLabelEncoder()
    le.fit(['b', 'a', 'c', 'd' ])
    le.classes_
    #Output:  array(['b', 'a', 'c', 'd'], dtype=object)
    """

    def fit(self, y):
        y = column_or_1d(y, warn=True)
        self.classes_ = pd.Series(y).unique()
        return self



def categorizar_numerica(df, columna, bins, labels=None):
    """
    bins como número de rangos o como limites de los 
    rangos para rangos irregulares. Labels como nombre de los
    intervalos si se quiere.
    """
    df[columna] = pd.cut(df[columna], bins, labels=labels)