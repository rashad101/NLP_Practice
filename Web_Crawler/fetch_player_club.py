"""
@author: rony
"""

import csv
import sys
import requests
from bs4 import BeautifulSoup


def fetch_player_table(wiki_link, team_name):
    url = requests.get(wiki_link)
    page_content = BeautifulSoup(url.content, 'html.parser')

    tables = page_content.find_all('table')

    found = 0
    rows = []
    for table in tables:
        if found<1:
            if table.find_all("tbody"):
                tbody = table.find_all("tbody")[0]

                if tbody.find_all("tr"):
                    tr = tbody.find_all("tr")[0]

                    if tr.find_all("td"):

                        all_td= tr.find_all("td")
                        for td1 in all_td:
                            if td1.find_all("table"):
                                tb = td1.find_all("table")[0]
                                if tb.find_all("tbody"):
                                    tbd = tb.find_all("tbody")[0]
                                    if tbd.find_all("tr"):
                                        tbr = tbd.find_all("tr")
                                        if(len(tbr)>0):
                                            tr_count=0
                                            for trr in tbr:
                                                if tr_count==0:
                                                    found+=1
                                                    found=True
                                                    rows.append(['No.','Position','Player'])
                                                else:
                                                    tdd = trr.find_all("td")
                                                    num = tdd[0].get_text().replace("\n","").strip()
                                                    pos = tdd[2].get_text().replace("\n","").strip()
                                                    pal = tdd[3].get_text().replace("\n","").strip()
                                                    rows.append([num,pos,pal])
                                                tr_count+=1
    for i in range(len(rows)):
        if i>1 and rows[i][0]=='No.':
            del(rows[i])
            break

    data = open((team_name + "_fullteam.csv"), 'w')
    data_writer = csv.writer(data)
    data_writer.writerows(rows)
    # print(rows)
    data.close()



if __name__ == "__main__":


    url = "https://en.wikipedia.org/wiki/FC_Porto"
    team_name = url[url.rfind("/") + 1:]

    fetch_player_table(url, team_name)
    #fetch_side_column(url, team_name)
