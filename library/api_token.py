import json
import requests

def api(url, params):
    """
    Hace un request a, con los parámetros de la API, 
    y devuleve un json para cargar en un dataframe.
    """
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return data