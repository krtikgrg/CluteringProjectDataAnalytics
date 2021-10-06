import json
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt
import numpy as np
import random
import pandas as pd
PATH = "bottom_up_reduced_7.json"
CLUSTER_TO_INDICES = {}
INDICES_TO_CLUSTER = []
reduced_data = []
DATALEN = 0
uniqueLabels = [0,1,2,3,4,5,6] #change for different k

def loadCluster():
    global CLUSTER_TO_INDICES
    with open(PATH,'r') as fp:
        CLUSTER_TO_INDICES = json.load(fp)

def developList():
    global CLUSTER_TO_INDICES
    global INDICES_TO_CLUSTER
    for i in range(DATALEN):
        INDICES_TO_CLUSTER.append(random.randint(0,2))
    for i in CLUSTER_TO_INDICES:
        # print(type(i))
        # print()
        # print()
        indices = CLUSTER_TO_INDICES[i]
        for j in indices:
            # print(type(j))
            INDICES_TO_CLUSTER[j] = int(i)

def runPCA(data):
    global reduced_data
    pca = PCA(n_components = 2)
    pca.fit(data)
    reduced_data = pca.transform(data)
    # print(reduced_data.shape)
    # print(reduced_data)
    # print(reduced_data[0,0])


def plot():
    global reduced_data
    global INDICES_TO_CLUSTER
    global uniqueLabels
    label = np.array(INDICES_TO_CLUSTER)
    # print(INDICES_TO_CLUSTER)
    for i in uniqueLabels:
        xcor = []
        ycor = []
        for j in range(DATALEN):
            if INDICES_TO_CLUSTER[j] == i:
                xcor.append(reduced_data[j,0])
                ycor.append(reduced_data[j,1])
        # print(xcor)
        plt.scatter(xcor,ycor,label=i)
    plt.legend()
    plt.title("Agglomerative Clustering")
    plt.show()

def runVisualise(data,df1):
    global DATALEN
    DATALEN = len(data)
    
    df1 = df1.reset_index()
    scaling = StandardScaler()
    scaling.fit(df1)
    scaled_data = scaling.transform(df1)
    # print(scaled_data)
    # print(scaled_data.shape)

    loadCluster()
    developList()
    runPCA(scaled_data)
    plot()
