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
    fig, ax = plt.subplots(figsize =(10, 7))
    arr = ax.bar(startIndex,counters,tick_label = tick_label,width = 0.8)
    # displaying values over each bar in the graph
    for rect in arr:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,'%d' % int(height),ha='center', va='bottom')

    #Show plot
    plt.show()
    

def analyse(data):
    plotAgeDistro(data['Age'])
    plotValueDistro(data['Value'])
    plotFootDistro(data["Preferred Foot"])
    plotReputationDistro(data["International Reputation"])
    plotBodyTypeDistro(data['Body Type'])