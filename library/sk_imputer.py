from sklearn.impute import SimpleImputer
import numpy as np 

def imputer_missing_values(x):
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp.fit(x)
    xt = imp.transform(x)
    return xt