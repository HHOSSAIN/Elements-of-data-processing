import pandas as pd
import argparse
import matplotlib.pyplot as plt

#imports by Hasne
import sys 
import os 

f_names = []
for f in sys.argv[1:]:
    f_names.append(f)

''' Here, I am assuming that parta1.py will be run before testing parta2.py and therefore, we 
    we will have this 'owid-covid-data-2020-monthly.csv' file in our hand '''
data = pd.read_csv('owid-covid-data-2020-monthly.csv',encoding = 'ISO-8859-1')

grouped = data.groupby('location')
final1 = grouped.agg({'total_cases': 'last', 'new_cases': 'sum', 'total_deaths': 'last', 'new_deaths': 'sum'}).reset_index()
new_col= final1["new_deaths"].div(final1["new_cases"])
final1.insert(loc=2, column="case_fatality_rate", value=new_col)
print(final1)

#FIRST PLOT
plt.scatter(final1.iloc[:,3],final1.iloc[:,2])  #,color='green')
#plt.show()
plt.ylabel("case_fatality_rate")
plt.xlabel("confirmed_new_cases")
plt.savefig(f_names[0])

#SECOND PLOT WITH log SCALE
plt.scatter(final1.iloc[:,3],final1.iloc[:,2]) 
plt.ylabel("case_fatality_rate")
plt.xlabel("confirmed_new_cases")
plt.xscale("log")
plt.savefig(f_names[1])