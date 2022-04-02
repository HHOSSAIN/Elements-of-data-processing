##
## merge_script.py
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

# Retrieve filepath of CSVs
master_dir = os.path.dirname(os.path.dirname(__file__))
rel_path = "Output/"
data_dir = os.path.join(master_dir, rel_path)

# Read in the gaming.csv
raw_df_ge = pd.read_csv(os.path.join(data_dir,'gaming.csv'),encoding = 'utf-8')
raw_df_ge = raw_df_ge.drop(raw_df_ge.columns[1],axis = 1)

# Read in the populations.csv
raw_df_pop = pd.read_csv(os.path.join(data_dir,'populations.csv'),encoding = 'utf-8')

# Read in the income.csv
raw_df_inc = pd.read_csv(os.path.join(data_dir,'income.csv'),encoding = 'utf-8')
raw_df_inc = raw_df_inc.drop(raw_df_inc.columns[1],axis = 1)


# Merge all csv dataframes
df = pd.merge(raw_df_pop,raw_df_inc,on = ['LGA_code','Year'])
df = pd.merge(df,raw_df_ge,on = ['LGA_code','Year'])

# Combine all yearly dataframes into one master dataframe
df = df.astype({'Total_EGMs': int, 'Venues': int})
df['EGMs_PV'] = df['Total_EGMs'] / (df['Venues'])
df['People_PEGM'] = (df['Total_population'] - df['0-19'])/df['Total_EGMs']
df['Expenditure_PP (AUD)'] = df['Net_expenditure (AUD)'] / (df['Total_population'] - df['0-19'])
df['Expenditure_PEGM (AUD)'] = df['Net_expenditure (AUD)'] / (df['Total_EGMs'])
df['Expenditure_PV (AUD)'] = df['Net_expenditure (AUD)'] / (df['Venues'])

summary_df = df.groupby(['LGA_name','Year']).agg({'Net_expenditure (AUD)':['sum'],'Total_EGMs':['sum'],'Total_population':['sum'],'Venues':['sum']})
df['EXP_PP_label'] = ""

for i in range(len(df)):
    if df.loc[i, 'Expenditure_PP (AUD)'] == 0:
        df.loc[i,'EXP_PP_label'] = "None"
    elif df.loc[i, 'Expenditure_PP (AUD)'] <= 200:
        df.loc[i,'EXP_PP_label'] = "Very Low"
    elif df.loc[i, 'Expenditure_PP (AUD)'] <= 400:
        df.loc[i,'EXP_PP_label'] = "Low"
    elif df.loc[i, 'Expenditure_PP (AUD)'] <= 600:
        df.loc[i,'EXP_PP_label'] = "Medium"
    elif df.loc[i, 'Expenditure_PP (AUD)'] <= 800:
        df.loc[i,'EXP_PP_label'] = "High"
    else:
        df.loc[i,'EXP_PP_label'] = "Very High"
        
df = df[df.Total_EGMs != 0]
df.reset_index(drop = True,inplace = True)

# Save to csv
out_path = "Output/"
out_dir = os.path.join(master_dir, out_path)
df.to_csv(os.path.join(out_dir,'merged.csv'),encoding = 'utf-8',index = False)

