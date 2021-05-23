#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 15:11:55 2021

@author: bigship
"""

import json, os, csv
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

directory_state = '../name_data/namesbystate'
directory_year = '../name_data/namesbyyear'

start_year = 1937
end_year = 2019


# Make a list of distinct names from state files

def make_names_states():

    names = set()

    for file in os.listdir(directory_state):
            if file.endswith(".TXT"):
                path = os.path.join(directory_state, file)
                with open(path, 'r') as read_obj:
                    csv_reader = csv.reader(read_obj)
                    list_of_rows = list(csv_reader)
                for row in list_of_rows:
                    if (int(row[2]) >= start_year) and (int(row[2]) <= end_year):
                        names.add(row[3])
                        
    names = list(names)
    names.sort()

    n=len(names)
    print(f"Length of the names list from the state data is {n}.")
    
    return names

# Make a list of distinct names from yearly national files

def make_names_national():
    
    names = set()
                
    for file in os.listdir(directory_year):
            if file.endswith(".txt"):
                year = int(file[3:7])
                if (year <= end_year) and (year >= start_year):
                    path = os.path.join(directory_year, file)
                    with open(path, 'r') as read_obj:
                        csv_reader = csv.reader(read_obj)
                        list_of_rows = list(csv_reader)
                    for row in list_of_rows:
                        names.add(row[0])
                        
    names = list(names)
    names.sort()

    n=len(names)
    print(f"Length of the names list from the national data is {n}.")
    
    return names
                

# Make a matrix with rows indexed by year and columns indexed by name.
# Each entry gives the ratio of the count of the name out of total count for
# that year
       
        
def years_matrix(distinct_names):
    
    # Make dictionary with key-value pairs of form year:total  
    with open('../json_files/national_totals.json','r') as file:
        totals = json.load(file)
    year_totals = {}
    for row in totals:
        if (row[0]>=start_year) and (row[0]<=end_year):
            year_totals[row[0]] = row[1]
            
    # Make disctionary with key-value pairs of form name:column_index
    name_index = {}
    n = len(distinct_names)
    for i in range(n):
        name_index[distinct_names[i]] = i
        
    # Initialize big matrix with rows indexed by year, columns by name,
    # each number represents the ratio of that name out of total names
    
    big_matrix = [[0 for _ in range(n)] for year in range(start_year,end_year+1)]
    
    # Fill in with data
    
    for year in range(start_year,end_year+1):
        path = directory_year + "/yob" + str(year) + ".txt"
        with open(path, 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            list_of_rows = list(csv_reader)
        for row in list_of_rows:
            big_matrix[year - start_year][name_index[row[0]]] += int(row[2])
        for i in range(n):
            big_matrix[year - start_year][i] = big_matrix[year - start_year][i] / year_totals[year]
            
    # Return matrix
    print("Matrix of years, names is complete.")
    return big_matrix
        

# 3d tensor indexed by names, state, year. Each entry contains the ratio of
# the name count in that state and year relative to the overall count for that
# name over all states and years. NOTE: This total will be different than the
# sum of the national totals for the name since many names make the cutoff
# for the national list, but not many of the state lists.

def names_matrix(distinct_names):
    
    # Make quick look-up of each name's index
    name_index = {}
    n = len(distinct_names)
    for i in range(n):
        name_index[distinct_names[i]] = i
        
    # We will normalize by each name's total count at the end
    
    name_norms = [0 for _ in range(n)]
        
    # Initialize big 3d tensor indexed by the distinct names, state, year
    
    big_matrix = [[[0 for year in range(start_year,end_year+1)] for _ in range(51)] for _ in range(n)]
    
    # Make list of states to reference for index
    
    list_of_states = []
    
    index_state = -1
    for file in os.listdir(directory_state):
            if file.endswith(".TXT"):
                
                list_of_states.append(file[0:2])
                index_state += 1
                
                path = os.path.join(directory_state, file)
                with open(path, 'r') as read_obj:
                    csv_reader = csv.reader(read_obj)
                    list_of_rows = list(csv_reader)
                    
                for row in list_of_rows:
                    if (int(row[2]) >= start_year) and (int(row[2]) <= end_year):
                        index_year = int(row[2]) - start_year
                        index_name = name_index[row[3]]
                        new_count = int(row[4])
                        
                        big_matrix[index_name][index_state][index_year] += new_count
                        name_norms[index_name] += new_count
    
    # Normalize the data
    
    temp_array = np.array(big_matrix)
    
    for index_name in range(n):
        temp_array[i] = temp_array[i] / name_norms[i]
        
    big_matrix = temp_array.tolist()

    # Package it all together to return
    
    big_package = {'names':distinct_names,'states':list_of_states,'years':[year for year in range(start_year,end_year+1)],'data':big_matrix, 'totals':name_norms}
    print("Tensor of names, states, years is complete.")
    return big_package

def kmeans_years(year_vectors, most_clusters, iterations):
        
    X = np.array(year_vectors)
    result = []
    for k in range(2,most_clusters+1):
        km = KMeans(n_clusters = k, n_init = iterations).fit(X)
        labels = [int(km.labels_[i]) for i in range(len(km.labels_))]
        result.append({'clusters':k, 'SSE':km.inertia_, 'labels':labels})
                      
    return result
        
def kmeans_names(name_matrices, most_clusters, iterations):
    
    r = len(name_matrices)
    c = len(name_matrices[0]) * len(name_matrices[0][0])
        
    X = np.array(name_matrices)
    X.shape = (r,c)
    result = []
    for k in range(2,most_clusters+1):
        km = KMeans(n_clusters = k, n_init = iterations).fit(X)
        labels = [int(km.labels_[i]) for i in range(len(km.labels_))]
        result.append({'clusters':k, 'SSE':km.inertia_, 'labels':labels})
                      
    return result



# distinct_names_national = make_names_national()

# with open("../json_files/distinct_names_national.json",'w') as file:
#     json.dump(distinct_names_national,file)
    
# y_matrix = years_matrix(distinct_names_national)
    
# with open("../json_files/national_year_vectors.json",'w') as file:
#     json.dump(y_matrix,file)
    
# distinct_names_states = make_names_states()

# with open("../json_files/distinct_names_states.json",'w') as file:
#     json.dump(distinct_names_states,file)
    
# big_data = names_matrix(distinct_names_states)

# with open("../json_files/name_stateyear_matrices.json",'w') as file:
#     json.dump(big_data,file)
    
# name_matrices = big_data['data']

# result_years = kmeans_years(y_matrix, 20,20)

# with open("../json_files/kmeans_on_year_vectors.json",'w') as file:
#     json.dump(result_years,file)
    
# X = []
# Y = []
# for k in range(2,21):
#     X.append(k)
#     Y.append(result_years[k-2]['SSE'])
# plt.plot(X,Y)

# with open('../json_files/name_stateyear_matrices.json','r') as file:
#     big_data = json.load(file)
    
# name_matrices = big_data['data']

# result_names = kmeans_names(name_matrices, 30, 10)

# with open("../json_files/kmeans_on_name_matrices.json",'w') as file:
#     json.dump(result_names,file)
    
# X = []
# Y = []
# for k in range(2,31):
#     X.append(k)
#     Y.append(result_names[k-2]['SSE'])
# plt.plot(X,Y)

with open("../json_files/kmeans_on_name_matrices.json",'r') as file:
    result_names = json.load(file)
    
with open('../json_files/name_stateyear_matrices.json','r') as file:
    big_data = json.load(file)
    
totals = big_data['totals']

for k in range(2,31):
    names_per_cluster = [0 for _ in range(k)]
    total_per_cluster = [0 for _ in range(k)]
    labels = result_names[k-2]['labels']
    for i in range(len(labels)):
        names_per_cluster[labels[i]] += 1
        total_per_cluster[labels[i]] += totals[i]
    result_names[k-2]['names_per_cluster'] = names_per_cluster
    result_names[k-2]['total_per_cluster'] = total_per_cluster
        
with open("../json_files/kmeans_on_name_matrices_plus.json",'w') as file:
    json.dump(result_names,file)
