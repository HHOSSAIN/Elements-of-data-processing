# Part B Task 2
import re
import os
import sys
import argparse #me

''' structuring file '''
def structure(pattern1, pattern2, content,revised_content):
    if re.search(pattern1, content) :
        revised_content = re.sub(pattern1, r'' , content)
    if re.search(pattern2, content) :
        revised_content = re.sub(pattern2, r' ' , revised_content)
    return revised_content

pattern1 = r'[^a-z^\s]' #remove except this
pattern2 = r'[\s]{1,}' #whitespace char repeating together 1 or more times

parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to write", type=str) 
args=parser.parse_args()

#assuming that we can also look for files in the current directory
directory = os.getcwd() + '/' + args.file 

file =open(directory, mode='r')
content = file.read()
content = content.lower()
            
revised_content=''
revised_content= structure(pattern1, pattern2, content,revised_content)

''' IF WE ASSUME THAT WE WILL ONLY READ FILES THAT WILL BE INSIDE THE "cricket" FOLDER, THEN 
    USE THE CODE COMMENTED IN THIS DOCSTRING

directory = os.getcwd() + '/cricket'
pattern3 = r'(.*)' #lagbe na
pattern4 = r'(\d{3}\.txt)'
#for char in args.file:
f = re.findall(pattern4, args.file)[0] #asssuming files stored in 'cricket' folder always

for entry in os.scandir(directory):
    if (entry.path.endswith(".txt") and entry.is_file()):
        #process the filename first
        name = os.path.basename(entry.path) #name of txt file which we are gonna through
        if name==f:
            file =open(entry.path, mode='r')
            content = file.read()
            content = content.lower()
            
            revised_content=''
            if re.search(pattern1, content) :
                revised_content = re.sub(pattern1, r' ' , content)
            
            if re.search(pattern2, content) :
                revised_content = re.sub(pattern2, r' ' , revised_content)
            break
        continue    '''

print(revised_content)



