from analyse import analyse
from kmeans import kMeans
from clusterVisualise import runVisualise
from optimal import optimalK
from bottomUpAgglomerative import bottomUp,bottomUpReduced
import pandas as pd
import numpy as np
from map import MAPPER
# df.iloc[2:4,1]
PATH = "../data/football_data.csv"
data = pd.read_csv(PATH)

#############  PERFORMING ANALYSIS #############

# analyse(data)



#############  PERFORMING KMEANS   #############

# kMeans(data)  # UNCOMMENT TO RUN KMEANS ALGO



#############  CLUSTER VISUALISE   #############

df1 = pd.read_csv("df.csv")
df1.fillna(0)
# print(df1)
for i in MAPPER:
    df1[MAPPER[i]] = df1[MAPPER[i]].fillna(df1[MAPPER[i]].mode().iloc[0])
    df1[MAPPER[i]].fillna(0)
    df1[MAPPER[i]].astype(int)
# print(df1)
runVisualise(data,df1)



#############  ELBOW AND SILHOUETTE FOR OPTIMAL K  #############
# preProcessedData = pd.read_csv("df.csv")
# optimalK(len(data),preProcessedData)

#############  AGGLOMERATIVE CLUSTERING TRY 1(all features) [FAILED]  #############
# preProcessedData = pd.read_csv("df.csv")
# bottomUp(preProcessedData)

#############  AGGLOMERATIVE CLUSTERING TRY 2(reduced features using pca) [SUCCESS] #############

# df1 = pd.read_csv("df.csv")
# df1.fillna(0)
# # print(df1)
# for i in MAPPER:
#     df1[MAPPER[i]] = df1[MAPPER[i]].fillna(df1[MAPPER[i]].mode().iloc[0])
#     df1[MAPPER[i]].fillna(0)
#     df1[MAPPER[i]].astype(int)
# bottomUpReduced(df1)