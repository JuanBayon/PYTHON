from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV   
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
    
    
    
def grid_search(self, kind, X_train, y_train,):
    pipe = Pipeline(steps=[
        ('classifier', RandomForestClassifier())])

    if kind == 'logistic':
        params = {
            'classifier': [LogisticRegression()],
            'classifier__penalty': ['l1', 'l2'],
            "classifier__C": [0.01, 0.1, 0.5, 1]}

    if kind == 'forest':
        params = {
            'classifier': [RandomForestClassifier()],
            'classifier__n_estimators': [10, 100, 1000],
            'classifier__max_features': [1,2,3]}

    if kind == 'svc':
        params = {
            'classifier': [svm.SVC()],
            'classifier__kernel': ('linear', 'rbf', 'sigmoid'),
            'classifier__C': [0.001, 0.1, 0.5, 1, 5, 10],
            'classifier__gamma': ('scale', 'auto')}

    if kind == 'knn':
        params = {
            'classifier': [KNeighborsClassifier()],
            'classifier__n_neighbors': [3, 5, 11, 19],
            'classifier__weights': ['uniform', 'distance'],
            'classifier__metric': ('euclidean', 'manhattan')}
        
    clf = GridSearchCV(estimator = pipe,
                    param_grid = params,
                    cv = 3,
                    verbose=1,
                    n_jobs=-1)

    clf.fit(X_train, y_train)
    return clf