import matplotlib.pyplot as plt
from map import MAPPER
import json

figure, axis = plt.subplots(2)
TRIES_PER_K = 2
DATALEN = 0
preProcessedData = []
CLUSTERS_TO_INDICES = {}

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

def generateMean(MAP):
    # print("DEBUG::IN GENERATE MEAN")
    global preProcessedData
    MAP_CLUSTER_TO_MEAN = {}
    for i in MAP:
        indices = MAP[i]
        numElements = len(indices)
        MEAN = {}
        for j in MAPPER:
            attribute = MAPPER[j]
            sumAll = 0
            for k in indices:
                sumAll += preProcessedData[attribute][k]
            if numElements!=0:
                sumAll = sumAll/numElements
            else:
                sumAll = 0
            MEAN[attribute] = sumAll
        attribute = MAPPER[22] #handling jersey number separately
        COMBINED_MAP = {}
        for k in indices:
            COMBINED_MAP[preProcessedData[attribute][k]] = 1
        COMBINED_LIST = []
        for k in COMBINED_MAP:
            COMBINED_LIST.append(k)
        MEAN[attribute] = COMBINED_LIST
        MAP_CLUSTER_TO_MEAN[i] = MEAN
    # print("DEBUG::RETURNING FROM GEN MEAN")
    return MAP_CLUSTER_TO_MEAN

def getSimilarity(MEAN_VECTOR,i):
    global MAPPER_INDEX_TO_DIFF
    global preProcessedData
    curSimilarity = 0
    for l in MAPPER:
        attribute = MAPPER[l]
        if l==22:
            if preProcessedData[attribute][i] in MEAN_VECTOR[attribute]:
                curSimilarity = curSimilarity + (1/len(MEAN_VECTOR[attribute]))
        else:
            diffVal = MAPPER_INDEX_TO_DIFF[l]
            curValMean = MEAN_VECTOR[attribute]
            lowerLimit = curValMean - diffVal
            upperLimit = curValMean + diffVal
            if (preProcessedData[attribute][i] >= lowerLimit) and (preProcessedData[attribute][i] <= upperLimit):
                curSimilarity += 1
    # print("SIMILARITY CALCULATED IS = ")
    # print(curSimilarity)
    return curSimilarity

def calcMSE(MEAN_CLUSTERS, MAP_CLUSTER_TO_INDICES,MAP_INDEX_TO_CLUSTER,k):
    global DATALEN
    print("DEBUG::IN MSE CALC")
    error = 0
    N = len(MAPPER)
    for i in range(DATALEN):
        clusterNum = MAP_INDEX_TO_CLUSTER[i]
        curSimilarity = getSimilarity(MEAN_CLUSTERS[clusterNum], i)
        curSimilarity = curSimilarity/N
        curSimilarity = 1 - curSimilarity
        error = error + curSimilarity**2
    return error

def distanceBetweenTwoVectors(i,l):
    global preProcessedData
    curSimilarity = 0
    for l in MAPPER:
        attribute = MAPPER[l]
        if l==22:
            if preProcessedData[attribute][i] == preProcessedData[attribute][l]:
                curSimilarity = curSimilarity + 1
        else:
            diffVal = MAPPER_INDEX_TO_DIFF[l]
            curValOth = preProcessedData[attribute][l]
            lowerLimit = curValOth - diffVal
            upperLimit = curValOth + diffVal
            if (preProcessedData[attribute][i] >= lowerLimit) and (preProcessedData[attribute][i] <= upperLimit):
                curSimilarity += 1
    curSimilarity = curSimilarity/len(MAPPER)
    distance = 1 - curSimilarity
    return distance

def calcMseSil(k,i):
    global DATALEN
    print("DEBUG::In msesil calc for k = "+str(k)+" and try = "+str(i))
    # global CLUSTERS_TO_INDICES
    PATH = "CLUSTERS_"+str(k)+"_"+str(i)+".json"
    CLUSTER = {}
    T_CLUSTER = {}
    with open(PATH,'r') as fp:
        CLUSTER = json.load(fp)
    MAP_INDEX_TO_CLUSTER = {}
    
    for j in CLUSTER:
        T_CLUSTER[int(j)] = CLUSTER[j]
    # CLUSTERS_TO_INDICES = T_CLUSTER
    for j in T_CLUSTER:
        indices = T_CLUSTER[j]
        for l in indices:
            MAP_INDEX_TO_CLUSTER[l] = j   
    
    # MEAN_CLUSTERS =  generateMean(T_CLUSTER)  #uncomment
    # MSE = calcMSE(MEAN_CLUSTERS, T_CLUSTER, MAP_INDEX_TO_CLUSTER, k) #uncomment
    MSE = 0 #comment

    totPoints = 0
    totSilVal = 0
    for j in T_CLUSTER:
        print("DEBUG::CALCULATING FOR CLUSTER "+str(j))
        indices = T_CLUSTER[j]
        numValuesInCluster = len(indices)
        totPoints += numValuesInCluster
        if numValuesInCluster > 1:
            for i in indices:
                a = 0
                for l in indices:
                    if i!=l:
                        a += distanceBetweenTwoVectors(i,l)
                a = a/(totPoints-1)
                mini = 1e9
                for m in T_CLUSTER:
                    if m!=j:
                        curclust = 0
                        indices2 = T_CLUSTER[m]
                        szclust = len(indices2)
                        b = 0
                        for l in indices2:
                            b += distanceBetweenTwoVectors(i, l)
                        b = b/szclust
                        if b<mini:
                            mini = b
                b = mini
                curSil = (b-a)/max(b,a)
                totSilVal+=curSil
    totSilVal = totSilVal/totPoints
    return MSE,totSilVal

def elbowSilhouettePlot():
    global axis
    mse_xcor = []
    mse_ycor = []
    silhouette_ycor = []
    ## To Compute mse and silhouette

    for k in range(3,8,2):
        avgMSE = 0
        avgSilhouette = 0
        for i in range(TRIES_PER_K):
            MSE,SIL = calcMseSil(k,i)
            avgMSE += MSE
            avgSilhouette += SIL
        avgMSE = avgMSE/TRIES_PER_K
        avgSilhouette = avgSilhouette/TRIES_PER_K
        mse_ycor.append(avgMSE)
        silhouette_ycor.append(avgSilhouette)
        mse_xcor.append(k)
    print(mse_xcor)
    print(silhouette_ycor)
    print(mse_ycor)

    ## Already computed mse and silhouette values copied from terminal
    mse_xcor = [3, 5, 7]
    mse_ycor = [11630.805841794223, 4729.406738121368, 3911.3918288615737]
    # silhouette_ycor = 

    axis[0].plot(mse_xcor,mse_ycor)
    axis[0].set_title("ELBOW METHOD PLOT")
    axis[0].set_xticks([1,3,5,7,9])

    axis[1].plot(mse_xcor,silhouette_ycor)
    axis[1].set_title("SILHOUETTE VALUE PLOT")
    axis[1].set_xticks([1,3,5,7,9])

def optimalK(datalen,Data):
    global DATALEN
    global preProcessedData
    designMapperIndexToDiff()
    DATALEN = datalen
    preProcessedData = Data
    elbowSilhouettePlot()
    # silhouettePlot()
    plt.show()
    