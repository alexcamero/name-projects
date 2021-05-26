
import matplotlib.pyplot as plt
import os, json, csv, requests
import numpy as np
from bs4 import BeautifulSoup as bs
from sklearn.cluster import KMeans

def scrape_totals(
        write_to_directory = '../json files/',
        url = "https://www.ssa.gov/OACT/babynames/numberUSbirths.html", 
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; '
                   + 'Intel Mac OS X 10_15_7)'
                   + 'AppleWebKit/537.36 (KHTML, like Gecko) '
                   + 'Chrome/88.0.4324.150 Safari/537.36'}):

    #initialize the list
    data = []
    
    # Retrieve the webpage
    response = requests.get(url, headers = headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        
        #start parsing the response text
        soup = bs(response.text, 'html.parser')
        
        # Each row of data is in a <tr> tag
        data_rows = soup.find_all('tr')
        data_rows.pop(0)
        
        for row in data_rows:
            # Extract data from <tr> tag
            cell_list = row.find_all('td')
            
            year = int(cell_list[0].get_text())
            male = int(cell_list[1].get_text().replace(',',''))
            female = int(cell_list[2].get_text().replace(',',''))
            total = int(cell_list[3].get_text().replace(',',''))
            
            # Append to data list
            data.append([year, total, female, male])
            
        # Sort data by year and write to file
        data.sort(key=lambda x: x[0])
        
        with open(write_to_directory + 'totals.json', 'w') as file:
            json.dump(data,file)
        return data
    else:
        print(f"There was an issue: Status Code {response.status_code}")
        raise NameError("AN HTML SITUATION")
    

class NameData:
    
    def __init__(self, min_year = 1937, max_year = 2020,
                 directory_year = '../../Name Data/namesbyyear/',
                 helper_files_directory = '../json files/'):
        
        
        self.min_year = min_year
        self.max_year = max_year
        self.files = helper_files_directory
        self.file_ending = '_' + str(min_year) + '_' + str(max_year) + '.json'
        
        
        
        #make list of relevant years and zero array of correct length
        self.years = range(self.min_year, self.max_year + 1)
        self.num_years = len(self.years)
        self.zero = np.array([0 for _ in self.years])
        
        self.distance_from = {"SoS":{"raw":{}, "prop":{}, "raw normed":{},
                              "prop normed":{}}}
        
        
        
        #open/make file of distinct names
        #format is [Name]
        try:
            with open(self.files + 'distinct_names' 
                      + self.file_ending, 'r') as file:
                self.distinct_names = json.load(file)
            
        except FileNotFoundError:
            print("Distinct name file not found. Making one.....")
            self.distinct_names = set()
                            
            for Y in self.years:
                path = os.path.join(directory_year, "yob" + str(Y) + ".txt")
                with open(path, 'r') as file:
                    csv_reader = csv.reader(file)
                    list_of_rows = list(csv_reader)
                    for row in list_of_rows:
                        self.distinct_names.add(row[0])
        
            self.distinct_names = list(self.distinct_names)
            self.distinct_names.sort()
            
            with open(self.files + 'distinct_names'
                      + self.file_ending, 'w') as file:
                json.dump(self.distinct_names,file)
                
        self.num_names = len(self.distinct_names)
        self.name_index = {self.distinct_names[i]:i 
                           for i in range(self.num_names)}
        print("List of distinct names ready.")
        
        
        
        
        #open/make the file of total births by year
        #format is [[year, total, female, male]]
        try:
            with open(self.files + 'totals.json', 'r') as file:
                total_data = json.load(file)
            
        except FileNotFoundError:
            print("File with total births data not found. Making one.....")
            total_data = scrape_totals(write_to_directory 
                                       = self.files)
        temp = {row[0]: {'B': row[1], 'F': row[2], 'M': row[3]} 
                for row in total_data}
                
        self.totals = np.array([temp[year]['B'] for year in self.years])
        self.totals_female = np.array([temp[year]['F'] for year in self.years])
        self.totals_male = np.array([temp[year]['M'] for year in self.years])
        print("Total births data ready.")
            
            
            
            
        #open/make the raw time series data for the names
        #format is {Name: [Int]}
        try:
            with open(self.files + 'time_series_national'
                      + self.file_ending, 'r') as file:
                tseries = json.load(file)
            
        except FileNotFoundError:
            print("Time series data file not found. Making one.....")
            #initialize dictionary for time series data
            tseries = [[0 for _ in range(self.num_years)] 
                                for _ in range(self.num_names)]
            
            for year in self.years:
                
                #open year file
                path = os.path.join(directory_year, "yob" + str(year) + ".txt")
                with open(path, 'r') as file:
                    csv_reader = csv.reader(file)
                    list_of_rows = list(csv_reader)
                
                #update dictionary for each row
                for row in list_of_rows:
                    i = self.name_index[row[0]]
                    tseries[i][year - self.min_year] += int(row[2])
            
            #write time series data to file
            with open(self.files + 'time_series_national'
                      + self.file_ending, 'w') as file:
                json.dump(tseries, file)
        #convert to np.array        
        self.tseries_raw = np.array(tseries)
        print("Time series data ready.")     
                
                
    
        #get the total number of named people by year 
        self.total_named = sum(self.tseries_raw)
        self.others = self.totals - self.total_named
        self.distinct_named = sum(self.tseries_raw > 0)
        self.lower_distinct = self.distinct_named + np.ceil(self.others/4)
        self.upper_distinct = self.distinct_named + self.others


    def get_matrix(self, series_type = "prop normed"):
        if series_type == "prop normed":
            return self.make_normed(self.tseries_raw/self.totals)
        elif series_type == "raw normed":
            return self.make_normed(self.tseries)
        elif series_type == "prop":
            return self.tseries_raw/self.totals
        elif series_type == "raw":
            return self.tseries_raw
        
    def make_normed(self, series):
        return np.transpose(np.transpose(series)/np.amax(series, axis = 1))
    
    def closest_neighbors_SoS(self, name, series_type = "prop normed"):
        matrix = self.get_matrix(series_type)
        
        if name in self.distinct_names:
            Nvector = matrix[self.name_index[name]]
        else:
            Nvector = self.zero
        
        result = np.sum(((matrix - Nvector)**2), axis=1)/self.num_years
        neighbors = [(self.distinct_names[i],result[i]) 
                     for i in range(self.num_names)]
        neighbors.sort(key = lambda x: x[1])
        self.distance_from["SoS"][series_type][name] = neighbors
            
        

    def raw(self, name):
        if name in self.distinct_names:
            return self.tseries_raw[self.name_index[name]]
        elif name == "OTHER NAMES":
            return self.others
        elif name == "ALL NAMED":
            return self.total_named
        else:
            return self.zero
    
    def proportion(self, name):
        return self.raw(name)/self.totals
        
    def raw_normed(self, name):
        series = self.raw(name)
        M = max(series)
        if M == 0:
            M = 1
        return series/M
        
    def prop_normed(self, name):
        series = self.proportion(name)
        M = max(series)
        if M == 0:
            M = 1
        return series/M
    
    def compare_shape(self, name1, name2):
        figure, axes = plt.subplots(nrows=2,ncols=1)
        axes[0].plot(self.years, self.raw(name1))
        axes[1].plot(self.years, self.raw(name2),'r-')
        axes[0].set_title(name1)
        axes[1].set_title(name2)
        figure.tight_layout()
        
    def run_kmeans(self, series_type = "prop normed", 
                   most_clusters = 20, iterations = 10):
        X = self.get_matrix(series_type)
        self.km = {}
        num_clusters = range(2,most_clusters+1)
        for k in num_clusters:
            self.km[k] = KMeans(n_clusters = k, n_init = iterations).fit(X)
        SSE = [self.km[k].inertia_ for k in num_clusters]
                      
        plt.plot(num_clusters, SSE)




        

