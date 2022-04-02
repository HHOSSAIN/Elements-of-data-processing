##
## gaming.py
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

# Initialise dictionary for converting LGA codes and other useful variables
LGA_dict = {"C2": "20110", "C43": "20260", "C20": "20570", "M15": "20660", "C29": "20740", "C6": "20830", "M8": "20910", "C48": "21010", "M12": "21110", "M28": "21180", "C7": "21270", "C10": "21370", "M24": "21450", "M23": "21610", "C31": "21670", "C18": "21750", "C3": "21830", "M11": "21890", "C28": "22110", "M22": "22170", "C38": "22250", "M7": "22310", "C25": "22410", "C32": "22490", "C19": "22620", "M21": "22670", "C21": "22750", "C24": "22830", "C26": "22910", "C8": "22980", "M3": "23110", "C5": "23190", "M27": "23270", "C35": "23350", "M20": "23430", "M18": "23670", "C30": "23810", "C46": "23940", "C45": "24130", "M14": "24210", "C49": "24250", "M5": "24330", "M17": "24410", "M1": "24600", "M29": "24650", "C27": "24780", "C13": "24850", "C17": "24900", "M19": "24970", "M9": "25060", "C22": "25150", "M10": "25250", "M31": "25340", "C47": "25430", "C36": "25490", "C41": "25620", "M16": "25710", "C14": "25810", "M2": "25900", "C44": "25990", "C1": "26080", "C4": "26170", "C37": "26260", "M6": "26350", "C42": "26430", "C33": "26490", "C23": "26610", "C34": "26670", "C9": "26700", "C16": "26730", "C12": "26810", "C39": "26890", "M13": "26980", "M26": "27070", "C15": "27170", "M30": "27260", "M4": "27350", "M25": "27450", "C40": "27630"}
drop_cols = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16, 17]

# Read in the xls 2012
raw_df = pd.read_excel(os.path.join(data_dir,os.path.join(data_dir,'Historical_gaming.xls')),sheet_name = '201112')
raw_df = raw_df[9:88]
raw_df.columns = ["LGA_name","LGA","Region","Net_expenditure (AUD)","SEIFA DIS Score","SEIFA","SEIFA","SEIFA ","SEIFA ADVDIS Score","SEIFA","SEIFA","SEIFA","Adult","Adults","EGMs","EXP","Workforce","Unemployed","Unemployment_rate"]
raw_df['Year'] = "2012"
df_2012 = raw_df

# Read in the xls 2013
raw_df = pd.read_excel(os.path.join(data_dir,'Historical_gaming.xls'),sheet_name = '201213')
raw_df = raw_df[9:88]
raw_df.columns = ["LGA_name","LGA","Region","Net_expenditure (AUD)","SEIFA DIS Score","SEIFA","SEIFA","SEIFA ","SEIFA ADVDIS Score","SEIFA","SEIFA","SEIFA","Adult","Adults","EGMs","EXP","Workforce","Unemployed","Unemployment_rate"]
raw_df['Year'] = "2013"
df_2013 = raw_df

# Read in the xls 2014
raw_df = pd.read_excel(os.path.join(data_dir,'Historical_gaming.xls'),sheet_name = '201314')
raw_df = raw_df[9:88]
raw_df.columns = ["LGA_name","LGA","Region","Net_expenditure (AUD)","SEIFA DIS Score","SEIFA","SEIFA","SEIFA ","SEIFA ADVDIS Score","SEIFA","SEIFA","SEIFA","Adult","Adults","EGMs","EXP","Workforce","Unemployed","Unemployment_rate"]
raw_df['Year'] = "2014"
df_2014 = raw_df

# Read in the xls 2015
raw_df = pd.read_excel(os.path.join(data_dir,'Historical_gaming.xls'),sheet_name = '201415')
raw_df = raw_df[9:88]
raw_df.columns = ["LGA_name","LGA","Region","Net_expenditure (AUD)","SEIFA DIS Score","SEIFA","SEIFA","SEIFA ","SEIFA ADVDIS Score","SEIFA","SEIFA","SEIFA","Adult","Adults","EGMs","EXP","Workforce","Unemployed","Unemployment_rate"]
raw_df['Year'] = "2015"
df_2015 = raw_df

# Read in the xls 2016
raw_df = pd.read_excel(os.path.join(data_dir,'Historical_gaming.xls'),sheet_name = '201516')
raw_df = raw_df[9:88]
raw_df.columns = ["LGA_name","LGA","Region","Net_expenditure (AUD)","SEIFA DIS Score","SEIFA","SEIFA","SEIFA ","SEIFA ADVDIS Score","SEIFA","SEIFA","SEIFA","Adult","Adults","EGMs","EXP","Workforce","Unemployed","Unemployment_rate"]
raw_df['Year'] = "2016"
df_2016 = raw_df

# Create master dataframe from combined yearly dataframes
vic_df = pd.concat([df_2012, df_2013, df_2014, df_2015, df_2016])
vic_df['LGA_code'] = vic_df['LGA'].map(LGA_dict)

vic_df = vic_df.drop(vic_df.columns[drop_cols],axis = 1)
vic_df['Total_EGMs'] = vic_df['EGMs'] * (vic_df['Adult'] / 1000)

vic_df = vic_df.astype({'Adult': float, 'Adults': float})
vic_df['Venues'] = vic_df['Adult'] / vic_df['Adults']

vic_df = vic_df.drop(vic_df.columns[[2, 3, 4]],axis = 1)
vic_df = vic_df[['Year', 'LGA_name', 'LGA_code', 'Total_EGMs', 'Venues', 'Unemployment_rate', 'Net_expenditure (AUD)']]

vic_df.replace([np.inf, -np.inf,np.nan],0,inplace = True)

vic_df.reset_index(drop = True,inplace = True)

# Save to csv
out_path = "Output/"
out_dir = os.path.join(master_dir, out_path)
vic_df.to_csv(os.path.join(out_dir,'gaming.csv'),encoding = 'utf-8',index = False)
