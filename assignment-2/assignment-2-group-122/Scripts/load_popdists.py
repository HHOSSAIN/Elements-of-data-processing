##
## load_popdists.py
## COMP20008 Assignment 2
##
## Created by Group 122
## Copyright © 2021. All rights reserved.
##

import pandas as pd
pd.options.mode.chained_assignment = None  # default = 'warn'
import numpy as np
import os
import argparse

# Retrieve filepath of scripts
master_dir = os.path.dirname(os.path.dirname(__file__))
rel_path = "Data/"
data_dir = os.path.join(master_dir, rel_path)

# Initialise useful variables
drop_cols = [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

# Read in the xls 2012
raw_df = pd.read_excel(os.path.join(data_dir,'lga_2011_2012.xls'),sheet_name = 'Table 6')
df_2012 = raw_df.loc[(raw_df['Unnamed: 1'] == 'Victoria') & (raw_df['Unnamed: 3'] != 'Unincorporated Vic')]
df_2012.columns = ["S/T_code","S/T_name","LGA_code","LGA_name","0-4","5-9","10-14","15-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80-84","85+","Total_population"]
df_2012['0-19'] = df_2012.iloc[:, 4:8].sum(axis = 1)
df_2012['20-64'] = df_2012.iloc[:, 8:17].sum(axis = 1)
df_2012['65+'] = df_2012.iloc[:, 17:22].sum(axis = 1)
df_2012['Year'] = "2012"
df_2012 = df_2012.drop(df_2012.columns[drop_cols],axis = 1)

# Read in the xls 2013
raw_df = pd.read_excel(os.path.join(data_dir,'lga_2013.xls'),sheet_name = 'Table 3')
df_2013 = raw_df.loc[(raw_df['Unnamed: 1'] == 'Victoria') & (raw_df['Unnamed: 3'] != 'Unincorporated Vic')]
df_2013.columns = ["S/T_code","S/T_name","LGA_code","LGA_name","0-4","5-9","10-14","15-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80-84","85+","Total_population"]
df_2013['0-19'] = df_2013.iloc[:, 4:8].sum(axis = 1)
df_2013['20-64'] = df_2013.iloc[:, 8:17].sum(axis = 1)
df_2013['65+'] = df_2013.iloc[:, 17:22].sum(axis = 1)
df_2013['Year'] = "2013"
df_2013 = df_2013.drop(df_2013.columns[drop_cols],axis = 1)

# Read in the xls 2014
raw_df = pd.read_excel(os.path.join(data_dir,'lga_2014.xls'),sheet_name = 'Table 3')
df_2014 = raw_df.loc[(raw_df['Unnamed: 1'] == 'Victoria') & (raw_df['Unnamed: 3'] != 'Unincorporated Vic')]
df_2014.columns = ["S/T_code","S/T_name","LGA_code","LGA_name","0-4","5-9","10-14","15-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80-84","85+","Total_population"]
df_2014['0-19'] = df_2014.iloc[:, 4:8].sum(axis = 1)
df_2014['20-64'] = df_2014.iloc[:, 8:17].sum(axis = 1)
df_2014['65+'] = df_2014.iloc[:, 17:22].sum(axis = 1)
df_2014['Year'] = "2014"
df_2014 = df_2014.drop(df_2014.columns[drop_cols],axis = 1)

# Read in the xls 2015
raw_df = pd.read_excel(os.path.join(data_dir,'lga_2015.xls'),sheet_name = 'Table 3')
df_2015 = raw_df.loc[(raw_df['Unnamed: 1'] == 'Victoria') & (raw_df['Unnamed: 3'] != 'Unincorporated Vic')]
df_2015.columns = ["S/T_code","S/T_name","LGA_code","LGA_name","0-4","5-9","10-14","15-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80-84","85+","Total_population"]
df_2015['0-19'] = df_2015.iloc[:, 4:8].sum(axis = 1)
df_2015['20-64'] = df_2015.iloc[:, 8:17].sum(axis = 1)
df_2015['65+'] = df_2015.iloc[:, 17:22].sum(axis = 1)
df_2015['Year'] = "2015"
df_2015 = df_2015.drop(df_2015.columns[drop_cols],axis = 1)

# Read in the xls 2016
raw_df = pd.read_excel(os.path.join(data_dir,'lga_2016.xls'),sheet_name = 'Table 3')
df_2016 = raw_df.loc[(raw_df['Unnamed: 1'] == 'Victoria') & (raw_df['Unnamed: 3'] != 'Unincorporated Vic')]
df_2016.columns = ["S/T_code","S/T_name","LGA_code","LGA_name","0-4","5-9","10-14","15-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80-84","85+","Total_population"]
df_2016['0-19'] = df_2016.iloc[:, 4:8].sum(axis = 1)
df_2016['20-64'] = df_2016.iloc[:, 8:17].sum(axis = 1)
df_2016['65+'] = df_2016.iloc[:, 17:22].sum(axis = 1)
df_2016['Year'] = "2016"
df_2016 = df_2016.drop(df_2016.columns[drop_cols],axis = 1)

# Combine all yearly dataframes into one master dataframe
vic_df = pd.concat([df_2012, df_2013, df_2014, df_2015, df_2016])
vic_df = vic_df.astype({'0-19': int, '20-64': int, '65+': int})
vic_df['Ratio: 65+ to 18+'] = vic_df['65+'] / (vic_df['65+'] + vic_df['20-64'])
vic_df = vic_df[['Year', 'LGA_name', 'LGA_code', '0-19', '20-64', '65+', 'Total_population', 'Ratio: 65+ to 18+']]
vic_df.reset_index(drop = True,inplace = True)

# Save to csv
out_path = "Output/"
out_dir = os.path.join(master_dir, out_path)
vic_df.to_csv(os.path.join(out_dir,'populations.csv'),encoding = 'utf-8',index = False)
