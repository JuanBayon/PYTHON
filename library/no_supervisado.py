from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
from sklearn import metrics, preprocessing
from sklearn.cluster import SpectralClustering
import numpy as np 
from sklearn.cluster import AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.mixture import BayesianGaussianMixture
from sklearn.cluster import MiniBatchKMeans


######### CLUSTER ###################################################


def kmeans(X, seed, kmin, kmax = None, good_init='k-means++'):
    if kmax:
        kmeans = []
        for i, k in enumerate(range(kmin, kmax +1)):
            print(f'######### K {k} ITERACION {i} #####################################################################')
            print('\n')
            kmeans_model = KMeans(n_clusters=i, random_state=seed, init=good_init).fit(X)
            print("kmeans.labels_:", kmeans_model.labels_)
            clusters = kmeans_model.cluster_centers_
            print("kmeans.cluster_centers_:", clusters)
            inercia = kmeans_model.inertia_
            print("kmeans.inertia_:", inercia)
            silhouette_coeficient = metrics.silhouette_score(X, kmeans_model.labels_)
            print("kmeans.shilhouette_:", silhouette_coeficient)
            kmeans.append(kmeans_model)
            print('\n')
    else:
        kmeans = KMeans(n_clusters=kmin, random_state=seed, init=good_init).fit(X)
        print("kmeans.labels_:", kmeans.labels_)
        # if X_predict:
        #     prediccion = kmeans.predict(X_predict)
        #     print("predict:", prediccion)
        clusters = kmeans.cluster_centers_
        print("kmeans.cluster_centers_:", clusters)
        inercia = kmeans.inertia_
        print("kmeans.inertia_:", inercia)
        # te quedas con la menor inercia!!
        silhouette_coeficient = metrics.silhouette_score(X, kmeans.labels_)
        print("kmeans.shilhouette_:", silhouette_coeficient)
        # score de silhouette para encontrar elbow
        # te quedas con el más alto!!
        # porcentaje de mejora entre un k y el siguiente

    return kmeans



def itera_semilla_kmeans(X, seed_min, seed_max, k):
    kmeans = []
    for i, seed in enumerate(range(seed_min, seed_max)):
            print(f'########### SEMILLA {seed} ITERACION {i} ##############')
            kmeans_model = KMeans(n_clusters=k, random_state=seed).fit(X)
            print("kmeans.labels_:", kmeans.labels_)
            clusters = kmeans.cluster_centers_
            print("kmeans.cluster_centers_:", clusters)
            inercia = kmeans.inertia_
            print("kmeans.inertia_:", inercia)
            silhouette_coeficient = metrics.silhouette_score(X, kmeans.labels_)
            print("kmeans.shilhouette_:", silhouette_coeficient)
            kmeans.append(kmeans_model)
    return kmeans



def spectral_clustering(X):
    sc1 = SpectralClustering(n_clusters=2, gamma=100, random_state=42)
    sc1.fit(X)
    print(np.percentile(sc1.affinity_matrix_, 95))
    return sc1


def agglomerative_clustering(X, estimator):
    agg = AgglomerativeClustering(linkage="complete").fit(X)
    print([attrib for attrib in dir(estimator)
            if attrib.endswith("_") and not attrib.startswith("_")])



def dbscan(X, target=None, eps=0.5, min_samples=5):
    # db = DBSCAN(eps=0.2 o 0.005, min_samples=5).fit(X)
    dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    labels = dbscan.labels_
    print(np.unique(labels))
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    print('Estimated number of clusters: %d' % n_clusters_)
    print('Estimated number of noise points: %d' % n_noise_)
    try:
        if target:
            print("Homogeneity: %0.3f" % metrics.homogeneity_score(target, labels))
            print("Completeness: %0.3f" % metrics.completeness_score(target, labels))
            print("V-measure: %0.3f" % metrics.v_measure_score(target, labels))
    except:
        pass
    print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))
    return dbscan


def minibatchkmeans(X):
    """
    Lo hace por partes(batches).
    """
    minibatch_kmeans = MiniBatchKMeans(n_clusters=5, random_state=42)
    minibatch_kmeans.fit(X)
    print(minibatch_kmeans.inertia_)
    return minibatch_kmeans




