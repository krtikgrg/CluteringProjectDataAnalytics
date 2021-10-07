from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as plt



def dendoGram(df1):
    df1 = df1.reset_index()
    scaling = StandardScaler()
    scaling.fit(df1)
    scaled_data = scaling.transform(df1)
    pca = PCA(n_components = 2)
    pca.fit(scaled_data)
    reduced_data = pca.transform(scaled_data)

    plt.figure(figsize=(10, 7))
    plt.title("Cluster Dendograms bottom up strategy")
    dend = shc.dendrogram(shc.linkage(reduced_data, method='ward'))
    plt.show()

