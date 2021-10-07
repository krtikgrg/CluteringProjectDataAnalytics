from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from math import sqrt

import json
from map import MAPPER

data = []
preProcessedData = []

diffTwoIndices = [3, 26]
diffZeroIndices = [15, 16, 17]
diffListMethod = [22]
diffFiveIndices = [7, 8, 27] + list(range(28,88))
diffTwoHundredIndices = [13]
MAPPER_INDEX_TO_DIFF = {}

def designMapperIndexToDiff():
    global diffFiveIndices
    global diffTwoHundredIndices
    global diffTwoIndices
    global diffZeroIndices
    for i in diffZeroIndices:
        MAPPER_INDEX_TO_DIFF[i] = 0
    for i in diffTwoIndices:
        MAPPER_INDEX_TO_DIFF[i] = 2
    for i in diffFiveIndices:
        MAPPER_INDEX_TO_DIFF[i] = 5
    for i in diffTwoHundredIndices:
        MAPPER_INDEX_TO_DIFF[i] = 200
    # MAPPER_INDEX_TO_DIFF[22] = "LIST"

def distanceBetweenTwoVectors(i,l):
    global preProcessedData
    i = list(i)
    l = list(l)
    i = i[0]
    l = l[0]
    curSimilarity = 0
    for k in MAPPER:
        attribute = MAPPER[k]
        if k==22:
            if preProcessedData[attribute][i] == preProcessedData[attribute][l]:
                curSimilarity = curSimilarity + 1
        else:
            diffVal = MAPPER_INDEX_TO_DIFF[k]
            curValOth = preProcessedData[attribute][l]
            lowerLimit = curValOth - diffVal
            upperLimit = curValOth + diffVal
            if (preProcessedData[attribute][i] >= lowerLimit) and (preProcessedData[attribute][i] <= upperLimit):
                curSimilarity += 1
    curSimilarity = curSimilarity/len(MAPPER)
    distance = 1 - curSimilarity
    # print("DEBUG::RETURNING")
    return distance

def sim_affinity(X):
    return pairwise_distances(X,metric=distanceBetweenTwoVectors)

def bottomUp(data):
    global preProcessedData
    preProcessedData = data
    designMapperIndexToDiff()
    for k in range(3,8,2):
        nuData = []
        for i in range(0,len(data)):
            temp = []
            temp.append(i)
            nuData.append(temp)
        cluster = AgglomerativeClustering(n_clusters=k, affinity=sim_affinity, linkage='average')
        CLUSTER_GIVEN = cluster.fit_predict(nuData)
        CLUSTER_TO_INDICES = {}
        for i in range(k):
            CLUSTER_TO_INDICES[i] = []
        for i in range(len(CLUSTER_GIVEN)):
            CLUSTER_TO_INDICES[CLUSTER_GIVEN[i]].append(i)
        print(len(CLUSTER_GIVEN))
        print(len(data))
        with open("agglomerative_bottom_up_df_"+str(k)+".json",'w') as fp:
            json.dump(CLUSTER_TO_INDICES,fp)

def bottomUpReduced(df1):
    df1 = df1.reset_index()
    scaling = StandardScaler()
    scaling.fit(df1)
    scaled_data = scaling.transform(df1)
    pca = PCA(n_components = 2)
    pca.fit(scaled_data)
    reduced_data = pca.transform(scaled_data)
    # print(len(reduced_data))
    for k in range(3,8,2):
        cluster = AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='ward')
        CLUSTER_GIVEN = cluster.fit_predict(reduced_data)
        CLUSTER_TO_INDICES = {}
        for i in range(k):
            CLUSTER_TO_INDICES[i] = []
        for i in range(len(CLUSTER_GIVEN)):
            CLUSTER_TO_INDICES[CLUSTER_GIVEN[i]].append(i)
        # print()
        # print(len(CLUSTER_GIVEN))
        # print(len(reduced_data))
        with open("bottom_up_reduced_"+str(k)+".json",'w') as fp:
            json.dump(CLUSTER_TO_INDICES,fp)

def calcMinClusterDistance(cluster):
    global data
    maxDist = 0
    a = -1
    b = -1
    for i in cluster:
        for j in cluster:
            if i != j:
                curDist = sqrt((data[i][0]-data[j][0])**2 + (data[i][1]-data[j][1])**2)
                if curDist > maxDist:
                    maxDist = curDist
                    a = i
                    b = j
    return maxDist,a,b

def upBottomK(k):
    global data
    # listNum = list(range(0,len(data)))
    # CLUSTERS = {}
    # CLUSTERS[0] = listNum
    # lstAvailIndex = 1
    tempCluster = {}
    with open("up_bottom_reduced_"+str(k-2)+".json",'r') as fp:
        tempCluster = json.load(fp)
    CLUSTERS = {}
    lstAvailIndex = k-2
    for i in tempCluster:
        CLUSTERS[int(i)] = tempCluster[i]

    while lstAvailIndex < k:
        print("DEBUG::CLUSTERS FORMED TILL NOW "+str(lstAvailIndex))
        distMax = 0
        cluster = -1
        a = -1
        b = -1
        for i in CLUSTERS:
            curmax,ca,cb = calcMinClusterDistance(CLUSTERS[i])
            if curmax>distMax:
                distMax = curmax
                cluster = i
                a = ca
                b = cb
        new1 = []
        new2 = []
        for i in CLUSTERS[cluster]:
            dista = sqrt((data[i][0]-data[a][0])**2 + (data[i][1]-data[a][1])**2)
            distb = sqrt((data[i][0]-data[b][0])**2 + (data[i][1]-data[b][1])**2)
            if dista<distb:
                new1.append(i)
            else:
                new2.append(i)

        CLUSTERS[cluster] = new1
        CLUSTERS[lstAvailIndex] = new2
        lstAvailIndex += 1
    
    with open("up_bottom_reduced_"+str(k)+".json",'w') as fp:
        json.dump(CLUSTERS,fp)

def upBottomReduced(df1):
    global data
    df1 = df1.reset_index()
    scaling = StandardScaler()
    scaling.fit(df1)
    scaled_data = scaling.transform(df1)
    pca = PCA(n_components = 2)
    pca.fit(scaled_data)
    reduced_data = pca.transform(scaled_data)
    data = reduced_data
    for k in range(5,8,2):
        upBottomK(k)