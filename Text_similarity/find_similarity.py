"""
@author: rony
"""
import csv
import requests
import math
import nltk
from nltk.corpus import stopwords
from nltk.cluster import cosine_distance
from nltk.probability import FreqDist
from bs4 import BeautifulSoup

query=[]
poi_name=[]
wikipedia_link=[]
answer=[]
relavent_paragraphs=[]
stopwords_en = stopwords.words("english")

def read_dataset():
    with open('queries_info.csv') as f:
        file = csv.reader(f)

        count=0
        for row in file:
            if count == 0:
                count+=1
                continue
            query.append(row[0])
            poi_name.append(row[1])
            wikipedia_link.append(row[2])
            answer.append(row[3])

def preprocessing(raw_text):
    wordlist = nltk.word_tokenize(raw_text)
    text = [word.lower() for word in wordlist if word not in stopwords_en]
    return text

def check_similarity(text1, text2):
    #preprocess text
    text1 = preprocessing(text1)
    text2 = preprocessing(text2)

    #TF-IDF calculation
    word_set = set(text1).union(set(text2))

    #calculate
    freqd_text1 = FreqDist(text1)
    text1_tf = dict.fromkeys(word_set,0)
    for w in text1:
        text1_tf[w]  = freqd_text1[w]/len(text1)

    freqd_text2 = FreqDist(text2)
    text2_tf = dict.fromkeys(word_set,0)
    for w in text2:
        text2_tf[w] = freqd_text2[w]/len(text2)

    #calculate IDF

    text12_idf = dict.fromkeys(word_set,0)

    for w in text12_idf.keys():
        if w in text1:
            text12_idf[w]+=1
        if w in text2:
            text12_idf[w]+=1

    for w,val in text12_idf.items():
        text12_idf[w] = 1 + math.log(2/float(val)) # since there are two text


    #calculate TF-IDF = TF*IDF
    text1_tfidf = dict.fromkeys(word_set,0)
    for w in text1:
        text1_tfidf[w] = (text1_tf[w])*(text12_idf[w])

    text2_tfidf = dict.fromkeys(word_set,0)
    for w in text2:
        text2_tfidf[w] = (text2_tf[w])*(text12_idf[w])


    #calculate osine similarity
    v1 = list(text1_tfidf.values())
    v2 = list(text2_tfidf.values())

    similarity = 1-cosine_distance(v1,v2)

    return similarity


def calculate_similarities_on_data():
        rows=[]
        rows.append(["query","poi_name","wikipedia-link","answer","most_relavent_paragraph","similarity"])
        for i in range(len(query)):

            url = requests.get(wikipedia_link[i])
            page_content = BeautifulSoup(url.content, 'html.parser')

            #fetching all the paragraphs
            paragraphs=[]
            for p_tag in page_content.find_all('p'):
                paragraphs.append(p_tag.get_text())

            #take the most relavent paragraph
            question = query[i]
            most_similar_paragraph = ""

            max_prob = 0.0
            for j in range(len(paragraphs)):
                prob = check_similarity(question,paragraphs[j])
                if(prob>max_prob):
                    max_prob=prob
                    most_similar_paragraph = paragraphs[j]
            relavent_paragraphs.append(most_similar_paragraph)

            #print("Question: "+question)
            #print("Paragraph: ("+str(max_prob)+") "+most_similar_paragraph)
            temp=[query[i],poi_name[i],wikipedia_link[i],answer[i],most_similar_paragraph,str(max_prob)]
            rows.append(temp)


        #data = open("updated_queries_info.csv",'w')
        #data_writer = csv.writer(data)
        #data_writer.writerows(rows)
        
        return relavent_paragraphs

def fetch_relavent_paragraphs():
        read_dataset()
        relv_para = calculate_similarities_on_data()
        return relv_para

if __name__== "__main__":
    
    fetch_relavent_paragraphs()
