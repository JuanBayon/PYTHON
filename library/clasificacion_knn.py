from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


def knn_model(X, y):
    modelo = KNeighborsClassifier(n_neighbors=3)
    modelo.fit(X, y)

    # print(neigh.predict([[1.1]]))
    # print(neigh.predict_proba([[0.9]]))  ## SACA LA PROBABILIDAD! COMO EN EL OTRO. PARA VER CON QUE SEGURIDAD ME ESTÁ DANDO EL RESULTADO. 
    # neigh.classes_
    return modelo


def comprueba_rango_vecinos_knn(x, target, seed, test_size=0.2, rango_k=20):
    x_train, x_test, y_train, y_test = train_test_split(x, target, test_size=test_size, random_state=seed)
    k_range = range(1, rango_k)
    scores = {}
    modelos = []
    for k in k_range:
        knn = KNeighborsClassifier(n_neighbors = k)
        knn.fit(x_train, y_train)
        scores[k] = knn.score(x_test, y_test)
        modelos.append(knn)
    maximo = max(scores.values())
    for k, value in scores.items():
        if value == maximo:
            print(f'Con k = {k} el algoritmo alcanza el maximo para un rango de {rango_k}')
    plt.figure()
    plt.xlabel('k')
    plt.ylabel('accuracy')
    plt.scatter(k_range, list(scores.values()))
    plt.xticks(list(range(0, rango_k, 5)))
    return scores, modelos
