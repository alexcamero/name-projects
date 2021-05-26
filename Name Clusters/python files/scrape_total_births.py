"""
This scrapes data from the SSA webpage where they list the total number of
applications for SSNs by year of birth. The data is listed in the form 'year 
of birth,' 'number of male applicants,' 'number of female applicants,' and
'total number of applicants.' The data will then be stored as a json file.
It's form will be a 2d array where each row gives
[YEAR, TOTAL, FEMALE, MALE].

This is necessary when taking the proportion for each individual name of a 
given year because the data files themselves do not list names that were
used 4 or fewer times.
"""

from bs4 import BeautifulSoup as bs
import requests
import json

#set the url and headers (you might want different headers, I just copied mine)
url = "https://www.ssa.gov/OACT/babynames/numberUSbirths.html"
headers = {'User-Agent':
           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
          + 'AppleWebKit/537.36 (KHTML, like Gecko) '
          + 'Chrome/88.0.4324.150 Safari/537.36'}
    
#initialize the list
data = []

# Retrieve the webpage
response = requests.get(url,headers = headers)

# Check if the request was successful
if response.status_code == 200:
    
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
    
    with open('totals.json', 'w') as file:
        json.dump(data,file)
        
else:
    
    print(f"There was an issue: Status Code {response.status_code}")
