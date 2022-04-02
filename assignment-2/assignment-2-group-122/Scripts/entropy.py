import pandas as pd
import numpy as np
import argparse
import os
import math

# Retrieve filepath of CSVs
master_dir = os.path.dirname(os.path.dirname(__file__))
rel_path = "Output/"
data_dir = os.path.join(master_dir, rel_path)

# Read in the merged.csv
raw_df = pd.read_csv(os.path.join(data_dir,'merged.csv'),encoding = 'utf-8')

#print(data.head())

count=0

#print(type(data['EXP_PP_label'].unique()))
labels = data['EXP_PP_label'].unique() #list of all unique labels

# GETTING COUNT OF ROWS FOR EACH UNIQUE EXPENDITURE LABEL..."MY_DICT" HOLDS IT
my_dict={}
for i in labels:
    my_dict[i] = 0

for index, row in data.iterrows():
    my_dict[row['EXP_PP_label']] += 1
#print(my_dict)

# COUNT OF TOTAL ROWS AND TOTAL TYPE OF UNIQUE EXPENDITURE LABELS
t_rows=0
for x in my_dict.values():
    t_rows += x
#print(t_rows)
n_labels=(len(my_dict.keys()))

# CALCULATING ENTROPY of exp/person
entropy_exp_per_person = 0 #discretised on basis of income labels
for x in my_dict.values():
    entropy_exp_per_person += -(x/t_rows)*math.log((x/t_rows),2) #2nd arg is the base
#print(entropy_exp_per_person)

# discretising ratio of 65+ to over 18
data['Age_Group'] = ""
#for i in range(len(data)):
for i, row in data.iterrows():
    if data.loc[i, 'Ratio: 65+ to 18+'] <= 0.1:
        data.loc[i,'Age_Group'] = "A"
    elif data.loc[i, 'Ratio: 65+ to 18+'] <= 0.2:
        data.loc[i,'Age_Group'] = "B"
    elif data.loc[i, 'Ratio: 65+ to 18+'] <= 0.3:
        data.loc[i,'Age_Group'] = "C"
    elif data.loc[i, 'Ratio: 65+ to 18+'] <= 0.4:
        data.loc[i,'Age_Group'] = "D"
    else:
        data.loc[i,'Age_Group'] = "E"
        
age_groups = data['Age_Group'].unique()
#print(age_groups)

my_dict2={}
for i in age_groups:
    my_dict2[i] = 0

# GETTING COUNT OF ROWS PRESENT IN EACH AGE GROUP..."MY_DICT_2" HOLDS IT
for index, row in data.iterrows():
    my_dict2[row['Age_Group']] += 1
#print(my_dict2)


# CALCULATING ENTROPY of Age Group
entropy_age_group = 0 #discretised on basis of income labels
for x in my_dict2.values():
    entropy_age_group += -(x/t_rows)*math.log((x/t_rows),2) #2nd arg is the base
#print("entropy_age_group= ", entropy_age_group)



# new GroupBy dataframe
grouped = data.groupby('Age_Group')
#for key, item in grouped:
 #   print(grouped. get_group(key))
    
    
#START
# CALCULATING ENTROPY #
entropy_exp_per_person_G_Age_Ratio = 0 #discretised on basis of income labels

my_dict2_vals = list(my_dict2.values())
my_dict2_vals_length = len(my_dict2_vals)
ints=0
for key, item in grouped:
    #print("types= ", type(ints), type(my_dict2_vals_length), ints)
    if ints < my_dict2_vals_length:
        fraction = my_dict2_vals[ints]/t_rows #
        ints+=1
    else:
        break

    # PREVIOUSLY, MY_DICT HELD THE COUNT OF ROWS FOR EACH EXPENDITURE LABEL TYPE
    nested_my_dict={}
    #GETTING THE EXPENDITURE PER PERSON LABEL COUNT FOR EACH AGE GROUP
    for i in labels: #labels is a list holding the names of all unique expenditure per person groups
        nested_my_dict[i] = 0

    # GETTING COUNT OF ROWS FOR EACH EXPENDITURE LABEL TYPE FOR EACH GROUPED DATAFRAME
    # LOOPING THROUGH EACH GROUP OF DATAFRAME
    for index, row in grouped. get_group(key).iterrows():
        #print(row['Age_Group'] , row['EXP_PP_label'])
        nested_my_dict[row['EXP_PP_label']] += 1

    # GETTING COUNT OF THE NESTED TOTAL ROWS FOR 1 OF THE GROUPED DATAFRAMES
    nested_t_rows=0
    for x in nested_my_dict.values():
        nested_t_rows += x


    nested_entropy_exp_per_person = 0
    #print("nested_my_dict= ", nested_my_dict)
    for x in nested_my_dict.values():
        if x == 0:
            continue
        nested_entropy_exp_per_person += -(x/nested_t_rows)*math.log((x/nested_t_rows),2) #2nd arg is the base
    #print("nested_entropy_exp_per_person= ", nested_entropy_exp_per_person)
    #entropy_exp_per_person_G_Age_Ratio += fraction * (-1) * nested_entropy_exp_per_person
    entropy_exp_per_person_G_Age_Ratio += fraction * nested_entropy_exp_per_person
    #print("entropy_exp_per_person_G_Age_Ratio(update)= ", entropy_exp_per_person_G_Age_Ratio)

#print("entropy_exp_per_person_G_Age_Ratio= ", entropy_exp_per_person_G_Age_Ratio)

mutual_information = entropy_exp_per_person - entropy_exp_per_person_G_Age_Ratio
#print(mutual_information)
        
normalised_mi = mutual_information/min(entropy_exp_per_person, entropy_age_group)
print("normalised_mi= ", normalised_mi)
