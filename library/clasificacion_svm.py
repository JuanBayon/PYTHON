from sklearn import svm


def model_svm(X, y, C, gamma, kernel, linear=False):
    if linear: 
        clf = svm.LinearSVC(C=C, gamma=gamma)
    else:
        clf = svm.SVC(C=C, kernel=kernel, gamma=gamma)
    return clf