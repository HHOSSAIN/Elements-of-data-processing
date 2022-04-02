import pandas as pd
import argparse

data = pd.read_csv('owid-covid-data.csv',encoding = 'ISO-8859-1')

data['date'] = pd.to_datetime(data['date'])
data_filter= data[data['date'].dt.year == 2020]
data_filter['date'] = data_filter['date'].dt.month

data2= data_filter.loc[: ,['date', 'location', 'total_cases','new_cases', 'total_deaths', 'new_deaths']]

data2= data2.dropna()
grouped = data2.groupby(['date','location'])

final1 = grouped.agg({'total_cases': 'last', 'new_cases': 'sum', 'total_deaths': 'last', 'new_deaths': 'sum'}).reset_index()

final2= final1[['location', 'date', 'total_cases','new_cases', 'total_deaths', 'new_deaths']]
final2.rename(columns = {'date':'month'}, inplace = True)

#START OF PART A, TASK 1, SECOND PART
new_col= final2["new_deaths"].div(final2["new_cases"])
final2.insert(loc=2, column="case_fatality_rate", value=new_col)
final2= final2.sort_values(['location', 'month'], ascending=[True, True])

# Printing the first 5 rows of the final dataframe as per question
print(final2.head())

parser = argparse.ArgumentParser()
'''https://docs.python.org/3/howto/argparse.html'''
parser.add_argument("file", help="file to write", type=str) 
args=parser.parse_args() #parser looks for a string after d filename
final2.to_csv(args.file)