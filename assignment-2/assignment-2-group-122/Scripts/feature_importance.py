##
## feature_importance.py
## COMP20008 Assignment 2
##
## Parts of script originally written by Eric from https://aegis4048.github.io/.
## https://aegis4048.github.io/mutiple_linear_regression_and_visualization_in_python#2D%20linear%20regression%20with%20scikit-learn
## Edited and extended by Group 122.
##
## Created by Group 122
## Copyright Â© 2021. All rights reserved.
##

import pandas as pd
pd.options.mode.chained_assignment = None  # default = 'warn'
import numpy as np
import os
import math
import matplotlib.pyplot as plt
import rfpimp

from mpl_toolkits.mplot3d import Axes3D
from sklearn import neighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Retrieve filepath of CSVs
master_dir = os.path.dirname(os.path.dirname(__file__))
rel_path = "Output/"
data_dir = os.path.join(master_dir, rel_path)

# Read in the merged.csv
raw_df = pd.read_csv(os.path.join(data_dir,'merged.csv'),encoding = 'utf-8')

summary_df = raw_df.groupby(['LGA_name','Year']).agg({'Total_EGMs':['sum'], 'Venues':['sum'], 'Total_population':['sum'],'Net_expenditure (AUD)':['sum']})

# X: features
features = ['Expenditure_PP (AUD)','Total_population','Ratio: 65+ to 18+','Median_income','Unemployment_rate','Total_EGMs','Net_expenditure (AUD)']
features_df = raw_df[features]
features_df = features_df.astype('float64')
df = pd.DataFrame(features_df,columns = features)

# Train and split data

df_train, df_test = train_test_split(df, test_size=0.20)
df_train = df_train[features]
df_test = df_test[features]

test_feature = 'Expenditure_PP (AUD)'
X_train, y_train = df_train.drop(test_feature,axis = 1), df_train[test_feature]
X_test, y_test = df_test.drop(test_feature,axis = 1), df_test[test_feature]

rf = RandomForestRegressor(n_estimators=100, n_jobs=-1)
rf.fit(X_train, y_train)

# Permutation feature importance

imp = rfpimp.importances(rf, X_test, y_test)

# Plot

fig, ax = plt.subplots(figsize=(6, 3))
ax.barh(imp.index, imp['Importance'], height=0.8, facecolor='grey', alpha=0.8, edgecolor='k')
ax.set_xlabel('Importance score')
ax.set_title(f"Permutation feature importance: {test_feature}")
plt.gca().invert_yaxis()

fig.tight_layout()
plt.show()
