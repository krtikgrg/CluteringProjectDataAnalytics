from analyse import analyse
from kmeans import kMeans
from clusterVisualise import runVisualise
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