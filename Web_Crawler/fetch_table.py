"""
Created on Fri Sep  7 14:59:17 2018

@author: rony
"""

import csv
import requests
from bs4 import BeautifulSoup


def fetch_table(wiki_link):
    url = requests.get(wiki_link)
    page_content = BeautifulSoup(url.content,'html.parser')
    
    tables = page_content.find_all('table')
    
    found = False
    rows=[]
    for table in tables:
        if not found:
            ths = table.find_all('th')
            header=[]
            count = 0
            #find the headers for the target table
            for th in ths:
                if(th.find('abbr')) and count<2:
                    if(th.find('abbr').attrs['title']=='number'):
                        found = True
                        count+=1
                        header.append(th.find('abbr').get_text())
                        continue
                    
                if found and count>=1 and count<7:
                        count+=1
                        header.append(th.get_text().strip())
                        
            #print(header)
            if found:
                rows.append(header)
                print("nothing")
        if found:
            #the the values from each row
            tbodys = table.find_all('tbody')
            for tbody in tbodys:
                trs = tbody.find_all('tr')
                
                for tr in trs:
                    single_row = []
                    for td in tr.find_all('td'):
                        single_row.append(td.get_text().replace("\n","").strip().replace("\xa0",""))
                    rows.append(single_row)
                    
            break
    del(rows[1])
    print(rows)
    
    


fetch_table("https://en.wikipedia.org/wiki/Germany_national_football_team")