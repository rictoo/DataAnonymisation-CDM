
import pandas as pd
import numpy as np
import hashlib
import re
import math
import pycountry_convert as pc

data = pd.read_csv("Data/customer_information.csv")
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
anon_data['birthdate'] = pd.cut(anon_data['birthdate'], range(anon_data['birthdate'].min(), anon_data['birthdate'].max(), 20))
# print(anon_data['birthdate'])


# Country_of_birth

# Current_country

# Postcode
#sep = ' '
postcode_list = []
for i in data['postcode']:
   # strip = str(i).split(sep, 1)[0]
    #anon_data['postcode'] = strip
    postcode_list.append(re.search('[a-zA-Z]*', i).group(0))

anon_data['postcode'] = postcode_list

# CC_Status

# Weight and Height
#print(anon_data['height'].max())
anon_data['weight'] = pd.cut(anon_data['weight'], range(math.floor(anon_data['weight'].min()), math.floor(anon_data['weight'].max()), 20))
anon_data['height'] = pd.cut(anon_data['height'], np.linspace(0, 2, 9))

# Banding avg_drinks
#anon_data['avg_n_drinks_per_week'] = pd.cut(anon_data['avg_n_drinks_per_week'], np.linspace(0, 2, 9))
print(anon_data['avg_n_drinks_per_week'].max())
print(anon_data['avg_n_drinks_per_week'].min())

# Education level banding
edu_list = []
for i in data['education_level']:
    if(i=="bachelor" or i=="masters" or i=="phD"):
        edu_list.append("supersmart")
    else:
        edu_list.append(i)
anon_data['education_level'] = edu_list



# Country of birth
def country_to_continent(country_name):
    country_alpha2 = ""
    try:
        country_code = pc.country_name_to_country_alpha2(country_name, cn_name_format="default")
        continent_name = pc.country_alpha2_to_continent_code(country_code)
        if(continent_name == "AN"):
            continent_name = "OTHR"
        elif(continent_name == "EU" or continent_name =="AS" or continent_name =="OC"):
            continent_name = "EURASOC"
        elif(continent_name == "NA" or continent_name =="SA"):
            continent_name = "AMER"
        
    except:
        continent_name = "OTHR"
    #country_continent_code = pc.convert_country_alpha2_to_continent_code(country_alpha2)
    #country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return continent_name
#for cname in anon_data['country_of_birth']: 
    #print(country_to_continent(cname))
test = anon_data['country_of_birth'].apply(lambda x: country_to_continent(x))
#print(anon_data['country_of_birth'])

merged = anon_data['country_of_birth'] + " " + test
merged.to_csv("merged.csv", sep=",")

anon_data['continent'] = test


#print(test)
#anon_data
   # anon_data['country_of_birth'] = country_to_continent(anon_data['country_of_birth'])

# country_alpha2 = pc.country_alpha2_to_continent_code(
         #   pc.country_name_to_country_alpha2(country_name), cn_name_format="default")
        #print(country_alpha2)


print(pd.concat([anon_data['weight'], anon_data['height']], axis=1) )
#print(pd.concat([anon_data['weight'], anon_data['weight2']], axis=1) )


# Re-ordering the columns
anon_data = anon_data[['id', 'gender', 'birthdate', 'country_of_birth', 'continent', 'postcode', 'cc_status', 'weight', 'height', 'blood_group', 'avg_n_drinks_per_week', 'avg_n_cigret_per_week', 'education_level', 'n_countries_visited']]

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# print(anon_data)

anon_data.to_csv("output.csv", sep=",")

# K-anonymity, 2 anonymous dataset
k = 2

# Calculate number of unique combinations in the columns
#df_count = anon_data.groupby(['gender', 'birthdate', 'country_of_birth', 'postcode', 'cc_status', 'weight', 'height', 'blood_group', 'avg_n_drinks_per_week', 'avg_n_cigret_per_week', 'education_level', 'n_countries_visited']).size().reset_index(name = 'Count')

#print anon_data.continent == 'UKN'

#df_count = anon_data.groupby(['gender', 'birthdate', 'continent']).size().reset_index(name = 'Count')
df_count = anon_data.groupby(['gender', 'birthdate', 'continent', 'education_level']).size().reset_index(name = 'Count') 
#df_count = anon_data.groupby(['education_level']).size().reset_index(name = 'Count') 

# Do we include outcome in k-anonymity?
# Do we include "other" elements in the calculation of k-anonymity?
# Do we include postcode at all?
# Can we have two datasets?


print(df_count[df_count['Count']<3  ])
#print(df_count)

#df_count = anon_data.groupby(['gender', 'birthdate', 'country_of_birth', 'postcode', 'cc_status', 'weight', 'height', 'blood_group', 'avg_n_drinks_per_week', 'avg_n_cigret_per_week', 'education_level', 'n_countries_visited']).size().describe()

#df_count = anon_data.groupby(['gender', 'birthdate']).size().describe()
#df_count = anon_data.groupby(['education_level']).size().describe()


#print(df_count)

# Filter rows with count less than k

#df_count[df_count['Count']<k]



# maybe

country_code = pc.country_name_to_country_alpha2("Namibia", cn_name_format="default")
#print(country_code)
continent_name = pc.country_alpha2_to_continent_code(country_code)
#print(continent_name)

#print(anon_data['education_level'].unique())

"""
df_exceptions = pd.DataFrame(columns=anon_data.columns)
for index,row in anon_data.iterrows():
   
      try:
        country_code = pc.country_name_to_country_alpha2(row['country_of_birth'], cn_name_format="default")
        continent_name = pc.country_alpha2_to_continent_code(country_code)
        anon_data.loc[index, 'Continent'] = continent_name
      ## print(country_code)
      # print (index)
       
    
      except:
       # print(row['country_of_birth'])
        #cond = row['country_of_birth']
        rows = anon_data.country_of_birth
        df_exceptions = df_exceptions.append(rows, ignore_index=True)
        anon_data.drop(rows.index, inplace=True)

    
  # continent_name = pc.country_alpha2_to_continent_code(country_code)
   #anon_data["Continent"] = continent_name
   #print(continent_name)
#print(anon_data[Country]== "Congo (Brazzaville)")
df_exceptions
"""


#print(pc.country_name_to_country_alpha2("Hungary"))