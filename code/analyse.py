import numpy as np
import copy as copy
from matplotlib import pyplot as plt


# code explanation
## to be uncommented

def plotAgeDistro(ageData):
    ageData = ageData.to_numpy()
    
    #determining minimum and maximum age values in the dataset given
    minAge = 1000
    maxAge = 0
    for age in ageData:
        if age<minAge:
            minAge = age
        if age>maxAge:
            maxAge = age
    
    #making brakets for histogram 
    ageBrackets = []
    minLim = minAge//5
    maxLim = 0
    if maxAge%5 == 0:
        maxLim = (maxAge//5) + 1
    else:
        maxLim = (maxAge//5) + 2
    for i in range(minLim,maxLim):
        ageBrackets.append(i*5)
    
    # Creating histogram
    ##fig, ax = plt.subplots(figsize =(10, 7))
    ##ax.hist(ageData, ageBrackets)
 
    # Show plot
    ##plt.show()


def plotValueDistro(valData):
    #Comverting Millions and Thousands to actual decimals
    convertedValData = []
    exceptIndex = []
    sumC = 0
    numC = 0
    for i in range(len(valData)):
        value = copy.deepcopy(valData[i])
        last = value[len(value)-1]
        value = value[1:len(value)-1]
        if len(value) == 0:
            value = '0'
            exceptIndex.append(i)
        else:
            numC = numC + 1
        value = float(value)
        if last == 'M':
            value = value*1e6
        else:
            value = value*1e3
        value = int(value)
        sumC = sumC + value;
        convertedValData.append(value)

    #Handling noise/errors by assigning the average value
    sumC = sumC // numC
    for i in exceptIndex:
        convertedValData[i] = sumC
    
    # Creating histogram
    ## fig, ax = plt.subplots(figsize =(10, 7))
    ## ax.ticklabel_format(useOffset=False,style='plain')
    ## arr = ax.hist(convertedValData, bins = 10)
    ## for i in range(10):
    ##     plt.text(arr[1][i],arr[0][i],str(arr[0][i]))

    # Show plot
    ## plt.show()
    # ax.ticklabel_format(useOffset=True)

def plotFootDistro(footData):
    # Counting number of left footers and right footers, noise/errors are ignored
    counters = []
    lefters = 0
    righters = 0
    for foot in footData:
        if isinstance(foot, str):
            if foot[0] == 'L':
                lefters += 1
            elif foot[0] == 'R':
                righters += 1

    #defining various variable objects that are required to draw bar graph
    counters.append(lefters)
    counters.append(righters)
    tick_label = ['Left','Right']
    startIndex = [1,2]

    #creating Bar graph
    ## fig, ax = plt.subplots(figsize =(10, 7))
    ## ax.bar(startIndex,counters,tick_label = tick_label,width = 0.8)

    #Show plot
    ## plt.show()
def plotReputationDistro(repuData):
    counters = []

    # initialising
    for i in range(5):
        counters.append(0)

    # converting scanned floats to integers and counting
    repuData = repuData.fillna(0)
    repuData = repuData.astype(int)
    for reputation in repuData:
        if reputation>=1 and reputation<=5:
            counters[reputation-1] += 1

    # defining variables for plotting graph
    tick_label = [1,2,3,4,5]        
    startIndex = [1,2,3,4,5]

    #creating Bar graph
    ## fig, ax = plt.subplots(figsize =(10, 7))
    ## arr = ax.bar(startIndex,counters,tick_label = tick_label,width = 0.8)
    #displaying values over each bar in the graph
    ## for rect in arr:
        ## height = rect.get_height()
        ## ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,'%d' % int(height),ha='center', va='bottom')

    #Show plot
    ## plt.show()

def plotBodyTypeDistro(bodyData):
    # Getting all unique values in the given body type data set
    sampleSpace = bodyData.unique()

    # variables for graph
    tick_label = []
    startIndex = []

    # BookKeeping variables
    counters = []
    index = 0
    MP = {}

    # preparing lists in order to develop counters list
    for typ in sampleSpace:
        tick_label.append(typ)
        MP[typ] = index
        counters.append(0)
        index += 1
        startIndex.append(index)
    
    #devoloping counters list
    for typ in bodyData:
        counters[MP[typ]] += 1
    
    #creating Bar graph
    ## fig, ax = plt.subplots(figsize =(10, 7))
    ## arr = ax.bar(startIndex,counters,tick_label = tick_label,width = 0.8)
    # displaying values over each bar in the graph
    ## for rect in arr:
        ## height = rect.get_height()
        ## ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,'%d' % int(height),ha='center', va='bottom')

    #Show plot
    ## plt.show()
    
def plotClubsvsAvgWt(dataClub, dataWt):
    # Getting unique clubs
    uniqueClubs = set(dataClub)
    uniqueClubs = (list(uniqueClubs))
    # Book keeping variables
    MPCLUBTOINDEX = {}
    totWeightPerClub = []
    totNumPerClub = []
    # initialising
    for index in range(len(uniqueClubs)):
        MPCLUBTOINDEX[uniqueClubs[index]] = index
        totWeightPerClub.append(0)
        totNumPerClub.append(0)
    # calculating sum of weights for all the clubs 
    for index in range(len(dataWt)):
        if isinstance(dataWt[index], str):
            weight = dataWt[index]
            club = dataClub[index]
            weight = weight[:-3]
            weight = int(weight)
            totWeightPerClub[MPCLUBTOINDEX[club]] += weight
            totNumPerClub[MPCLUBTOINDEX[club]] += 1
    
    # variable that will ultiately be used to draw the graph
    avgWeightPerClub = []
    clubs = []
    # selecting the clubs that are at interval of 75 from the list of all unique clubs
    # All clubs can also be plotted but it will not be human interpretable 
    STEP = 75
    # calculating avg weights for clubs at an interval of 75
    for index in range(0,len(totWeightPerClub),STEP):
        value = totWeightPerClub[index]
        tot = totNumPerClub[index]
        value = value // tot
        avgWeightPerClub.append(value)
        clubs.append(uniqueClubs[index])
    # List required to build bar graph
    startIndex = []
    start = 0
    for i in range(0,len(uniqueClubs),STEP):
        startIndex.append(start)
        start += 0.2

    #creating Bar graph
    ## fig, ax = plt.subplots(figsize =(10, 7))
    ## arr = ax.bar(startIndex,avgWeightPerClub,tick_label = clubs,width = 0.15)
    # displaying values over each bar in the graph
    ## for rect in arr:
        ## height = rect.get_height()
        ## ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,'%d' % int(height),ha='center', va='bottom')

    #Show plot
    ## plt.show()
        
def plotClubsvsAvgHt(dataClub, dataHt):
    # Getting unique clubs
    uniqueClubs = set(dataClub)
    uniqueClubs = (list(uniqueClubs))
    # Book keeping variables
    MPCLUBTOINDEX = {}
    totHeightPerClub = []
    totNumPerClub = []
    # initialising
    for index in range(len(uniqueClubs)):
        MPCLUBTOINDEX[uniqueClubs[index]] = index
        totHeightPerClub.append(0)
        totNumPerClub.append(0)
    # calculating sum of heights for all the clubs 
    for index in range(len(dataHt)):
        if isinstance(dataHt[index], str):
            height = dataHt[index]
            club = dataClub[index]
            foot = int(height[0])
            inch = int(height[2:len(height)])
            height = foot*12 + inch
            height = int(height)
            totHeightPerClub[MPCLUBTOINDEX[club]] += height
            totNumPerClub[MPCLUBTOINDEX[club]] += 1
    
    # variable that will ultiately be used to draw the graph
    avgHeightPerClub = []
    clubs = []
    # selecting the clubs that are at interval of 75 from the list of all unique clubs
    # All clubs can also be plotted but it will not be human interpretable 
    STEP = 75
    # calculating avg Heights for clubs at an interval of 75
    for index in range(0,len(totHeightPerClub),STEP):
        value = totHeightPerClub[index]
        tot = totNumPerClub[index]
        value = value // tot
        avgHeightPerClub.append(value)
        clubs.append(uniqueClubs[index])
    # List required to build bar graph
    startIndex = []
    start = 0
    for i in range(0,len(uniqueClubs),STEP):
        startIndex.append(start)
        start += 0.2

    #creating Bar graph
    ## fig, ax = plt.subplots(figsize =(10, 7))
    ## arr = ax.bar(startIndex,avgHeightPerClub,tick_label = clubs,width = 0.15)
    # displaying values over each bar in the graph
    ## for rect in arr:
        ## height = rect.get_height()
        ## ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,'%d' % int(height),ha='center', va='bottom')

    #Show plot
    ## plt.show()       

def analyse(data):
    plotAgeDistro(data['Age'])
    plotValueDistro(data['Value'])
    plotFootDistro(data["Preferred Foot"])
    plotReputationDistro(data["International Reputation"])
    plotBodyTypeDistro(data['Body Type'])
    plotClubsvsAvgWt(data['Club'], data['Weight'])
    plotClubsvsAvgHt(data['Club'], data['Height'])