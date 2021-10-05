from map import MAPPER
import copy
import random
import json
preProcessedData = {}
diffTwoIndices = [3, 26]
diffZeroIndices = [15, 16, 17]
diffListMethod = [22]
diffFiveIndices = [7, 8, 27]
diffTwoHundredIndices = [13]
MAPPER_INDEX_TO_DIFF = {}
gk = 0
gi = 0
DATALEN = 0

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
    
def makeDiffFive():
    nuList = list(range(28,88))
    global diffFiveIndices
    diffFiveIndices = diffFiveIndices + nuList

def preProcessHeight(dataHt):
    nuDataHt = []
    for index in range(len(dataHt)):
        if isinstance(dataHt[index], str):
            foot = int(dataHt[index][0])
            inch = int(dataHt[index][2:len(dataHt[index])])
            nuDataHt.append(foot*12.0+inch)
        else:
            nuDataHt.append(0)
    return nuDataHt

def preProcessWeight(dataWt):
    nuDataWt = []
    for index in range(len(dataWt)):
        if isinstance(dataWt[index], str):
            weight = dataWt[index]
            weight = int(weight[:-3])
            nuDataWt.append(weight)
        else:
            nuDataWt.append(0)
    return nuDataWt

def preProcessAccordingToList(data):
    i = 22
    attribute = MAPPER[i]
    nuAttrData = []
    for val in data[attribute]:
        nuList = []
        nuList.append(val)
        nuAttrData.append(nuList)
    preProcessedData[attribute] = nuAttrData

def preProcessRemoveSpare(data,toProcessIndices):
    for i in toProcessIndices:
        attribute = MAPPER[i]
        nuAttrData = []
        for val in data[attribute]:
            if isinstance(val, str):
                nuStr = val[:-2]
                nuStr = int(nuStr)
                nuAttrData.append(nuStr)
            else:
                nuAttrData.append(0)
        preProcessedData[attribute] = nuAttrData

def copyOriginalData(data,accToList):
    for i in MAPPER:
        if i not in accToList:
            preProcessedData[MAPPER[i]] = copy.deepcopy(data[MAPPER[i]])

def generateMean(MAP):
    # print("DEBUG::IN GENERATE MEAN")
    global preProcessedData
    MAP_CLUSTER_TO_MEAN = {}
    for i in MAP:
        indices = MAP[i]
        # print()
        # print("DEBUG::Indices in cluster i")
        # print(i)
        # print(indices)
        # print()
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
    global gk
    global gi
    print("DEBUG::IN MSE CALC")
    error = 0
    N = len(MAPPER)
    for i in range(DATALEN):
        clusterNum = MAP_INDEX_TO_CLUSTER[i]
        curSimilarity = getSimilarity(MEAN_CLUSTERS[clusterNum], i)
        curSimilarity = curSimilarity/N
        curSimilarity = 1 - curSimilarity
        error = error + curSimilarity**2
    print(error)
    with open("CLUSTERS_"+str(gk)+"_"+str(gi)+".json","w") as fp:
        json.dump(MAP_CLUSTER_TO_INDICES, fp)

def runKmeansAlgo(k):
    global DATALEN
    print("DEBUG::IN KMEANS ALGO")
    # print(DATALEN)
    global MAPPER_INDEX_TO_DIFF
    global preProcessedData
    initialPopu = random.sample(range(0,DATALEN),k)
    # print(initialPopu)
    MAP_CLUSTER_TO_INDICES = {}
    MAP_INDEX_TO_CLUSTER = {}
    for i in range(0,DATALEN):
        MAP_INDEX_TO_CLUSTER[i] = -1
    for i in range(0,k):
        onlyIndex = []
        onlyIndex.append(initialPopu[i])
        MAP_CLUSTER_TO_INDICES[i] = copy.deepcopy(onlyIndex)
        MAP_INDEX_TO_CLUSTER[initialPopu[i]] = i
    
    MEAN_CLUSTERS = generateMean(MAP_CLUSTER_TO_INDICES)
    change = 1
    iteration = 1

    while change:
        print("iteration = "+str(iteration))
        NEW_INDEX_TO_CLUSTER = {}
        for i in range(DATALEN):
            similarity = 0
            currentGroup = -1
            for j in range(k):
                MEAN_VECTOR = MEAN_CLUSTERS[j]
                curSimilarity = getSimilarity(MEAN_VECTOR,i)
                # print("SIMILARITY CALCULATED IS = ")
                # print(curSimilarity)
                if curSimilarity > similarity:
                    # print("in great for "+ str(j))
                    similarity = curSimilarity
                    currentGroup = j
            NEW_INDEX_TO_CLUSTER[i] = currentGroup
        
        change = 0
        for i in range(DATALEN):
            if NEW_INDEX_TO_CLUSTER[i] != MAP_INDEX_TO_CLUSTER[i]:
                change = 1
                MAP_INDEX_TO_CLUSTER = copy.deepcopy(NEW_INDEX_TO_CLUSTER)
                break
        
        if change:
            NEW_MAP_CLUSTER_TO_INDICES = {}
            for i in range(k):
                NEW_MAP_CLUSTER_TO_INDICES[i] = []
            for i in range(DATALEN):
                NEW_MAP_CLUSTER_TO_INDICES[NEW_INDEX_TO_CLUSTER[i]].append(i)
            MAP_CLUSTER_TO_INDICES = copy.deepcopy(NEW_MAP_CLUSTER_TO_INDICES)
            MEAN_CLUSTERS = generateMean(MAP_CLUSTER_TO_INDICES)
        iteration += 1
    calcMSE(MEAN_CLUSTERS,MAP_CLUSTER_TO_INDICES,MAP_INDEX_TO_CLUSTER,k)

def kMeans(data):
    global DATALEN
    global gk
    global gi
    DATALEN = len(data)
    # print(DATALEN)
    preProcessedData["Height"] = preProcessHeight(data["Height"]) #26
    preProcessedData["Weight"] = preProcessWeight(data["Weight"]) #27
    # preProcessAccordingToList(data) ##MAY REQUIRE UNCOMMENTING
    accToList = list(range(28,54))
    preProcessRemoveSpare(data,accToList)
    accToList = [] #[22] MAY REQUIRE UNCOMMENTING
    toConcat = list(range(26,54))
    accToList = accToList + toConcat
    copyOriginalData(data,accToList)
    makeDiffFive()
    designMapperIndexToDiff()
    runKmeansAlgo(3)
    # for k in range(3,8,2):
        # gk = k
        # print()
        # print()
        # print("DEBUG::RUNNING K MEANS FOR k="+str(k))
        # for i in range(5):
            # gi = i
            # runKmeansAlgo(k)