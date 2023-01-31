import numpy as np
from Lib.Utilities import Output
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


def classify_documents_via_clusters(document_links, document_keyword_matrix, vocabulary, input_keywords, top_n_keywords = 10, relevance_threshold = 0.65):
    
    # preprocess input keywords to ensure they are of the same case as the vocabulary 
    input_keywords = [keyword for sub_keywords in input_keywords for keyword in sub_keywords.lower().split()]
    
    pca = PCA(2)
    pca_results = pca.fit_transform(document_keyword_matrix)
    
    kmeans = KMeans(n_clusters=2, init='k-means++', random_state=1)
    clustering_results = kmeans.fit_predict(pca_results)
    
    doc_classes = np.empty(shape=(kmeans.labels_.shape[0]), dtype=object)
    
    cluster_0_results = document_keyword_matrix[clustering_results == 0]
    cluster_0_results_col_sum = np.sum(cluster_0_results, axis=0)
    cluster_0_top_n_keywords = vocabulary[np.argsort(cluster_0_results_col_sum)[::-1][:top_n_keywords]]

    cluster_1_results = document_keyword_matrix[clustering_results == 1]
    cluster_1_results_col_sum = np.sum(cluster_1_results, axis=0)
    cluster_1_top_n_keywords = vocabulary[np.argsort(cluster_1_results_col_sum)[::-1][:top_n_keywords]]
    
    cluster_0_input_kw_matches = np.intersect1d(cluster_0_top_n_keywords, input_keywords)
    cluster_1_input_kw_matches = np.intersect1d(cluster_1_top_n_keywords, input_keywords)
    
    relevant_cluster = 0 if len(cluster_0_input_kw_matches) > len(cluster_1_input_kw_matches) else 1
    
    for idx, label in enumerate(kmeans.labels_):
        doc_classes[idx] = 'Relevant' if label == relevant_cluster else 'Irrelevant'

    Output.write_classification_results_to_csv(document_links, doc_classes)