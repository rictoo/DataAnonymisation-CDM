import pandas as pd
import numpy as np
import hashlib
import re
import os
import math
from functions import *

# 
# Main anonymisation class
# 

# Read in data to be anonymised
data = pd.read_csv("Data/customer_information.csv")

# Create anon_data variable as initial data with unneeded direct identifiers dropped
#anon_data = data.drop(['given_name', 'surname', 'phone_number', 'national_insurance_number', 'bank_account_number'], axis=1)
anon_data = pd.DataFrame()

# Clean NIN formatting and assign Sample ID as a hashed form of the NIN
key = os.urandom(16)
data["national_insurance_number"], anon_data['Sample.ID'], salts = zip(*data["national_insurance_number"].apply(
    lambda x: hash(key, re.sub(r'(.{2})(?!$)','\\1 ', x.replace(' ', '') ))))

# Create a reference table between NIN and respective hashed NIN
reference_table = pd.DataFrame()
reference_table['Hashed.NIN'] = anon_data['Sample.ID']
reference_table['Salt'] = salts
reference_table['Key'] = key.hex()
reference_table['NIN'] = data['national_insurance_number']

# Assign gender
anon_data['Gender'] = data['gender']

# Assign birthdate as banded birthyears
# Select the birth year only
birthyears = pd.DatetimeIndex(data['birthdate']).year
# Band the birth years into 5-year intervals
anon_data['Birthyear'] = pd.cut(birthyears, np.arange(birthyears.min(), birthyears.max()+20, 20), right=False)

# Assign postcode as truncated postcode
anon_data['Postcode'] = data['postcode'].apply(lambda x: re.search('[a-zA-Z]*', x).group(0))

#anon_data['Region'] = data['postcode'].apply(lambda x: postcode_to_region(x))
postcode_dictionary = pd.read_csv('Data/postcode_region.csv')
anon_data = pd.merge(anon_data, postcode_dictionary.iloc[: , :-1], on='Postcode', how='left')
#anon_data['Region'] = anon_data['Postcode'].to_frame().merge(postcode_dictionary.iloc[: , :-1], on='Postcode', how='left')

#print(anon_data['Region'])

# Assign weight and height as banded weights and heights
#anon_data['Weight'] = pd.cut(data['weight'], np.arange(math.floor(data['weight'].min()), math.floor(data['weight'].max()+20), 20), right=False)
weight_noise = np.random.normal(0,1,1000)*5
anon_data['Weight'] = round(data['weight']+weight_noise, 1)

# Round minimum and maximum heights to nearest one-fifth prior to making bins
#anon_data['Height'] = pd.cut(data['height'], np.arange(round(data['height'].min()*5)/5, (round(data['height'].max()*5)/5)+0.2, 0.2), right=False)
height_noise = np.random.normal(0,1,1000)/5
anon_data['Height'] = round(data['height']+height_noise, 2)
bmi = data['weight'] / data['height']**2
print(anon_data['Height'])
print(data['height'])#anon_data['BMI'] = pd.cut(bmi, bins=[math.floor(bmi.min()), 18.5, 25, 30, round(bmi.max(), -1)], right=False)
#print(anon_data['BMI'])
# Assign avg_drinks as banded avg_drinks
#anon_data['avg_n_drinks_per_week'] = pd.cut(anon_data['avg_n_drinks_per_week'], np.linspace(0, 2, 9))

# Assign education level as banded education level
anon_data['Education.Level'] = data['education_level'].map(lambda x: "Higher" if x in ["bachelor", "masters", "phD"] else "BasicOther")

anon_data['Continent.of.Birth'] = data['country_of_birth'].apply(lambda x: country_to_continent(x))

# Output the files
anon_data.to_csv("output.csv", sep=",", index=None)
reference_table.to_csv("reference_table.csv", sep=",", index=None)

# Calculating K-anonymity, 2 anonymous dataset
k = 2
############
# Checking k-anonymity, fix this for variable names
df_count = anon_data.groupby(['Gender', 'Birthyear', 'Continent.of.Birth', 'Education.Level', 'Region']).size().reset_index(name = 'Count') 
print(df_count[df_count['Count']==1])
# print(df_count.size().describe())

print(anon_data.groupby('Education.Level').size())
print(anon_data.groupby('Continent.of.Birth').size())
print(anon_data.groupby('Region').size())


############
