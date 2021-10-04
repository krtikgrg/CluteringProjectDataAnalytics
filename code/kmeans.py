from map import MAPPER
import random
preProcessedData = {}
diffTwoIndices = [3, 26]
diffZeroIndices = [15, 16, 17]
diffListMethod = [22]
diffFiveIndices = [7, 8, 27]
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
    MAPPER_INDEX_TO_DIFF[22] = "LIST"
    
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
            preProcessedData[MAPPER[i]] = data[MAPPER[i]]

def generateMean(MAP):
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
            sumAll = sumAll/numElements
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
    return MAP_CLUSTER_TO_MEAN

def runKmeansAlgo(k):
    initialPopu = random.sample(xrange(0,18207),k)
    MAP_CLUSTER_TO_INDICES = {}
    MAP_INDEX_TO_CLUSTER = {}
    for i in range(0,18207):
        MAP_INDEX_TO_CLUSTER[i] = -1
    for i in range(0,k):
        onlyIndex = []
        onlyIndex.append(initialPopu[i])
        MAPPER_CLUSTER_TO_INDICES[i] = onlyIndex
        MAP_INDEX_TO_CLUSTER[initialPopu[i]] = i
    
    MEAN_CLUSTERS = generateMean(MAPPER_CLUSTER_TO_INDICES)
    change = 1

    while change:
        NEW_INDEX_TO_CLUSTER = {}
        for i in range(18207):
            similarity = 0
            currentGroup = -1
            for j in range(k):
                curSimilarity = 0
                MEAN_VECTOR = MEAN_CLUSTERS[j]
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
                if curSimilarity > similarity:
                    similarity = curSimilarity
                    currentGroup = j
            NEW_INDEX_TO_CLUSTER[i] = j
        
        change = 0
        for i in range(18207):
            if NEW_INDEX_TO_CLUSTER[i] != MAP_INDEX_TO_CLUSTER[i]:
                change = 1
                MAP_INDEX_TO_CLUSTER = NEW_INDEX_TO_CLUSTER
                break
        
        if change:
            NEW_MAPPER_CLUSTER_TO_INDICES = {}
            for i in range(k):
                NEW_MAPPER_CLUSTER_TO_INDICES[i] = []
            for i in range(18207):
                NEW_MAPPER_CLUSTER_TO_INDICES[NEW_INDEX_TO_CLUSTER[i]].append(i)
            MAPPER_CLUSTER_TO_INDICES = NEW_MAPPER_CLUSTER_TO_INDICES
            MEAN_VECTOR = generateMean(MAPPER_CLUSTER_TO_INDICES)

def kMeans(data):
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
    runKmeansAlgo(k)