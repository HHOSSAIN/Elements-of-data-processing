##
## income.py
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
drop_cols = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 28, 29, 30, 31, 32, 33, 34, 35, 36]

# Read in the xls 2012
raw_df = pd.read_excel(os.path.join(data_dir,os.path.join(data_dir,'income_data.xls')),sheet_name = 'Table 1.5')
df = raw_df[137:216]
df = df.drop(df.columns[drop_cols],axis = 1)
df.columns = ['LGA_code','LGA_name','2012','2013','2014','2015','2016']

# Construct Victorian dataframe with year and median income columns
vic_df = pd.melt(df,id_vars = ['LGA_code','LGA_name'],value_vars = ['2012','2013','2014','2015','2016'])
vic_df.columns = ['LGA_code','LGA_name','Year','Median_income']
vic_df.reset_index(drop = True,inplace = True)

# Save to csv
out_path = "Output/"
out_dir = os.path.join(master_dir, out_path)
vic_df.to_csv(os.path.join(out_dir,'income.csv'),encoding = 'utf-8',index = False)
