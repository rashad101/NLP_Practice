"""
@author: rony
"""

import csv
import sys
import requests
from bs4 import BeautifulSoup


def fetch_player_table(wiki_link, team_name):
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
        if found:
            #values from each row
            tbodys = table.find_all('tbody')
            for tbody in tbodys:
                trs = tbody.find_all('tr')
                
                
                for tr in trs:
                    t_count = 0
                    single_row = []
                    for td in tr.find_all('td'):
                        t_count+=1
                        if(t_count==2):
                            text = td.get_text().replace("\n","").strip().replace("\xa0","")
                            single_row.append(text[len(text)-2:])
                        elif(t_count==3):
                            single_row.append(tr.find('th').get_text().replace("\n","").strip())
                            single_row.append(td.get_text().replace("\n","").strip().replace("\xa0",""))
                            t_count+=1
                        else:
                            single_row.append(td.get_text().replace("\n","").strip())
                            
                    rows.append(single_row)
                    #print(single_row)
                    
            break
    del(rows[1])
    no_empty_rows_found = False
    
    while(not no_empty_rows_found):
        no_empty_rows_found = True
        for i in range(len(rows)):
            if(rows[i][0]==""):
                del(rows[i])
                no_empty_rows_found=False
                break
    
    data = open((team_name+"_fullteam.csv"),'w')
    data_writer = csv.writer(data)
    data_writer.writerows(rows)
    #print(rows)
    data.close()
    


def fetch_side_column(wiki_link,team_name):
    url = requests.get(wiki_link)
    page_content = BeautifulSoup(url.content,'html.parser')
    
    tables = page_content.find_all('table',{'class':'infobox'})
    table = tables[0]
    trs = table.find('tbody').find_all('tr')
    current_found = False
    highest_found = False
    lowest_found = False
    curr = ""
    high = ""
    low = ""
    rows = []
    header=['Current_ranking','Highest_ranking','Lowest_ranking']
    infos = []
    
    pre_1 = ""
    pre_1_info = ""
    pre_2 = ""
    pre_2_info = ""
    
    pre_count=0
    for tr in trs:
        if(current_found and highest_found and lowest_found):
            
            if tr.find("th"):
                if pre_count==0:
                    pre_1 = tr.find("th").get_text().replace("\n","").strip()
                    if tr.find("td"):
                        pre_1_info = tr.find("td").get_text().replace("\n","").strip()
                elif pre_count==1:
                    pre_2 = tr.find("th").get_text().replace("\n","").strip()
                    if tr.find("td"):
                        pre_2_info = tr.find("td").get_text().replace("\n","").strip()
                else:
                    text = tr.find("th").get_text().replace("\n","").strip()
                    if text == "Best result":
                        current_info = tr.find("td").get_text().replace("\n","").strip()
                        header.append(pre_1)
                        infos.append("Appearances: "+pre_2_info+"\nBest result: "+current_info)
                        
                        pre_1 = pre_2
                        pre_1_info = pre_2_info
                        pre_2  = text
                        pre_2_info = current_info
                        
                    else:
                        pre_1 = pre_2
                        pre_1_info = pre_2_info
                        pre_2 = tr.find("th").get_text().replace("\n","").strip()
                        if tr.find("td"):
                            pre_2_info = tr.find("td").get_text().replace("\n","").strip()
                        
                pre_count+=1
            
        words = tr.get_text().replace("\n","").strip().split(" ")
        if 'Current' in words[0]:
            current_found=True
            
            if "[" in words[0]:
                curr = words[0][len('Current'):words[0].find("[")]
                infos.append(curr)
            else:
                curr = words[0][len('Current'):]
                infos.append(curr)
            
        if 'Highest' in words[0]:
            highest_found=True
            if "[" in words[0]:
                high = words[0][len('Highest'):words[0].find("[")]
                infos.append(high)
            else:
                high = words[0][len('Highest'):]
                infos.append(high)
        if 'Lowest' in words[0]:
            lowest_found=True
            if "[" in words[0]:
                low = words[0][len('Lowest'):words[0].find("[")]
                infos.append(low)
            else:
                low = words[0][len('Lowest'):]
                infos.append(low)

    rows.append(header)
    #deleting ELO rankings
    del(infos[3])
    del(infos[3])
    del(infos[3])
    rows.append(infos)
    data = open((team_name+"_ranking.csv"),'w')
    data_writer = csv.writer(data)
    data_writer.writerows(rows)
    data.close()    
            
    
if __name__=="__main__":
    
    if(sys.argv):
        
        url = sys.argv[1:][0]
        team_name = url[url.rfind("/")+1:]
        
        fetch_player_table(url,team_name)
        fetch_side_column(url,team_name)
        
        


