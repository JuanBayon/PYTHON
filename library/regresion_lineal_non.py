import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.preprocessing import PolynomialFeatures
import os, sys

ruta = os.path.dirname(__file__)
sys.path.append(ruta)

from comprobaciones_ML import indicativos_regresion, indicativos_clasificacion



def regresion_lineal(df, columnas, target, seed):
    """
    Dada un dataframe, se devuelve la regresión lineal de las columnas elegidas con el target. 
    Se muestra por pantalla información sobre pendiente, porcentajes de acierto y errores.
    """

    if len(columnas) == 1:
        x = df.loc[:, columnas[0]]
        x = x.values.reshape(-1, 1)
        target = df.loc[:, target]
    
    else:
        x = df[columnas]
        target = df.loc[:, target]

    x_train, x_test, target_train, target_test = train_test_split(x, target, test_size=0.2, random_state=seed)

    linear = LinearRegression(n_jobs=-1)
    linear.fit(x_train, target_train)
    predicciones = linear.predict(x_test)

    if (target >= 100000).all() and (predicciones >=100000).all():  
        mean_squared_log_error=metrics.mean_squared_log_error(target, predicciones)

    explained_variance = metrics.explained_variance_score(target, predicciones)
    r2 = metrics.r2_score(target, predicciones)

    print('Las pendientes son:', linear.coef_)

    print('PORCENTAJES-----------------------------------------------------')
    print('El score de acierto en el test es de:', linear.score(x_test, target_test))
    print('El score de acierto en el entrenamiento es de:', linear.score(x_train, target_train))
    print('La varianza explicada es:', explained_variance)
    print('R2:', r2)

    print('DESVIACIONES----------------------------------------------------')
    print('MAE:', metrics.mean_absolute_error(target_test, predicciones))
    print('MSE:', metrics.mean_squared_error(target_test, predicciones))
    print('RMSE:', np.sqrt(metrics.mean_squared_error(target_test, predicciones)))
    print('RMSLE(mean_squared_log_error):', mean_squared_log_error)
    print('----------------------------------------------------------------')

    ## OPCIÓN DE SACAR PROBABILIDAD!!

    return x_train, x_test, target_train, target_test, linear, predicciones



def imprime_variaciones_regresion_lineal(coeficientes, columnas, target):
    for coef, columna in zip(coeficientes, columnas):
        print(f'Manteniendo el resto de valores fijos, una unidad de incremento en la variable {columna}, incrementa {target} en {coef}')




def conjuntos_regresion_tvs(L, T, V=0, S=False):
    """
    Obtiene los grupos para el entrenamiento dada una lista. Se dan como parámetros el 
    porcenaje de test y de validación si existe, del 0 al 100, y si se mezclan (Falso por defecto).
    """
    list_train, list_test = train_test_split(L, test_size=T, shuffle=S)
    if V > 0:
        list_train, list_val = train_test_split(list_train, test_size=V, shuffle=S)
        return list_train, list_val, list_test
    return list_train, list_test


def convierte_grados(X, target, degree, seed):
    polinominal_model = PolynomialFeatures(degree) 
    x_train, x_test, target_train, target_test = train_test_split(X, target, test_size=0.2, random_state=seed)
    X_poly = polinominal_model.fit_transform(x_train, target_train)
    X_test_poly = polinominal_model.fit_transform(x_test)
    return X_poly, X_test_poly, target_train, target_test, polinominal_model



def itera_grados(X, target, degree_max, seed, degree_min=2, clasificacion=False, cv=None, pendientes=False):
    models = []
    trains_tests = []
    polinomials = []
    n_scores = []
    for degree in range(degree_min,degree_max+1):
        X_poly, X_test_poly, target_train, target_test, polinominal_model = convierte_grados(X, target, degree, seed)
        train_test = (X_poly, X_test_poly, target_train, target_test)
        trains_tests.append(train_test)
        polinomials.append(polinominal_model)
        X_t = polinominal_model.transform(X)
        lin_reg_model = LinearRegression()
        if clasificacion:
            print(f'GRADO {degree}  ###########################################################################################')
            print('\n')
            indicativos_clasificacion(seed=seed, model=lin_reg_model, test_size=0.2, train_test=train_test, x=X_t, target=target, cv=cv, pendientes=pendientes)
            models.append(lin_reg_model)
        else:
            print(f'GRADO {degree}  ###########################################################################################')
            print('\n')
            indicativos_regresion(model=lin_reg_model, seed=seed, test_size=0.2, train_test=train_test, x=X_t, target=target, cv=cv, pendientes=pendientes)
            models.append(lin_reg_model)
    return models, trains_tests, polinomials, n_scores
