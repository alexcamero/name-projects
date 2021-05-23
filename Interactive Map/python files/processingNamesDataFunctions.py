#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Alex Cameron
"""

import csv, json, os, string
import networkx as nx

header_state = ['state','sex','year','name','number']
header_year = ['name','sex','number']

states = ['NAT', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 
          'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
          'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 
          'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 
          'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
letters = list(string.ascii_uppercase)


minYear=1937
maxYear=2020
directoryState = '../../name_data/names_by_state/'
directoryYear = '../../name_data/names_by_year/'
namesFilePath = 'names_list.json'

def makeListOfAllNames(min_year = minYear, max_year = maxYear, 
                       directory_state = directoryState, 
                       directory_year = directoryYear, 
                       names_file_target = namesFilePath):

    names = set()
    
    print("Making list of all names from state data........")
    
    for i in range(1,52):
        print("Processing "+states[i]+"...........")
        path = os.path.join(directory_state, states[i]+".TXT")
        with open(path,'r') as file:
            csv_reader = csv.reader(file)
            list_of_rows = list(csv_reader)
            for row in list_of_rows:
                if int(row[2])>=min_year:
                    names.add(row[3])
                    
    for y in range(min_year,max_year+1):
        print("Processing "+str(y)+"...........")
        path = os.path.join(directory_year, "yob"+str(y)+".txt")
        with open(path,'r') as file:
            csv_reader = csv.reader(file)
            list_of_rows = list(csv_reader)
            for row in list_of_rows:
                names.add(row[0])

    names = list(names)
    names.sort()
    
    n=len(names)
    
    with open(names_file_target,'w') as file:
        json.dump(names,file)
        
    print(f"JSON file of all names has been created. There are {n} distinct names that appear in the data.")
        


def makeIndividualNameFiles(min_year = minYear, max_year = maxYear, directory_state = directoryState, directory_year = directoryYear, names_file = namesFilePath):
    
    for let in letters:
        path = os.path.join("../namesData/", let)
        os.mkdir(path)
    
    
    with open(names_file,'r') as file:
        names = json.load(file)
    
    bigD = {}
    
    print("Making the big dictionary...........")
    
    for name in names:
        bigD[name]=[[0 for s in range(52)] for y in range(min_year,max_year+1)]
        
    for i in range(1,52):
        print("Processing "+states[i]+"...........")
        path = os.path.join(directory_state, states[i]+".TXT")
        with open(path,'r') as file:
            csv_reader = csv.reader(file)
            list_of_rows = list(csv_reader)
            for row in list_of_rows:
                if int(row[2])>=min_year:
                    bigD[row[3]][int(row[2])-min_year][i]+=int(row[4])
                    
    for y in range(min_year,max_year+1):
        print("Processing "+str(y)+"...........")
        path = os.path.join(directory_year, "yob"+str(y)+".txt")
        with open(path,'r') as file:
            csv_reader = csv.reader(file)
            list_of_rows = list(csv_reader)
            for row in list_of_rows:
                bigD[row[0]][y-min_year][0] += int(row[2])
                
    print("Producing individual files for each name...........")
                
    for name in bigD.keys():
        path = os.path.join('../namesData/'+name[0:1]+'/', name+'.json')
        with open(path,'w') as file:
            json.dump(bigD[name],file)
            
    print("All done!")
    
def most_popular_data(min_year = minYear, max_year = maxYear, directory_state = directoryState, directory_year = directoryYear):
    most_pop_national = {'F':{}, 'M':{}, 'B':{}}
    for Y in range(min_year,max_year+1):
        file="yob" + str(Y) + ".txt"
        path = os.path.join(directory_year, file)
        with open(path, 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            list_of_rows = list(csv_reader)
        most_pop_national['F'][Y]=[[list_of_rows[i][0],list_of_rows[i][2]] for i in range(10)]
        for row in list_of_rows[10:]:
            if row[2] == most_pop_national['F'][Y][-1][1]:
                most_pop_national['F'][Y].append([row[0],row[2]])
            else:
                break
        i=0
        most_pop_national['M'][Y] = []
        for row in list_of_rows:
            if ((i<10) and (row[1] == 'M')) or ((i>=10) and (row[2]==most_pop_national['M'][Y][-1][1])):
                most_pop_national['M'][Y].append([row[0], row[2]])
                i+=1
            elif i >= 10:
                break
        CombinedList = most_pop_national['F'][Y] + most_pop_national['M'][Y]
        CombinedList.sort(key = lambda x: x[1], reverse = True)
        most_pop_national['B'][Y] = CombinedList[0:10]
        for pair in CombinedList[10:]:
            if pair[1] == CombinedList[9][1]:
                most_pop_national['B'][Y].append(pair)
            else:
                break
            
    most_pop_states = {'F':{}, 'M':{}, 'B':{}}
    for Y in range(min_year,max_year+1):
        most_pop_states['F'][Y] = {}
        most_pop_states['M'][Y] = {}
        most_pop_states['B'][Y] = {}
    for i in range(1,52):
        file = states[i] + ".TXT"
        path = os.path.join(directory_state, file)
        with open(path, 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            list_of_rows = list(csv_reader)
        year = -1
        i=0
        state = list_of_rows[0][0]
        for row in list_of_rows:
            if (int(row[2]) >= min_year) and (int(row[2]) != year):
                i = 1
                year = int(row[2])
                most_pop_states[row[1]][year][state] = [[row[3], row[4]]]
            elif (int(row[2]) >= min_year) and (i<5):
                i+=1
                most_pop_states[row[1]][year][state].append([row[3], row[4]])
            elif (int(row[2]) >= min_year) and (i == 5) and (row[4] == most_pop_states[row[1]][year][state][-1][1]):
                most_pop_states[row[1]][year][state].append([row[3], row[4]])
        for year in range(min_year,max_year+1):
            CombinedList = most_pop_states['F'][year][state] + most_pop_states['M'][year][state]
            CombinedList.sort(key = lambda x: x[1], reverse = True)
            most_pop_states['B'][year][state] = CombinedList[0:5]
            for pair in CombinedList[5:]:
                if pair[1] == CombinedList[4][1]:
                    most_pop_states['B'][year][state].append(pair)
                else:
                    break
    with open('../mostPopStates.json','w') as file:
        json.dump(most_pop_states,file)
        
    with open('../mostPopNat.json','w') as file:
        json.dump(most_pop_national,file)
                

def make_names_graph(sex='B',min_year=minYear,max_year=maxYear):
    max_clique = 0
    names_graph = nx.Graph()
    with open('../mostPopStates.json') as file:
        MPS = json.load(file)
    with open('../mostPopNat.json') as file:
        MPN = json.load(file)
    MEN = MPS[sex]
    MEN_nat = {str(Y):MPN[sex][str(Y)][0][0] for Y in range(min_year,max_year+1)}

    for year in range(min_year,max_year+1):
        Temp = {MEN[str(year)][states[i]][0][0] for i in range(1,52)}
        for i in range(1,52):
            win_num = MEN[str(year)][states[i]][0][1]
            for j in range(1,5):
                if MEN[str(year)][states[i]][j][1] == win_num:
                    Temp.add(MEN[str(year)][states[i]][j][0])
        bestman = MEN_nat[str(year)]
        Temp.add(bestman)
        Temp.remove(bestman)
        max_clique = max([max_clique,len(Temp)])
        T = nx.complete_graph(list(Temp))
        names_graph.add_edges_from(list(T.edges))
    return names_graph, max_clique

        
def weighted_grays(sex='B',min_year=minYear,max_year=maxYear):
    with open('../mostPopStates.json') as file:
        MPS = json.load(file)
    with open('../mostPopNat.json') as file:
        MPN = json.load(file)
    MEN = MPS[sex]
    MEN_nat_winners = {str(Y):MPN[sex][str(Y)][0][0] for Y in range(min_year,max_year+1)}
    weights={}
    for year in range(min_year,max_year+1):
        for i in range(1,52):
            win_num = MEN[str(year)][states[i]][0][1]
            winners = [MEN[str(year)][states[i]][0][0]]
            for j in range(1,5):
                if MEN[str(year)][states[i]][j][1] == win_num:
                    winners.append(MEN[str(year)][states[i]][j][0])
            for winner in winners:
                if winner != MEN_nat_winners[str(year)]:
                    if winner in weights.keys():
                        weights[winner]+=1
                    else:
                        weights[winner]=1
    list_of_weights = [(name,weights[name]) for name in weights.keys()]
    list_of_weights.sort(key=lambda x: x[1], reverse=True)
    ordered_list = [name for name,_ in list_of_weights]
    return ordered_list

def greedy_coloring(sex='B',min_year=minYear,max_year=maxYear):
    G, _ = make_names_graph(sex, min_year, max_year)
    names_in_order = weighted_grays(sex, min_year, max_year)
    coloring = {x:-1 for x in names_in_order}
    for x in names_in_order:
        i=0
        nbh_colors = {coloring[y] for y in list(G.adj[x])}
        while i in nbh_colors:
            i+=1
        coloring[x] = i
    return coloring

def make_grayConnection_file(min_year=minYear,max_year=maxYear):
    gray_connection = {sex:greedy_coloring(sex,min_year,max_year) for sex in ['F','M','B']}
    with open('../grayConnection.json','w') as file:
        json.dump(gray_connection,file)
        
make_grayConnection_file()