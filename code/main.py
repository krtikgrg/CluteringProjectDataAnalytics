from analyse import analyse
import pandas as pd
# df.iloc[2:4,1]
PATH = "../data/football_data.csv"
data = pd.read_csv(PATH)


#############  PERFORMING ANALYSIS #############
analyse(data)
