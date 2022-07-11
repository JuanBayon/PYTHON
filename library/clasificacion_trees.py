from sklearn.model_selection import RepeatedKFold
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt 
from sklearn import tree


def randomforest_cal_stimators(x, target, seed, n_stimators=100, test_size=0.2, n_splits=10):

    X_train, X_test, y_train, y_test = train_test_split(x, target, test_size=test_size, random_state=seed)
    train_test = (X_train, X_test, y_train, y_test)

    k_fold = RepeatedKFold(n_splits=n_splits, n_repeats=1, random_state=seed)
    val_score = []
    train_score = []
    model = RandomForestClassifier(warm_start=True, n_estimators=n_stimators)
    path = os.path.dirname(__file__) + os.sep

    for i, (train, val) in enumerate(k_fold.split(X_train)):
        print("Iteración:", i+1)
        print("val_size:", len(val))
    
        model.fit(X_train[train], y_train[train])
        model.n_estimators += 100

        score_val = model.score(X_train[val], y_train[val])
        val_score.append(score_val)
        score_train = model.score(X_train[train], y_train[train])
        train_score.append(score_train)
        print('Score val:', score_val)
        print('Score train:', score_train)
        print('##########################')

        # EARLY STOP GUARDANDO EL MODELO.
        if np.mean(val_score) > 0.99 and len(val_score) > 50:
            pickle.dump(model, open(path + "model_saved.sav", "wb"))
            print("STOP")
            break
        print('##########################')
        
    return model, train_test


def feature_importance(model, X):
    feature_list = list(X.columns)
    importances = list(model.feature_importances_)
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
    [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]


def plot_tree(tree_model, X, y, save=False):
    text_representation = tree.export_text(tree_model)
    print(text_representation)
    if save:
        with open("decistion_tree.log", "w") as fout:
            fout.write(text_representation)

    fig = plt.figure(figsize=(25,20))
    _ = tree.plot_tree(tree_model, 
                    feature_names=X.columns,  
                    class_names=y,
                    filled=True)
    if save:
        fig.savefig("decistion_tree.png")