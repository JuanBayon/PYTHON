import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import sklearn.preprocessing as preprocessing
from sklearn.model_selection import RepeatedStratifiedKFold, RepeatedKFold
import matplotlib.pyplot as plt


def indicativos_regresion(model, seed, test_size=0.2, train_test=None, x=None, target=None, cv=None, pendientes=False):
    """
    Dada un dataframe, se devuelve la regresión lineal de las columnas elegidas con el target. 
    Se muestra por pantalla información sobre pendiente, porcentajes de acierto y errores.

    train_test = (x_train, x_test, target_train, target_test)
    """
    if not train_test:
        x_train, x_test, target_train, target_test = train_test_split(x, target, test_size=test_size, random_state=seed)
    else:
        x_train, x_test, target_train, target_test = train_test

    scores_index = None
    if cv:
        scores_index = train_cross_val(seed, model, x_train, target_train, splits=cv[0], repeats=cv[1], stratified=cv[2], tree_warm_start=cv[3])
    else:
        model.fit(x_train, target_train)
    
    predicciones = model.predict(x_test)

    # mean_squared_log_error = None
    # if x_train[0][0] > 100000:
    #     mean_squared_log_error=metrics.mean_squared_log_error(target_test, predicciones)

    explained_variance = metrics.explained_variance_score(target_test, predicciones)
    r2 = metrics.r2_score(target_test, predicciones)

    #errors = abs(predicciones - target_test)
    #mape = 100 * (errors / x_test)

    if pendientes:
        print('Las pendientes son:', model.coef_)
        print('\n')

    print('PORCENTAJES-----------------------------------------------------')
    print('El score de acierto en el test es de:', model.score(x_test, target_test))
    print('El score de acierto en el entrenamiento es de:', model.score(x_train, target_train))
    try:
        print('El score de acierto total es de:', model.score(x, target))
    except:
        pass
    print('La varianza explicada es:', explained_variance)
    print('R2:', r2)
    #print("mean MAPE(mean absolute percentage error", np.mean(mape))
    print('\n')

    print('DESVIACIONES----------------------------------------------------')
    print('MAE:', metrics.mean_absolute_error(target_test, predicciones))
    print('MSE:', metrics.mean_squared_error(target_test, predicciones))
    print('RMSE:', np.sqrt(metrics.mean_squared_error(target_test, predicciones)))
    # if mean_squared_log_error:
    #     print('RMSLE(mean_squared_log_error):', mean_squared_log_error)
    print('----------------------------------------------------------------')
    print('\n')

    ## OPCIÓN DE SACAR PROBABILIDAD!!
    # print(neigh.predict_proba([[0.9]]))  ## SACA LA PROBABILIDAD! COMO EN EL OTRO. PARA VER CON QUE SEGURIDAD ME ESTÁ DANDO EL RESULTADO. 

    if  not train_test:
        return x_train, x_test, target_train, target_test, predicciones, scores_index
    else:
        return predicciones, scores_index



def train_cross_val(seed, model, x_train, y_train, splits, repeats=1, stratified=False, tree_warm_start=False):
    try:
        if stratified:
            k_fold = RepeatedStratifiedKFold(n_splits=splits, n_repeats=repeats, random_state=seed)
    except ValueError:
        k_fold = RepeatedKFold(n_splits=splits, n_repeats=repeats, random_state=seed)

    val_score = []
    train_score = []
    train_index = []
    val_index = []

    for i, (train, val) in enumerate(k_fold.split(x_train)):
        print("Iteración:", i+1)
        print("val_size:", len(val))
        train_index.append(train)
        val_index.append(val)
    
        model.fit(x_train[train], y_train[train])
        if tree_warm_start:
            model.n_estimators += 100

        score_val = model.score(x_train[val], y_train[val])
        val_score.append(score_val)
        score_train = model.score(x_train[train], y_train[train])
        train_score.append(score_train)
        print('Score val:', score_val)
        print('Score train:', score_train)
        print('##########################')

    return train_score, val_score, train_index, val_index



# Dos tipos de lectura de error: 
# - En porcentaje
# - En valor. 

#1. VALOR 

#Se utiliza mejor el RMSE que el mse porque tiene el mismo sentido. Para trabajar con números más pequeños. POR DEBAJO DE UNO NO!

""" CUANTO MÁS DISTANCIA ENTRE EL MAE Y EL RMSE MÁS OUTLIERS HAY!!!!!
            SI NO HAY DISPERSIÓN MAE Y RMSE COINCIDEN!!!!!!!"""

# si tenemos valores por debajo de 1, cuanto más cercano al uno mejor. (La raíz cuadrada de 0,5 es 0,7.) MUY afectado por los outlliers. Puede servir para buscarlos. EVIDENCIA LOS OUTLIERS! Son un porcentaje de acierto. SCORE??

# MEAN_SQUARED_LOG_ERROR RMSLE. se usa para valores muy grandes. Se pasa antes por el logaritmo. Equivalente al rmse y no realzar la magnitud de los datos. 

"""MSE NO SE USA CASI POR SUS VALORES GRANDES. RMSLE(LOG) SÓLO EN CASO DE VALORES MUY GRANDES"""

#-----------------------------------------------------------------------

#2. PORCENAJE

# EXPLAINED VARIANCE es con valor hasta 1. cuanto más cercano a 1 más perfecto. Igual en este caso que R2. R2 en otros momentos tiene otro valor.  PUEDE LLEGAR A -INFINITO. Lo más cercano a uno posible.

#SCORE. % DE ACIERTO. ES UNA MEZCLA DE MEDIDAS. EN REGRESIÓN LINEAL ES R2 A MUERTE. EN OTROS MODELOS R2 CAMBIA. EN REGRESIÓN LOGISTICA ES UN ACCURACY. 

