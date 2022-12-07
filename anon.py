#%%

import pandas as pd
import numpy as np
import hashlib
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize
import re
import os

data = pd.read_csv(os.getcwd() + "/Data/customer_information.csv")
data

# Hashing NIN
hashed_nin = data["national_insurance_number"].apply(lambda x: 
    hashlib.sha256(x.encode()).hexdigest())

# print(hashed_nin.shape)

# Create the reference table and adding the hashed_nin values
reference_table = pd.DataFrame()
reference_table['nin_hashed'] = hashed_nin
reference_table['national_insurance_number'] = data['national_insurance_number']
print(reference_table)

# Anonymised data
anon_data = data

# Drop unneeded direct identifiers
anon_data.drop(['given_name', 'surname', 'phone_number', 'national_insurance_number', 'bank_account_number'], axis=1)

# Birthdate
# Convert birthdate to a datetime object
anon_data['birthdate'] = pd.to_datetime(anon_data['birthdate'])
# Select the birth year only
anon_data['birthdate'] = pd.DatetimeIndex(anon_data['birthdate']).year
# print(anon_data['birthdate'])
# Band the birth years into 5-year intervals
anon_data['birthdate'] = pd.cut(anon_data['birthdate'], range(1900, 2500, 5))
# print(anon_data['birthdate'])

# Country_of_birth

# Current_country

# Postcode
#sep = ' '
postcode_list = []
for i in data['postcode']:
   # strip = str(i).split(sep, 1)[0]
    #anon_data['postcode'] = strip
    postcode_list.append(re.search('([^\s]+)', i).group(0))

anon_data['postcode'] = postcode_list

# CC_Status

# Weight and Height
#print(anon_data['height'].max())
anon_data['weight'] = pd.cut(anon_data['weight'], range(0, 105, 5))
#print(max(anon_data['height']))
print(min(anon_data['height']))

anon_data['height'] = pd.cut(anon_data['height'], np.linspace(1.4, 2, 7))

# Plot heights
#figsize(7, 5)
#plt.hist(anon_data['height'], color='blue', edgecolor='black', bins=10)
#fig, ax = plt.subplots()
#anon_data['height'].value_counts().plot(ax=ax, kind='bar')
#fig.show()

anon_data.groupby('height')['height'].count().plot(kind='bar')

#print(pd.concat([anon_data['weight'], anon_data['height']], axis=1) )
#print(pd.concat([anon_data['weight'], anon_data['weight2']], axis=1) )


# Blood group

# Avg_n_drinks_per_week and cigrets

# Education_level

# n_countries_visited



## K-anonymity test

test = {'age': [20, 20, 20, 30, 30, 30], 'zip': [130, 130, 130, 148, 148, 148]}
test = pd.DataFrame(data=test)
print(test.groupby(['age', 'zip']).size())








# %%

