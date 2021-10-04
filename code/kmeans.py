from map import MAPPER
preProcessedData = {}
diffTwoIndices = [3, 26]
diffZeroIndices = [5, 9, 14, 15, 16, 17, 18, 19, 21, 22]
diffFiveIndices = [7, 8, 27]
diffTwoHundredIndices = [13]
MAPPER_INDEX_TO_DIFF = {}

def designMapperIndexToDiff():
    for i in diffZeroIndices:
        MAPPER_INDEX_TO_DIFF[i] = 0
    for i in diffTwoIndices:
        MAPPER_INDEX_TO_DIFF[i] = 2
    for i in diffFiveIndices:
        MAPPER_INDEX_TO_DIFF[i] = 5
    for i in diffTwoHundredIndices:
        MAPPER_INDEX_TO_DIFF[i] = 200
    
def makeDiffFive():
    nuList = range(28,88)
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

def preProcessAccordingToList(data,toProcessIndices):
    for i in toProcessIndices:
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

def kMeans(data):
    preProcessedData["Height"] = preProcessHeight(data["Height"]) #26
    preProcessedData["Weight"] = preProcessWeight(data["Weight"]) #27
    accToList = [5, 9, 14, 18, 19, 21, 22]
    preProcessAccordingToList(data,accToList)
    accToList = range(28,54)
    preProcessRemoveSpare(data,accToList)
    accToList = [5, 9, 14, 18, 19, 21, 22]
    toConcat = range(26,54)
    accToList = accToList + toConcat
    copyOriginalData(data,accToList)
    makeDiffFive()
    designMapperIndexToDiff()