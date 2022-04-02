## Part B Task 5
import re
import os
import sys
import pandas as pd
import nltk

# additional imports by me
from nltk.stem.porter import * 
import argparse 
from sklearn.feature_extraction.text import TfidfTransformer
import math

from numpy import dot

from numpy.linalg import norm
def cosine_sim(v1, v2):
    return round((dot(v1, v2)/(norm(v1) * norm(v2))), 4)

def structure(pattern1, pattern2, content):
    if re.search(pattern1, content) :
        revised_content = re.sub(pattern1, r'' , content)
    if re.search(pattern2, content) :
        revised_content = re.sub(pattern2, r' ' , revised_content)
    return revised_content

def file_read(entry):
    import sys
    import os
    if (entry.path.endswith(".txt") and entry.is_file()):
        #process the filename first
        name = os.path.basename(entry.path) #name of txt file which we are gonna through
        
        file =open(entry.path, mode='r')
        content = file.read()
        
        return name, content #returns a tuple
    else:
        return False, False
    
pattern1 = r'[^a-z^\s]' #remove except this
pattern2 = r'[\s]{1,}' #whitespace char repeating together 2 or more times
id_pattern = r'[a-zA-Z]{4}-\d{3}[a-zA-Z]?'

revised_content=''

''' Assuming we will be searching the files in cricket folder '''
directory = os.getcwd() + '/cricket'

parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to write", type=str) 
    
keywords =[]
for keyword in sys.argv[1:]:
    keywords.append(keyword)
    
#print(keywords) #python partb3.py cricket/missing lee ponting (for testing)

codes=[] #all doc codes
final_codes=[]
f_names=[]
two_d_list=[]
dict_list=[]
combined_dict={}
stemmed_keywords = []

for entry in os.scandir(directory):
    values = file_read(entry)
    name=values[0] #filename
    content=values[1] #the whole text in d file
    if(content == False):
        continue
        
    if re.search(id_pattern, content) :
        code = re.findall(id_pattern, content)[0]
        codes.append(code)
        
    content = content.lower()
        
    revised_content= structure(pattern1, pattern2, content)
    
    # tokenize and stem the keywords
    # tokenize and stem the file content
    wordList = nltk.word_tokenize(revised_content)
    #we also have keywords list
    
    '''making list of stemmed words from keywords list '''
    porterStemmer = PorterStemmer()
    #stemmed_keywords = []
    for word in keywords:
        stemWord = porterStemmer.stem(word)
        stemmed_keywords.append(stemWord)
        
    target = len(stemmed_keywords)
    
    '''making dict of stemmed words 4m the file '''
    stem_list=[]
    wordDict = {} #frequency counter of each stem word
    for word in wordList:
        ''' https://www.geeksforgeeks.org/python-stemming-words-with-nltk/ '''
        stemWord = porterStemmer.stem(word)
        
        stem_list.append(stemWord)
        
        if stemWord in wordDict : 
            wordDict[stemWord] = wordDict[stemWord] +1
        else :
            wordDict[stemWord] = 1
            
    count = 0        
    for i in range(target):
        if(stemmed_keywords[i] in wordDict):
            count += 1
            
    if(count == target):
        final_codes.append(code) #CODES OF THE FILENAMES ORDER
        f_names.append(name) #FILENAMES LIST ORDER
        two_d_list.append(stem_list)
        
        new_dict={}
        #making the corpus and list of dicts
        for word in stem_list:
            if word in new_dict:
                new_dict[word] += 1
            else:
                new_dict[word] = 1
                
            if word in combined_dict:
                continue
            else:
                combined_dict[word] = 1
        dict_list.append(new_dict) #DICTS OF THE FILENAME ORDER

words=list(combined_dict.keys())
#print(words) --->for testing

#Need to make 2d list of counts
term_counts=[]
for d in dict_list:
    counts=[]
    for w in words:
        if w in d:
            counts.append(d[w])
        else:
            counts.append(0)
    term_counts.append(counts)
    
#print(term_counts) --->for testing

from sklearn.feature_extraction.text import TfidfTransformer

transformer = TfidfTransformer()
tfidf= transformer.fit_transform(term_counts)
doc_tfidf = tfidf.toarray()
#print(tfidf.toarray()) --->for testing

#math
query_vector=[]
keywords_dict={}
for kw in stemmed_keywords:
    if kw in keywords_dict:
        keywords_dict[kw] += 1
    else:
        keywords_dict[kw] = 1
        
#print(keywords_dict) --> for testing

for w in words:
    if w in keywords_dict:
        query_vector.append(keywords_dict[w])
    else:
        query_vector.append(0)
q_unit = [x/math.sqrt(len(stemmed_keywords)) for x in query_vector]
#print(q_unit)

sims= [ cosine_sim(q_unit, doc_tfidf[d_id]) for d_id in range(doc_tfidf.shape[0]) ] #d_id-->doc num
#print(sims)

df = pd.DataFrame({'documentID':final_codes, 'score':sims})
df = df.sort_values(by='score' , ascending=False)
print(df)