# LA FUNCIÓN SCORE ENTRE ALGORITMOS ES COMPARABLE. CUANTO MÁS ALTO MEJOR. --PUEDE HABER SCORE NEGATIVO-- ES NEGATIVO SI ES PEOR QUE PREDECIR LA MEDIA. A PARTIR DE 0 AJUSTE BAJO, 0,5 AJUSTE MEDIO Y MÁS DE 0,8 AJUSTE BUENO. SI ES NEGATIVO ES MEJOR USAR LA ALEATORIEDAD.

"""SCORE SIEMPRE Y LUEGO R2 Y VARIANZA EXPLICATIVA"""

# RESUMEN MAE Y RMSE / SCORE LOS MÁS IMPORTANES. 




def indicativos_clasificacion(model, seed, test_size=0.2, train_test=None, x=None, target=None, cv=None):
    """
    train_test = (x_train, x_test, target_train, target_test)
    """
    if not train_test:
        x_train, x_test, target_train, target_test = train_test_split(x, target, test_size=test_size, random_state=seed)
    else:
        x_train, x_test, target_train, target_test = train_test

    scores_index = None
    if cv:
        scores_index = train_cross_val(seed, model, x_train, target_train, splits=cv[0], repeats=cv[1], stratified=cv[2], tree_warm_start=cv[3])
    else:
        model.fit(x_train, target_train)

    print('\n')
    print('PORCENTAJES-----------------------------------------------------')
    print('El score de acierto en el test es de:', model.score(x_test, target_test))
    print('El score de acierto en el entrenamiento es de:', model.score(x_train, target_train))
    print('El score de acierto total es de:', model.score(x, target))
    # RECALL, PRECITION, F1 (FALSOS POSITIVOS, FALSOS NEGATIVOS, FACTOR DE TODO)
    # EXHAUSTIVIDAD, PRECISIÓN Y F-VALUE
    # CURVA-ROC. 
    # BAJO BIAS!! (ENCUENTRA EL PATRÓN PERO NO FUNCIONA PORQUE NO SABE DIFERENCIAR)
    # BAJA VARIANZA!! (NO ECUENTRA EL PATRÓN Y POR TANTO TAMPOCO FUNCIONA)
    print('\n')
    
    print('MATRIZ_CONFUSION------------------------------------------------')
    predictions = model.predict(x_test)
    print(confusion_matrix(target_test, predictions))
    print('\n')

    print('MATRIZ_CONFUSION ENTRENAMIENTO ---------------------------------')
    predictions_train = model.predict(x_train)
    print(confusion_matrix(target_train, predictions_train))
    print('\n')

    if  not train_test:
        return x_train, x_test, target_train, target_test, predictions, scores_index
    else:
        return predictions, scores_index



def epoca_cross_val_test(seed, model, x_train, y_train, splits, repeats=1, stratified=False):
    if stratified:
        k_fold = RepeatedStratifiedKFold(n_splits=splits, n_repeats=repeats, random_state=seed)
    else:
        k_fold = RepeatedKFold(n_splits=splits, n_repeats=repeats, random_state=seed)

    n_scores = model_selection.cross_val_score(model, x_train, y_train, cv=k_fold, scoring='accuracy', n_jobs=-1, error_score='raise')
    msg = 'Accuracy: %.3f (%.3f)' % (n_scores.mean(), "+-", n_scores.std())
    print('Los porcentajes de acierto en las diferentes iteraciones fueron:', n_scores)
    print('Para este modelo el porcentaje de acierto es:')
    print(msg)



def normalizar(X, normalizador=None):
    if normalizador == 'minmax':
        scaler = preprocessing.MinMaxScaler()
        scaler.fit(X)
        X_normalized = scaler.transform(X)
        return X_normalized, scaler
    elif normalizador == 'maxabs':
        scaler = preprocessing.MaxAbsScaler()
        scaler.fit(X)
        X_normalized = scaler.transform(X)
        return X_normalized, scaler
    elif normalizador == 'normalizer':
        scaler = preprocessing.Normalizer()
        scaler.fit(X)
        X_normalized = scaler.transform(X)
        return X_normalized, scaler
    elif normalizador == 'power':
        scaler = preprocessing.PowerTransformer()
        scaler.fit(X)
        X_normalized = scaler.transform(X)
        return X_normalized, scaler
    elif normalizador == 'quantileuniform':
        scaler = preprocessing.QuantileTransformer(output_distribution='uniform')
        scaler.fit(X)
        X_normalized = scaler.transform(X)
        return X_normalized, scaler
    elif normalizador == 'quantilenormal':
        scaler = preprocessing.QuantileTransformer(output_distribution='normal')
        scaler.fit(X)
        X_normalized = scaler.transform(X)
        return X_normalized, scaler
    elif normalizador == 'robust':
        scaler = preprocessing.RobustScaler()
        scaler.fit(X)
        X_normalized = scaler.transform(X)
        return X_normalized, scaler
    elif normalizador == 'standard':
        scaler = preprocessing.StandardScaler()
        scaler.fit(X)
        X_normalized = scaler.transform(X)
        return X_normalized, scaler


def plot_results(x_train, y_train, y_pred):
    X_train_to_show, y_train_to_show = zip(*sorted(zip(x_train, y_train)))
    plt.scatter(X_train_to_show, y_train_to_show, color='violet')
    X_train_to_show, y_pred = zip(*sorted(zip(x_train, y_pred)))
    plt.plot(X_train_to_show, y_pred, color='purple')
    plt.show()


