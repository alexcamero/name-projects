#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 13:25:46 2021

@author: bigship
"""

# Run k-means clustering algorithm on big matrix

def kmeans_run(most_clusters, iterations):
    
    with open('../json_files/year_nameratio_matrix.json','r') as file:
        big_matrix = json.load(file)
        
    X = np.array(big_matrix)
    result = []
    for k in range(2,most_clusters+1):
        km = KMeans(n_clusters = k, n_init = iterations).fit(X)
        labels = [int(km.labels_[i]) for i in range(len(km.labels_))]
        result.append({'clusters':k, 'SSE':km.inertia_, 'labels':labels})
                      
    with open('../json_files/kmeans_results.json','w') as file:
        json.dump(result,file)
        
def kmeans_names(most_clusters,iterations):
    with open('../json_files/big_names_data_nozero.json','r') as file:
        big_matrix_file = json.load(file)
    
    big_matrix = big_matrix_file['data']
    r = len(big_matrix)
    c = len(big_matrix[0]) * len(big_matrix[0][0])
        
    X = np.array(big_matrix)
    X.shape = (r,c)
    result = []
    for k in range(2,most_clusters+1):
        km = KMeans(n_clusters = k, n_init = iterations).fit(X)
        labels = [int(km.labels_[i]) for i in range(len(km.labels_))]
        result.append({'clusters':k, 'SSE':km.inertia_, 'labels':labels})
                      
    with open('../json_files/kmeans_results_names.json','w') as file:
        json.dump(result,file)