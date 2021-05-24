
import csv, json, os, string
import networkx as nx

"""To produce all of the json files you need to make the interactive 
map you can set the min and max year in the following lines as well as
the paths to where you have the csv files containing the data and
the location you'd like the output to go to.
Then you can just run this file."""

minYear=1937
maxYear=2020
directoryState = '../../Name Data/namesbystate/'
directoryYear = '../../Name Data/namesbyyear/'
namesFilePath = 'distinct_names_list.json'
siteFolder = '../website files/'

header_state = ['state','sex','year','name','number']
header_year = ['name','sex','number']

states = ['NAT', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 
          'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
          'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 
          'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 
          'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
letters = list(string.ascii_uppercase)

def make_list_of_all_names(min_year = minYear, max_year = maxYear, 
                       directory_year = directoryYear, 
                       names_file_target = namesFilePath):
    """"This function returns a list of distinct names found in all files from
    directory_year of the form 'yobYYYY.txt' where YYYY is a year between
    min_year and max_year (inclusive). All years in this range must have a
    file in the directory. The resulting list of distinct names will be
    written to the path given to names_file_target."""

    #initialize the set of names
    names = set()
    
    #open the csv files and add names to the set
    for y in range(min_year, max_year + 1):
        path = os.path.join(directory_year, "yob" + str(y) + ".txt")
        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            list_of_rows = list(csv_reader)
            for row in list_of_rows:
                names.add(row[0])
    
    #sort the names into alphabetical order
    names = list(names)
    names.sort()
    
    #write the list to a json file
    with open(names_file_target, 'w') as file:
        json.dump(names, file)
        

def make_individual_name_files(min_year = minYear, max_year = maxYear, 
                            directory_state = directoryState, 
                            directory_year = directoryYear, 
                            names_file = namesFilePath,
                            site_dir = siteFolder):
    """This function creates a directory of json files, one for each name
    listed in the names_file. Each file is a 52 by (max_year+1 - min_year)
    matrix where the (i,j)th entry gives the number of times the name was
    given to a baby in state i in year j (state 0 is all of the US)."""
    
    #make the directory
    for let in letters:
        path = os.path.join(site_dir + "namesData/", let)
        os.mkdir(path)
    
    #load the names
    with open(names_file, 'r') as file:
        names = json.load(file)
    
    #initialize the big dictionary with key value pairs of Name: Matrix
    bigD = {}
    for name in names:
        bigD[name] = [[0 for s in range(52)] for y in range(min_year, 
                                                            max_year + 1)]
    
    #open the state files and add their data to the matrices
    for i in range(1, 52):
        path = os.path.join(directory_state, states[i] + ".TXT")
        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            list_of_rows = list(csv_reader)
            for row in list_of_rows:
                if int(row[2]) >= min_year:
                    bigD[row[3]][int(row[2]) - min_year][i] += int(row[4])
    
    #open the year files and add their data to the matrices
    for y in range(min_year, max_year + 1):
        path = os.path.join(directory_year, "yob" + str(y) + ".txt")
        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            list_of_rows = list(csv_reader)
            for row in list_of_rows:
                bigD[row[0]][y - min_year][0] += int(row[2])
                
    #produce the individual json files for each distinct name         
    for name in bigD.keys():
        path = os.path.join(site_dir + 'namesData/' + name[0:1] + '/', 
                            name + '.json')
        with open(path, 'w') as file:
            json.dump(bigD[name], file)

    
def most_popular_data(min_year = minYear, max_year = maxYear,
                      directory_state = directoryState,
                      directory_year = directoryYear,
                      site_dir = siteFolder):
    """This function outputs two json files for use with the popular baby
    names interactive map. The first is a dictionary containing the
    top ten most popular names by year of the form
    {SEX: {YEAR: [[NAME, COUNT]]}} where SEX is F, M, or B. The second file
    is a dictionary containing the most popular five names for each sex,
    state, and year. This dictionary is of the form
    {SEX: {YEAR: {STATE: [[NAME, COUNT]]}}}. The resulting json files are 
    written to site_dir."""
    
    #initialize the big dictionary for national top ten lists
    most_pop_national = {'F': {}, 'M': {}, 'B': {}}
    
    #open year files to add their data to the big dictionary
    for Y in range(min_year, max_year + 1):
        file = "yob" + str(Y) + ".txt"
        path = os.path.join(directory_year, file)
        with open(path, 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            list_of_rows = list(csv_reader)
            
        #add the female data which is listed at the beginning of these files
        most_pop_national['F'][Y] = [[list_of_rows[i][0], list_of_rows[i][2]] 
                                   for i in range(10)]
        for row in list_of_rows[10:]:
            if row[2] == most_pop_national['F'][Y][-1][1]:
                most_pop_national['F'][Y].append([row[0], row[2]])
            else:
                break
        
        #add the male data which begins after the female data
        i=0
        most_pop_national['M'][Y] = []
        for row in list_of_rows:
            if ((i < 10) 
                and (row[1] == 'M')) \
                or ((i >= 10) 
                    and (row[2] == most_pop_national['M'][Y][-1][1])):
                most_pop_national['M'][Y].append([row[0], row[2]])
                i+=1
            elif i >= 10:
                break
            
        #use the gathered male and female data to create the ranking for both
        CombinedList = most_pop_national['F'][Y] + most_pop_national['M'][Y]
        CombinedList.sort(key = lambda x: x[1], reverse = True)
        most_pop_national['B'][Y] = CombinedList[0:10]
        for pair in CombinedList[10:]:
            if pair[1] == CombinedList[9][1]:
                most_pop_national['B'][Y].append(pair)
            else:
                break
    
    #initialize the big dictionary for their top five lists
    most_pop_states = {'F': {}, 'M': {}, 'B': {}}
    for Y in range(min_year, max_year+1):
        most_pop_states['F'][Y] = {}
        most_pop_states['M'][Y] = {}
        most_pop_states['B'][Y] = {}
    
    #add state data
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
            elif (int(row[2]) >= min_year) and (i == 5) and \
                (row[4] == most_pop_states[row[1]][year][state][-1][1]):
                most_pop_states[row[1]][year][state].append([row[3], row[4]])
        for year in range(min_year, max_year+1):
            CombinedList = most_pop_states['F'][year][state] \
                + most_pop_states['M'][year][state]
            CombinedList.sort(key = lambda x: x[1], reverse = True)
            most_pop_states['B'][year][state] = CombinedList[0:5]
            for pair in CombinedList[5:]:
                if pair[1] == CombinedList[4][1]:
                    most_pop_states['B'][year][state].append(pair)
                else:
                    break
                
    #write the big dictionaries to json files
    with open(site_dir + 'mostPopStates.json', 'w') as file:
        json.dump(most_pop_states, file)
    with open(site_dir + 'mostPopNat.json', 'w') as file:
        json.dump(most_pop_national, file)
                

def make_names_graph(sex = 'B', min_year = minYear, max_year = maxYear,
                     site_dir = siteFolder):
    """"Returns a graph with vertex set = names that were the most popular in
    some state, but not in the US in a at least one year, i.e. names that
    receive a shade of gray on the map in at least one year, and has
    edge set of pairs of names that do this in the same year at least
    once, i.e. pairs of names that need two different shades of gray.
    
    Also returns a list of the names that appear in the graph ordered, 
    descending, by the number of years each name appears on the map 
    in this way."""
    
    #initialize the graph and the name weights
    names_graph = nx.Graph()
    weights={}
    
    #open the files with the most popular names data
    with open(site_dir + 'mostPopStates.json') as file:
        MPS = json.load(file)
    with open(site_dir + 'mostPopNat.json') as file:
        MPN = json.load(file)
        
    #take out data for relevant sex
    state_dict = MPS[sex]
    nat_dict = {str(Y): MPN[sex][str(Y)][0][0] 
               for Y in range(min_year, max_year + 1)}
    
    #for each year make a set of distinct names that won a state
    for year in range(min_year, max_year + 1):
        Temp = {state_dict[str(year)][states[i]][0][0] for i in range(1, 52)}
        for i in range(1, 52):
            win_num = state_dict[str(year)][states[i]][0][1]
            winners = [state_dict[str(year)][states[i]][0][0]]
            for j in range(1, 5):
                if state_dict[str(year)][states[i]][j][1] == win_num:
                    Temp.add(state_dict[str(year)][states[i]][j][0])
                    winners.append(state_dict[str(year)][states[i]][j][0])
            for winner in winners:
                if winner != nat_dict[str(year)]:
                    if winner in weights.keys():
                        weights[winner] += 1
                    else:
                        weights[winner] = 1
                    
        #remove the national winner from the set
        best = nat_dict[str(year)]
        Temp.add(best)
        Temp.remove(best)
        
        #add the complete graph on this set to the names graph overall
        T = nx.complete_graph(list(Temp))
        names_graph.add_edges_from(list(T.edges))
        
        #make the list of names ordered by the number of times they appear 
        #as gray for a year, descending.
        list_of_weights = [(name, weights[name]) for name in weights.keys()]
        list_of_weights.sort(key=lambda x: x[1], reverse = True)
        ordered_list = [name for name,_ in list_of_weights]
        
    #return the names graph and the corresponding list of names
    return names_graph, ordered_list


def greedy_coloring(sex = 'B', min_year = minYear, max_year = maxYear,
                    site_dir = siteFolder):
    """Makes a greedy coloring of the names graph where the names are colored
    in order of the number of times they appear in gray on the map"""
    
    #get the graphs and order the vertices
    G, order = make_names_graph(sex, min_year, max_year, site_dir = site_dir)
    
    #greedily color the vertices properly in order of importance
    coloring = {x:-1 for x in order}
    for x in order:
        i=0
        nbh_colors = {coloring[y] for y in list(G.adj[x])}
        while i in nbh_colors:
            i += 1
        coloring[x] = i
        
    #return the coloring
    return coloring


def make_grayConnection_file(min_year = minYear, max_year = maxYear,
                             site_dir = siteFolder):
    """Produces a json file at site_dir of the form
    {SEX: {NAME: INTEGER}} which gives a proper coloring of the vertices of
    the graph of names that need to appear in gray at some point on the map
    (as the vertices) and names that appear on the map in some year together
    both in gray (as the edges) - a different coloring for each sex."""
    
    gray_connection = {sex: greedy_coloring(sex, min_year, max_year,
                                            site_dir = site_dir) 
                       for sex in ['F', 'M', 'B']}
    
    with open(site_dir + 'grayConnection.json', 'w') as file:
        json.dump(gray_connection, file)

make_list_of_all_names()
most_popular_data()
make_grayConnection_file()
make_individual_name_files()