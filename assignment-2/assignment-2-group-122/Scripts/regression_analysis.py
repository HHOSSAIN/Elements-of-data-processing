##
## regression_analysis.py
## COMP20008 Assignment 2
##
## Created by Group 122
## Copyright © 2021. All rights reserved.
##

import pandas as pd
pd.options.mode.chained_assignment = None  # default = 'warn'
import numpy as np
import scipy.stats
import os
import math
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from sklearn import neighbors
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Retrieve filepath of CSVs
master_dir = os.path.dirname(os.path.dirname(__file__))
rel_path = "Output/"
data_dir = os.path.join(master_dir, rel_path)

# Read in the merged.csv
raw_df = pd.read_csv(os.path.join(data_dir,'merged.csv'),encoding = 'utf-8')

summary_df = raw_df.groupby(['LGA_name','Year']).agg({'Total_EGMs':['sum'], 'Venues':['sum'], 'Total_population':['sum'],'Net_expenditure (AUD)':['sum']})

# Interested variables
features_arr = ['Total_EGMs','Expenditure_PP (AUD)']
goal = 'Net_expenditure (AUD)'

# X: features
features = ['Total_population','Ratio: 65+ to 18+','Median_income','Unemployment_rate','Total_EGMs','People_PEGM','Venues','Net_expenditure (AUD)','Expenditure_PP (AUD)','Expenditure_PEGM (AUD)','EGMs_PV','Expenditure_PV (AUD)']
features_df = raw_df[features]
features_df = features_df.astype('float64')
df = pd.DataFrame(features_df,columns = features)

# Y: target
goal_df = raw_df[goal]
target = pd.DataFrame(goal_df,columns = [goal])
target = target.astype('float64')

# Loop to determine most influential pair of features on target statistic
for i in range(0,len(features)):
    for j in range(i+1,len(features)):
        curr_features = [features[i],features[j]]
        if goal in curr_features:
            break;
        X = df[curr_features]
        Y = target[goal]

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        lm = linear_model.LinearRegression()
        model = lm.fit(X_train, y_train)
        
        r2_test = lm.score(X_test, y_test)
        r2_train = lm.score(X_train, y_train)
        
        print(curr_features)
        print('Coefficient of determination (training): {0:.2f}'.format(r2_train), end = " | ")
        print('Coefficient of determination (test): {0:.2f}'.format(r2_test))

# Construct a linear regression model with most influential pair variables
X = df[features_arr]
Y = target[goal]

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
lm = linear_model.LinearRegression()
model = lm.fit(X_train, y_train)

# Coefficient of determination figures
r2_test = lm.score(X_test, y_test)
r2_train = lm.score(X_train, y_train)

# Plot 3D
x = X[X.columns[0]]
y = X[X.columns[1]]
z = Y

x_pred = np.linspace(min(x) * 0.95, max(x) * 1.05, 100)
y_pred = np.linspace(min(y) * 0.95, max(y) * 1.05, 100)
xx_pred, yy_pred = np.meshgrid(x_pred, y_pred)
model_viz = np.array([xx_pred.flatten(), yy_pred.flatten()]).T
predicted = model.predict(model_viz)

r2 = model.score(X, Y)

plt.style.use('default')

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(x,y,z,color = 'k',zorder = 15,linestyle = 'none',marker = 'o',alpha = 0.5)
ax.scatter(xx_pred.flatten(),yy_pred.flatten(),predicted,facecolor = (0,0,0,0),s = 5,edgecolor='#72b4f0')
ax.set_xlabel(features_arr[0], fontsize = 10)
ax.set_ylabel(features_arr[1], fontsize = 10)
ax.set_zlabel(goal, fontsize = 10)
ax.locator_params(nbins=6, axis='x')
ax.locator_params(nbins=5, axis='y')
ax.zaxis.set_tick_params(labelsize = 8)
ax.yaxis.set_tick_params(labelsize = 8)
ax.zaxis._axinfo['label']['space_factor'] = 10.0
ax.xaxis.set_tick_params(labelsize = 8)
ax.view_init(elev = 18,azim = -142)
plt.title("R\u00b2: {0:.2f}".format(r2))
plt.legend(['Actual','Predicted'])
fig.tight_layout()
plt.show()


# Plot residules
y_test_h = lm.predict(X_test)
y_train_h = lm.predict(X_train)

residual_train = [Y - yh for Y, yh in zip(y_train, y_train_h)]
residual_test = [Y - yh for Y, yh in zip(y_test, y_test_h)]

resplot = plt.figure(2)
plt.scatter(y_test_h, residual_test, color='C0', label = 'R^2 (test):{0:.2f}'.format(r2_test))
plt.scatter(y_train_h, residual_train, color='C4', alpha = 0.1, label = 'R^2 (training):{0:.2f}'.format(r2_train))
plt.plot([min(y_train_h), max(y_train_h)], [0,0], color= 'C2')
plt.legend()
plt.xlabel(goal)
plt.title(f"Residule plot")
resplot.show()

# key_feature 0 vs key_feature 1
indepplot = plt.figure(3)
result = scipy.stats.linregress(df[features_arr[0]], df[features_arr[1]])
pearsson_coeff = result.rvalue
coeff_det = pearsson_coeff * pearsson_coeff
plt.scatter(df[features_arr[0]], df[features_arr[1]], color='C0', label = 'R :{0:.2f}'.format(pearsson_coeff))
plt.xlabel(features_arr[0])
plt.ylabel(features_arr[1])
plt.legend()
indepplot.show()
input()



# Save to csv
#out_path = "Output/"
#out_dir = os.path.join(master_dir, out_path)
#df.to_csv(os.path.join(out_dir,'merged.csv'),encoding = 'utf-8',index = False)

