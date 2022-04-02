## Part B Task 3
import re
import sys
import pandas as pd
import nltk
import os

import argparse #me

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

revised_content=''

directory = os.getcwd() + '/cricket'

parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to write", type=str) 

id_pattern = r'[a-zA-Z]{4}-\d{3}[a-zA-Z]?'

codes=[]
final_codes=[]
f_names=[] #store file names for future reference

#listing down the arguments
keywords=[]

for keyword in sys.argv[1:]:
    keywords.append(keyword)

#print(keywords) #for testing
    
target = len(keywords)

for entry in os.scandir(directory):
    values = file_read(entry)
    name=values[0]
    content=values[1]
   
    if(content == False):
        continue
        
    if re.search(id_pattern, content) :
        code = re.findall(id_pattern, content)[0]
        codes.append(code)
        
    content = content.lower()
    
    '''structuring the file content '''
    revised_content= structure(pattern1, pattern2, content)
            
    items = revised_content.split()
    count=0
    for i in range(target):
        if(keywords[i] in items):
            count += 1
            
    if(count == target):
        final_codes.append(code)
        f_names.append(name)

print("Document IDS = ", final_codes)