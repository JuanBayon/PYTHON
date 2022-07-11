from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import VotingClassifier
from sklearn. metrics import accuracy_score
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingClassifier




def ensemble(kind, estimators, voting='hard'):
    """
    estimators = [('name_model', model), ...}
    """

    if kind == 'voting':
        voting_clf = VotingClassifier(estimators = estimators, voting=voting)
        voting_clf.fit(X_train, y_train)
        for clf in (log_clf, rnd_clf, svm_clf, voting_clf):
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)
            print(clf.__class__.__name__, accuracy_score(y_test, y_pred))


    elif kind == 'bagging':
        estimator = DecisionTreeClassifier(random_state=42)
        bag_clf = BaggingClassifier(
                    base_estimator = estimator,
                    n_estimators = 500,
                    max_samples = 100,
                    bootstrap = True,  #BOOSTRAP ES CON REEMPLAZAMIENTO
                    random_state=42)
        bag_clf.fit(X_train, y_train)
        y_pred = bag_clf.predict(X_test)
        accuracy_score(y_test, y_pred)


    elif kind == 'randomforestclassifier':
        passrnd_reg = RandomForestClassifier(n_estimators=500, max_depth = 5, random_state=42)
        rnd_reg.fit(X_reg, Y_reg)
        y_pred_reg = rnd_reg.predict(X_reg)
        mean_absolute_error(Y_reg, y_pred_reg)

    
    elif kind == 'randomforestregressor':
        passrnd_reg = RandomForestRegressor(n_estimators=500, max_depth = 5, random_state=42)
        rnd_reg.fit(X_reg, Y_reg)
        y_pred_reg = rnd_reg.predict(X_reg)
        mean_absolute_error(Y_reg, y_pred_reg)

        
    elif kind == 'adaboostclassifier':
        estimator = DecisionTreeClassifier(max_depth=1)
        ada_clf = AdaBoostClassifier(base_estimator = estimator, n_estimators = 200, learning_rate=0.5, random_state=42)
        ada_clf.fit(X_train, y_train)
        y_pred = ada_clf.predict(X_test)
        accuracy_score(y_test, y_pred)


    elif kind == 'adaboostregression':
        ada_reg = AdaBoostRegressor(n_estimators=200, random_state=42)
        ada_reg.fit(X_reg, Y_reg)
        y_pred_ada_reg = ada_reg.predict(X_reg)
        mean_absolute_error(Y_reg, y_pred_ada_reg)

    
    elif kind == 'gradientboostingclassifier':
        gbct = GradientBoostingClassifier(max_depth=2, n_estimators=3, learning_rate=1, random_state=42)
        gbct.fit(X_train, y_train)
        y_pred_gbct = gbct.predict(X_test)
        accuracy_score(y_test, y_pred_gbct)


    elif kind == 'gradientboostingregressor':
        gbrt = GradientBoostingRegressor(max_depth=2, n_estimators = 3, learning_rate=1, random_state=42)
        gbrt.fit(X_reg, Y_reg)
        y_pred_gbrt = gbrt.predict(X_reg)
        mean_absolute_error(Y_reg, y_pred_gbrt)


    elif kind == 'xgbclassifier':
        xgb_clas = xgboost.XGBClassifier(random_state=42)
        xgb_clas.fit(X_train, y_train)
        y_pred = xgb_clas.predict(X_test)
        accuracy_score(y_test, y_pred)


    elif kind == 'xgbregressor':
        xgb_reg = xgboost.XGBRegressor(random_state=42)
        xgb_reg.fit(X_reg, Y_reg)
        y_pred = xgb_reg.predict(X_reg)
        mean_absolute_error(Y_reg, y_pred) 



"""
**¿Qué hiperparámetros debería tocar en el XGB?**
1. `n_estimators`: igual que para el GradientBoosting.
2. `booster`: tipo de modelo que correrá en cada iteración. Arboles o regresiones. `gbtree` or `gblinear`. Los árboles suelen ir bien.
3. `learning_rate`: o también llamado `eta`. Como el learning rate del GradientBoosting.
4. `max_depth`: nada nuevo

Si quieres afinar más todavía el XGBoost consulta [esta completa guía](https://www.analyticsvidhya.com/blog/2016/03/complete-guide-parameter-tuning-xgboost-with-codes-python/).
"""