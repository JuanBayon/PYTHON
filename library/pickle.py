import pickle

def guarda_pickle(variable, full_path):
    pickle.dump( variable, open(full_path, "wb" ))


def carga_pickle(full_path):
    return pickle.load(open(full_path, "rb" ))