from analyse import analyse
from kmeans import kMeans
import pandas as pd
# df.iloc[2:4,1]
PATH = "../data/football_data.csv"
data = pd.read_csv(PATH)


#############  PERFORMING ANALYSIS #############
analyse(data)

# print(len(data))

#############  PERFORMING KMEANS   #############
kMeans(data)
