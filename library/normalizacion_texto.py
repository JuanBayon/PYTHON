import unicodedata

def normalizacion(texto):
    """
    ejemplo = 'Pingüino: Málaga es una ciudad fantástica y en Logroño me pica el... moño'
    """

    texto_modificado = unicodedata.normalize("NFKD", texto).encode("ascii","ignore").decode("ascii")
    return texto_modificado
