

def round_half_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.49) / multiplier


def pareados(texto):
    pares = {"{": "}", "(": ")", "[": "]"}
    caracteres = []
    resultados = []
    for caracter in texto:
        if caracter in pares.keys():
            resultados.append(caracter)
        elif len(resultados) != 0 and caracter == pares[resultados[-1]]:
            resultados.pop()
        else:
            return False
    return len(resultados) == 0
        