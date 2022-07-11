from sklearn import model_selection
from sklearn.metrics import confusion_matrix


def logistic_regression_basic(df, columnas, target, seed, model):
    x = df[columnas]
    target = df.loc[:, target]
    x_train, x_test, target_train, target_test = model_selection.train_test_split(x, target, test_size=0.2, random_state=seed)
    model.fit(x_train, target_train)

    print('PORCENTAJES-----------------------------------------------------')
    print('El porcentaje de acierto en el test es de:', model.score(x_test, target_test))
    print('El porcentaje de acierto en el entrenamiento es de:', model.score(x_train, target_train))
    
    print('MATRIZ_CONFUSION------------------------------------------------')
    predictions = model.predict(x_test)
    print(confusion_matrix(target_test, predictions))
    
    # print('RESTO-----------------------------------------------------')
    return x_train, x_test, target_train, target_test, model, predictions


def cross_val_test(seed, model, x_train, y_train, splits):
    kfold = model_selection.KFold(n_splits=splits, random_state=seed) 
    cv_results = model_selection.cross_val_score(model, x_train, y_train, cv=kfold, scoring='accuracy')
    msg = "%s: %f %s (%f)" % ('Logistic Regression', cv_results.mean(), "+-", cv_results.std())
    print('Los porcentajes de acierto en las diferentes iteraciones fueron:', cv_results)
    print('Para este modelo el porcentaje de acierto es:')
    print(msg)


def predict_prob(model, x_test):
    model.predict_proba(x_test)



"""
model3 = linear_model.LogisticRegression(max_iter=900, penalty='l1', solver='saga', n_jobs=-1)
model2 = linear_model.LogisticRegression(max_iter=9000)
model5 = linear_model.LogisticRegression(max_iter=90000, penalty='l1', solver='saga', class_weight={2 : 0.5}, n_jobs=-1)
model4 = linear_model.LogisticRegression(max_iter=900000, penalty='l2', solver='liblinear', dual=True, n_jobs=-1)
model6 = linear_model.LogisticRegression(max_iter=90000, solver='newton-cg', n_jobs=-1)
model8 = linear_model.LogisticRegression(max_iter=90000, solver='sag', n_jobs=-1)
model7 = linear_model.LogisticRegression(max_iter=90000, solver='liblinear', n_jobs=-1)
"""