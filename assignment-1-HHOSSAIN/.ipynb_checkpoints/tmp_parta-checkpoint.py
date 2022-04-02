import pandas as pd
import argparse

data = pd.read_csv('owid-covid-data.csv',encoding = 'ISO-8859-1')
#print(data.head())

data['date'] = pd.to_datetime(data['date'])
print("testttereeeee")
include = data[data['date'].dt.year == 2020]
print(include) #59831
''''''
#include.to_csv('testA2.csv')


#data['date'] = pd.to_datetime(data['date']).dt.month

'''no of rows=79476 still even though 2021 dated row gulir date blank hoye gese'''
#data['date'] = pd.to_datetime(include['date']).dt.month #previously 2415 rows, now 2073 rows...PROBLEM
#data.to_csv('testA3.csv')
data_filter= data[data['date'].dt.year == 2020]
#data_filter= data_f
data_filter['date'] = data_filter['date'].dt.month
data_filter.to_csv('testA3.csv')




data2= data_filter.loc[: ,['date', 'location', 'total_cases','new_cases', 'total_deaths', 'new_deaths']]
print(data2)

data2= data2.dropna()
grouped = data2.groupby(['date','location'])
print(type(grouped))

'''try to find num of rows in groupby object...prolly (date,location) key er dataframe no of rows
   The simplest way to get row counts per group is by calling .size(), which returns a Series '''
print("group sizes!!!\n",grouped.size())
print(type(grouped.size()))
#print(grouped)
grouped.size().to_csv('test2.csv') #new file create hoye bhitore dhuke

    
#final1=grouped.first().reset_index() #THIS IS WHERE THE PROBLEM IS...IT TOOK 1ST ROW FROM EACH DATAFRAME OF EACH GROUP
#print(final1)
#final1=final1.dropna()
final1= grouped.sum().reset_index()
final1=final1.dropna()
#final1=final1[(final1['new_cases'] > 0) and (final1['total_cases'] > 0)]
'''problem individually konota match na korlei baad diye diche... '''
#final1= final1.loc[(final1['new_cases'] > 0) & (final1['total_cases'] > 0) & (final1['new_deaths'] > 0) & (final1['total_deaths'] > 0), :]

print(final1) #this is d correct ans...1758 rows
final2= final1[['location', 'date', 'total_cases','new_cases', 'total_deaths', 'new_deaths']]
print(final2)


'''for country, df in grouped:
    print(country)
    total_cases= df['total_cases'].value_counts()'''

#for index, row in final1.iterrows():
#    final.at[index, ] = 10


#final1["case_fatality_rate"]= final1["total_deaths"].div(final1["total_cases"])
#do new deaths/new cases later
new_col= final2["total_deaths"].div(final2["total_cases"])
#print(final1)
final2.insert(loc=2, column="case_fatality_rate", value=new_col)
final2.rename(columns = {'date':'month'}, inplace = True)
print(final2)
final2= final2.sort_values(['location', 'month'], ascending=[True, True])
print(final2.head())
#data_filter.to_csv('testA3.csv')

parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to write", type=str) #1st arg is the type we looking for in arguments 4m cli...so when we do
                                                        #args.file(), we get the this file argument
args=parser.parse_args()
final2.to_csv(args.file)
    