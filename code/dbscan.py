from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt 
import sklearn.utils
import json

data = []

def dbscan():
    global data
    db = DBSCAN(eps = 0.2, min_samples=25).fit(data)
    CLUSTER_GIVEN = db.labels_
    k = len(CLUSTER_GIVEN)
    CLUSTER_TO_INDICES = {}
    for i in set(CLUSTER_GIVEN):
        print(i)
        print(type(i))
        CLUSTER_TO_INDICES[int(i)] = []
    for i in range(len(CLUSTER_GIVEN)):
        CLUSTER_TO_INDICES[CLUSTER_GIVEN[i]].append(i)
    # print()
    # print(len(CLUSTER_GIVEN))
    # print(len(reduced_data))
    with open("db_scan_reduced_"+str(k)+".json",'w') as fp:
        json.dump(CLUSTER_TO_INDICES,fp)

def performDBscan(df1):
    global data
    df1 = df1.reset_index()
    scaling = StandardScaler()
    scaling.fit(df1)
    scaled_data = scaling.transform(df1)
    pca = PCA(n_components = 2)
    pca.fit(scaled_data)
    reduced_data = pca.transform(scaled_data)
    data = reduced_data
    # plt.scatter(data[:,0],data[:,1])
    plt.show()
    dbscan()