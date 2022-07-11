import collections
import pandas as pd
from tqdm import tqdm
from pandas_profiling import ProfileReport
import numpy as np 


"""
import warnings
warnings.filterwarnings('ignore')

"""



def interpolate(pd_series, method=None):
    """
    s = pd.Series([0, 2, np.nan, 5])
    """
    if method == 'pad':
        pd_series.interpolate(method="pad")
    if method == 'nearest':
        pd_series.interpolate(method="nearest")
    if method == 'quadratic':
        pd_series.interpolate(method="quadratic")
    if method == 'polinomic':
        pd_series.interpolate(method="polinomic")
    else:
        pd_series.interpolate()



def separa_rangos_dataframe(df, columna, rangos):
    columna_rangos =  pd.cut(df[columna], rangos)
    return columna_rangos


def percent_nan(df):
    percent_missing = df.isnull().sum() * 100 / len(df)
    missing_value_df = pd.DataFrame({'column_name': df.columns, 'percent_missing': percent_missing})
    return missing_value_df


def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop



def get_top_abs_correlations(df, n=5):
    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]



def separar_columnas_dataframe_comascolumnaunica(df):
    """
    Separa en columnas un dataframe que tiene todos los valores
    en una única columna separados por comas. 
    """
    new_df = df.iloc[0].str.split(',', expand=True)

    for i in range(1, df.shape[0]):
        b = df.iloc[i].str.split(',', expand=True)
        new_df = new_df.append(b, ignore_index=True)

    return new_df


def encontrar_string_repetido(df, columna):
    """
    Devuelve los valores repetidos de una columna de strings
    en un dataframe, dados como argumentos.
    """
    strings = list(df[f'{columna}'].values)
    answer = [item for item, count in collections.Counter(strings).items() if count > 1]
    return answer


def try_convert_to_int(x):
    """
    The function shows in the screen the rare values 
    that aren't integers.
    """
    try:
        return int(x)
    except:             
        print("Rare value:", x)  
        return x


def busca_opcion(df, column, opcion):
    """
    Si le das una columna y un daframe con opciones, 
    devulve la máscara con las entradas que contienen
    la opción
    """
    mask = df[f'{column}'].str.match(f'\w*{opcion}\w*')
    return mask


def profile_report(df):
    pr = ProfileReport(df, title='Pandas Profiling Report')
    return pr


def tqdm(iterable, enumerate=False):
    """
    Añade un texto en cada iteración de un for.
    """
    if enumerate:
        #for i2,(indice, variable) in tqdm(enumerate(iterable), total=iteraciones_total, desc=Texto de la iteración: "Small train progress" + i/len(total))
        pass
    else:
        pass


def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]