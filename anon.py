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

# Assign weight and height as banded weights and heights
anon_data['Weight'] = pd.cut(data['weight'], np.arange(math.floor(data['weight'].min()), math.floor(data['weight'].max()+20), 20), right=False)
# Round minimum and maximum heights to nearest one-fifth prior to making bins
anon_data['Height'] = pd.cut(data['height'], np.arange(round(data['height'].min()*5)/5, (round(data['height'].max()*5)/5)+0.2, 0.2), right=False)

# Assign avg_drinks as banded avg_drinks
#anon_data['avg_n_drinks_per_week'] = pd.cut(anon_data['avg_n_drinks_per_week'], np.linspace(0, 2, 9))

# Assign education level as banded education level
anon_data['Education.Level'] = data['education_level'].map(lambda x: "Higher" if x in ["bachelor", "masters", "phD"] 
                                                           else "Basic" if x in ["primary", "secondary"] else "Other")

anon_data['Continent.of.Birth'] = data['country_of_birth'].apply(lambda x: country_to_continent(x))

anon_data.to_csv("output.csv", sep=",", index=None)
reference_table.to_csv("reference_table.csv", sep=",", index=None)

# Calculating K-anonymity, 2 anonymous dataset
k = 2
############
# Checking k-anonymity, fix this for variable names
df_count = anon_data.groupby(['Gender', 'Birthyear', 'Continent.of.Birth', 'Education.Level']).size().reset_index(name = 'Count') 
print(df_count[df_count['Count']<2  ])
# print(df_count.size().describe())

print(anon_data.groupby('Education.Level').size())
############