def gaussian_mixture(X, n_components, seed, n_init=10, n_components_max=None, best=None):
    """
    You can impose constraints on the covariance matrices that the algorithm looks for by setting the `covariance_type` hyperparameter:
    * `"full"` (default): no constraint, all clusters can take on any ellipsoidal shape of any size.
    * `"tied"`: all clusters must have the same shape, which can be any ellipsoid (i.e., they all share the same covariance matrix).
    * `"spherical"`: all clusters must be spherical, but they can have different diameters (i.e., different variances).
    * `"diag"`: clusters can take on any ellipsoidal shape of any size, but the ellipsoid's axes must be parallel to the axes (i.e., the covariance matrices must be diagonal).
    gm_full = GaussianMixture(n_components=3, n_init=10, covariance_type="full", random_state=42)
    gm_tied = GaussianMixture(n_components=3, n_init=10, covariance_type="tied", random_state=42)
    gm_spherical = GaussianMixture(n_components=3, n_init=10, covariance_type="spherical", random_state=42)
    gm_diag = GaussianMixture(n_components=3, n_init=10, covariance_type="diag", random_state=42)
    gm_full.fit(X)
    gm_tied.fit(X)
    gm_spherical.fit(X)
    gm_diag.fit(X)
    """
    gm = GaussianMixture(n_components=n_components, n_init=n_init, random_state=seed)
    gm.fit(X) 
    print(gm.weights_ )
    print(gm.bic(X))
    print(gm.aic(X))

    if n_components_max:
        gms_per_k = [GaussianMixture(n_components=k, n_init=n_init, random_state=seed).fit(X)
                for k in range(n_components, n_components_max)]
        bics = [model.bic(X) for model in gms_per_k]
        aics = [model.aic(X) for model in gms_per_k]
        print(bics)
        print(aics)

    min_bic = np.infty

    if best:
        for k in range(n_components, n_components_max):
            for covariance_type in ("full", "tied", "spherical", "diag"):
                bic = GaussianMixture(n_components=k, n_init=n_init,
                                    covariance_type=covariance_type,
                                    random_state=seed).fit(X).bic(X)
                if bic < min_bic:
                    min_bic = bic
                    best_k = k
                    best_covariance_type = covariance_type
                    print(best_k, best_covariance_type)
                    return min_bic, best_k, best_covariance_type

    return gm, bics, aics



def Bayesian_gaussianmixture(X):
    """
    Detecta el número de componentes directamente, sin necesidad de hacerlo manual 
    con la función anterior gaussian_mixture.
    """
    bgm = BayesianGaussianMixture(n_components=10, n_init=10, random_state=42)
    bgm.fit(X)
    return bgm






######### DETECCIÓN ANOMALÍAS ###############################################
"""
Detección de anomalías. Tienes que poner un límite subjetivo siempre. 
Se calcula la media y se estipula un porcentaje respecto a la desviación típica de la media.
Media +- Desviación típica = Rango de lo que es normal. Por ejemplo 20% más anomalía. AWS Amazon por defecto 20%. 
"""

def GaussianMixture_anomaly(gm, X):
    densities = gm.score_samples(X)
    density_threshold = np.percentile(densities, 4)
    anomalies = X[densities < density_threshold]
    return anomalies






######### IMAGEN ######################################################
"""
# reshape(-1, 3)!!!
# se usa kfolds!!
from matplotlib.image 
image = image.os.....

pipeline = Kmeans (n_cluster = 50) y gridsearch para ver cómo clusterizar la imagen
SERÍA EL NÚMERO DE COLORES
para conseguir mejor resultado. 
para la regresión lineal

"""
######### SEMISUPERVISADO ##############################################
"""
Ponemos etiquetas a parte y propagamos las etiquetas, eligiendo para poner etiquetas 
los n valores más significativos.

"""
########################################################################







######### REDUCIR GRADOS ###############################################


def pca(X, n_components, seed):
    """
    If n_components == 'mle' and svd_solver == 'full', Minka’s MLE is used to guess the dimension. Use of n_components == 'mle' will interpret svd_solver == 'auto' as svd_solver == 'full'
    If 0 < n_components < 1 and svd_solver == 'full', select the number of components such that the amount of variance that needs to be explained is greater than the percentage specified by n_components.
    If svd_solver == 'arpack', the number of components must be strictly less than the minimum of n_features and n_samples.
    """
    pca = PCA(n_components=n_components, random_state=seed)
    X2 = pca.fit_transform(X)
    print(pca.explained_variance_ratio_)
    return pca, X2



def itera_para_un_porcentaje_perdida_datos():
    pass



def t_sne(df, k):
    X_embedded = TSNE(n_components=k).fit_transform(df.values)
    print(X_embedded.kl_divergence_)
    return X_embedded







######### PLOT ##############################################################


def plot(X, target_color):
    plt.scatter(X[:, 0], X[:, 1], c=target_color)
    plt.scatter([X[90][0]], [X[90][1]], s=600, c=["r"], alpha=0.5)











