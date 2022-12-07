import pandas as pd
import numpy as np
import hashlib
import re


data = pd.read_csv("/Users/tina/Desktop/HDA Term 1/CDM/CDM_Coursework2/Data/customer_information.csv")
data

# Anonymised data
anon_data = data

# Drop unneeded direct identifiers
anon_data = anon_data.drop(['given_name', 'surname', 'phone_number', 'national_insurance_number', 'bank_account_number'], axis=1)

# Hashing NIN
hashed_nin = data["national_insurance_number"].apply(lambda x: 
    hashlib.sha256(x.encode()).hexdigest())

anon_data['id'] = hashed_nin

# print(hashed_nin.shape)

# Create the reference table and adding the hashed_nin values
reference_table = pd.DataFrame()
reference_table['nin_hashed'] = hashed_nin
reference_table['national_insurance_number'] = data['national_insurance_number']
print(reference_table)



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
anon_data['height'] = pd.cut(anon_data['height'], np.linspace(0, 2, 9))

# Banding avg_drinks
#anon_data['avg_n_drinks_per_week'] = pd.cut(anon_data['avg_n_drinks_per_week'], np.linspace(0, 2, 9))
print(anon_data['avg_n_drinks_per_week'].max())
print(anon_data['avg_n_drinks_per_week'].min())


print(pd.concat([anon_data['weight'], anon_data['height']], axis=1) )
#print(pd.concat([anon_data['weight'], anon_data['weight2']], axis=1) )


# Re-ordering the columns
anon_data = anon_data[['id', 'gender', 'birthdate', 'country_of_birth', 'postcode', 'cc_status', 'weight', 'height', 'blood_group', 'avg_n_drinks_per_week', 'avg_n_cigret_per_week', 'education_level', 'n_countries_visited']]

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(anon_data)

anon_data.to_csv("output.csv", sep=",")

# K-anonymity, 2 anonymous dataset
k = 2

# Calculate number of unique combinations in the columns
#df_count = anon_data.groupby(['gender', 'birthdate', 'country_of_birth', 'postcode', 'cc_status', 'weight', 'height', 'blood_group', 'avg_n_drinks_per_week', 'avg_n_cigret_per_week', 'education_level', 'n_countries_visited']).size().reset_index(name = 'Count')
df_count = anon_data.groupby(['gender', 'birthdate', 'postcode']).size().reset_index(name = 'Count')

#df_count = anon_data.groupby(['gender', 'birthdate', 'country_of_birth', 'postcode', 'cc_status', 'weight', 'height', 'blood_group', 'avg_n_drinks_per_week', 'avg_n_cigret_per_week', 'education_level', 'n_countries_visited']).size().describe()

#df_count = anon_data.groupby(['gender', 'birthdate']).size().describe()


#print(df_count)

# Filter rows with count less than k
print(df_count[df_count['Count']])
#df_count[df_count['Count']<k]















