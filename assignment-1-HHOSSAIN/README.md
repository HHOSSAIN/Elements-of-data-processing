# COMP20008 2021 Semester 1 Assignment 1
Readme file

Student name: Hasne Hossain
ID: 1102602

The project basically had 2 parts- part A and B. For part 1, we used data from owid-covid-data.csv file to do some data preprocessing to get useful insights from the data. We also visualized some of our results by plotting scatter plots in task 2 of part A. The report from task 3 discusses the visual analysis of the plots.

In part B, we explored "cricket" dataset. We did text preprocessing with the aim of building a simple search engine that will allow a user to specify keywords and find all articles related to those keywords. Topics explored includes regular expressions(regex), TF-IDF, cosine similarity and many more.

Dependencies:

Part A:
1)In parta1.py, we required to import pandas, argparse
2)In parta2.py, we imported pandas, argparse, matplotlib, sys, os. We also assume that parta1.py will be run before testing parta2.py and therefore, we we will have this 'owid-covid-data-2020-monthly.csv' file in our hand

Part B:
1)In partb1.py, we imported re, pandas, argparse, os

2)In partb2.py, we imported re, argparse, sys, os

3)In partb3.py, we imported pandas, re, argparse, sys, nltk, os

4)In partb4.py, we imported re, pandas, argparse, sys, os, nltk

5)In partb5.py, we imported re, pandas, argparse, sys, os, nltk, TfidfTransformer from sklearn.feature_extraction.text, numpy, math
