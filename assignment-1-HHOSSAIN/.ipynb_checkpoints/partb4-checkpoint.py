## Part B Task 4
import re
import pandas as pd
import os
import sys
import nltk

from nltk.stem.porter import * #me
import argparse #me
# first time:
#nltk.download('punkt')
#nltk.download('stopwords')

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

#print(keywords) #python partb3.py cricket/missing lee ponting -->for testing

codes=[] #all doc codes
final_codes=[]
f_names=[]

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
    
    '''making list of stemmed words from keywords list '''
    porterStemmer = PorterStemmer()
    stemmed_keywords = []
    for word in keywords:
        stemWord = porterStemmer.stem(word)
        stemmed_keywords.append(stemWord)
        
    target = len(stemmed_keywords)
    
    '''making dict of stemmed words from the file '''
    wordDict = {} #frequency counter of each stem word
    for word in wordList:
        stemWord = porterStemmer.stem(word)
        if stemWord in wordDict : 
            wordDict[stemWord] = wordDict[stemWord] +1
        else :
            wordDict[stemWord] = 1
            
    count = 0        
    for i in range(target):
        if(stemmed_keywords[i] in wordDict):
            count += 1
    if(count == target):
        final_codes.append(code)
        f_names.append(name)

print(final_codes)
#print(f_names)   