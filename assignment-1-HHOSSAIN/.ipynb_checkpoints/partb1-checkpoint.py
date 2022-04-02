## Part B Task 1

import re
import pandas as pd
import os 
import argparse 

''' In the pdf, it was not specified that the letters in documentID must be uppercase letters. Therefore,
    I am allowing lowercase letters in the pattern as well '''
pattern = r'[a-zA-Z]{4}-\d{3}[a-zA-Z]?'

#directory= r'/home/jovyan/storage/assignment-1-HHOSSAIN'
directory = os.getcwd() + '/cricket'

names=[]  # list of all the txt files
codes=[]  # list of unique code from each file

for entry in os.scandir(directory):
    if (entry.path.endswith(".txt") and entry.is_file()):
        name = os.path.basename(entry.path) #name of txt file which we are gonna through
        names.append(name)
        file =open(entry.path, mode='r')
        content = file.read()
        if re.search(pattern, content) :
            code = re.findall(pattern, content)[0]
            codes.append(code)

d = {'filename':names,'documentID':codes}
#retained the indexing beside the filenames as it's easier to go through the file and read it
df = pd.DataFrame(d) 

parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to write", type=str) 
args=parser.parse_args()
df.to_csv(args.file)