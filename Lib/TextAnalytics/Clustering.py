from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

sns.set_style('darkgrid')

def visualize_document_keyword_clusters(document_keyword_matrix, vocabulary, n_clusters = 5, top_n_keywords = 10):
    
    pca = PCA(2)
    pca_results = pca.fit_transform(document_keyword_matrix)
    
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=1)
    clustering_results = kmeans.fit_predict(pca_results)
    
    for label in np.unique(kmeans.labels_):
        keybert_cluster_results = document_keyword_matrix[clustering_results == label]
        keybert_cluster_results_col_sum = np.sum(keybert_cluster_results, axis=0)
        cluster_top_n_keywords = vocabulary[np.argsort(keybert_cluster_results_col_sum)[::-1][:top_n_keywords]]
        cluster = pca_results[clustering_results == label]
        plt.scatter(cluster[:, 0], cluster[:, 1], label=f'{label} ({cluster.shape[0]}) - ' + '\n'.join(wrap(', '.join(cluster_top_n_keywords), 50)))
        
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=10, color='black')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()
    
    return (clustering_results, pca_results)