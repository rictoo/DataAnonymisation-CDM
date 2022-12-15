# %% [markdown]
# # Anonymisation of 'customer_information.csv' dataset for use by Imperial researchers and government (and calculation of K-anonymity)

# %% [markdown]
# Anonymisation is the practice of removing identifying information from data in order to protect individuals' privacy. By anonymising data, we can ensure that sensitive information is kept secure. In this project, we aim to create an anonymised dataset by removing personally identifiable information from the original dataset whilst attempting to retain its utility and insights by using a combination of techniques such as pseudonymous identification and data perturbation.

# %%
import pandas as pd
import numpy as np
import hashlib
import re
import os
import country_converter as coco
from geopy.geocoders import Nominatim
from cryptography.fernet import Fernet


# %% [markdown]
# ## Helper functions
# The following helper functions are needed:
# 

# %%
# Helper functions

# The following variable countries were hard-coded to fix unmatched territory errors
northern_countries = ["Svalbard & Jan Mayen Islands"]
southern_countries = ["Micronesia"]

# Parse country into shortform 
def parse_country(country_name):
    return coco.convert(country_name, to='name_short', include_obsolete=True)

# Convert country of birth into Hemisphere (Northern or Southern) based on latitude coordinates
def country_to_hemisphere(country_name):
    try:  
        if country_name in southern_countries: 
            return "Southern Hemisphere" 
        elif country_name in northern_countries:
            return "Northern Hemisphere"
        else:
            return ("Southern" if Nominatim(user_agent="CDM").geocode(parse_country(country_name)).latitude < 0 else "Northern") + " Hemisphere"
    except Exception as e:
        print(e)
        return "Error"
    
# SHA hash function using a key and salt
def hash(to_hash, key):
    salt = os.urandom(16)
    h = hashlib.sha256()
    h.update(key)
    h.update(salt)
    h.update(to_hash.encode())
    return to_hash, h.hexdigest(), salt.hex()

# To encrypt and save as encrypted file; specify file to encrypt, encrypted file destination, and destination key location
def encrypt(to_encrypt, file_destination, key_location):
    key = Fernet.generate_key() # AES in CBC mode with a 128-bit key for encryption
    fernet = Fernet(key)
    
    with open(key_location, 'wb') as f:
        f.write(key)
    
    with open(to_encrypt, 'rb') as f:
        plaintext = f.read()   
    
    encrypted = fernet.encrypt(plaintext)
    with open(file_destination, 'wb') as e:
        e.write(encrypted)


# %% [markdown]
# ## Loading required data and creating the anonymised dataframe

# %%
# Read in data to be anonymised
original_data = pd.read_csv("Data/customer_information.csv")

# Reading in postcode_region.csv to map given postcode to countries in the UK - 'England' and 'Other'(includes Wales, Scotland, Northern Ireland)
postcode_dictionary = pd.read_csv('Data/postcode_region.csv')

# Create anon_data variable as initial data with unneeded direct identifiers dropped
anon_data = pd.DataFrame()

postcode_dictionary.head()

# %% [markdown]
# ## Adding variables to the anonymised dataset

# %% [markdown]
# Assigning gender and case-control status as given

# %%
# Assign gender
anon_data['Gender'] = original_data['gender']

# Assign case-control status
anon_data['CC.Status'] = original_data['cc_status']

anon_data.head()

# %% [markdown]
# # Anonymisation

# %% [markdown]
# ## Pseudonymisation with hashed Sample ID

# %% [markdown]
# Next, a unique Sample ID is created from the National Insurance Number to link the anonymised data with the reference data containing sensitive information.

# %%
# Clean NIN formatting and assign Sample ID as a hashed form of the NIN
key = os.urandom(16)
original_data["national_insurance_number"], anon_data['Sample.ID'], salts = zip(*original_data["national_insurance_number"].apply(
    lambda x: hash(re.sub(r'(.{2})(?!$)','\\1 ', x.replace(' ', '') ), key)))

anon_data.head()

# %%
# Create a reference table between NIN and respective hashed NIN
reference_table = pd.DataFrame()
reference_table['Hashed.NIN'] = anon_data['Sample.ID']
reference_table['Salt'] = salts
reference_table['Key'] = key.hex()
reference_table['NIN'] = original_data['national_insurance_number']

reference_table.head()

# %% [markdown]
# ## Banding

# %% [markdown]
# ### Date of birth and education level

# %%
# Birth years are extracted
birthyears = pd.DatetimeIndex(original_data['birthdate']).year

# Banding the birth years into 20-year intervals
anon_data['Birthyear'] = pd.cut(birthyears, np.arange(birthyears.min(), birthyears.max()+20, 20), right=False)

anon_data.head()

# %% [markdown]
# ### Full postcode to countries within the UK

# %%
# Assign UK country derived from postcode by comparing to the postcode_dictionary reference table
anon_data['Postcode'] = original_data['postcode'].apply(lambda x: re.search('[a-zA-Z]*', x).group(0))
anon_data = pd.merge(anon_data, postcode_dictionary, on='Postcode', how='left')
anon_data = anon_data.rename(columns={'Region': 'UK.Country'})

anon_data.head()

# %% [markdown]
# ### Education level and country of birth

# %%
# Assign education level as banded education level
anon_data['Education.Level'] = original_data['education_level'].map(lambda x: "Higher" if x in ["bachelor", "masters", "phD"] else "BasicOther")

# Assign hemisphere of birth depending on country of birth
anon_data['Location.of.Birth'] = original_data['country_of_birth'].apply(lambda x: country_to_hemisphere(x))

anon_data.head()

# %% [markdown]
# ## Data perturbation (adding Gaussian noise)

# %%
# Add gaussian noise to weight, height, countries visited, average number of drinks in alcohol units per week and average cigrettes smoked per week.
weight_noise = np.random.normal(0,1,1000)*5
anon_data['Weight'] = round(original_data['weight']+weight_noise, 1)

height_noise = np.random.normal(0,1,1000)/5
anon_data['Height'] = round(original_data['height']+height_noise, 2)

countries_noise = np.random.normal(0,1,1000)*5
anon_data['Countries.Visited'] = round(original_data['n_countries_visited']+countries_noise)

alcohol_noise = np.random.normal(0,1,1000)
anon_data['Avg.Alcohol'] = round(original_data['avg_n_drinks_per_week']+alcohol_noise, 1)

smoking_noise = np.random.normal(0,1,1000)*20
anon_data['Avg.Cigarettes'] = round(original_data['avg_n_cigret_per_week']+smoking_noise)

anon_data.head()

# %% [markdown]
# # Calculating K-anonymity using quasi-identifiers

# %% [markdown]
# The following code groups the quasi-identifiers specified, calculates the k-value, and returns a count of the "unique" rows.

# %%
# Checking counts of quasi-identifiers permutations
df_count = anon_data.groupby(['Gender', 'Birthyear', 'Location.of.Birth', 
                            'UK.Country', 'Education.Level']).size().reset_index(name = 'Count') 
counts_exceeding_0 = df_count.sort_values("Count")[df_count.sort_values("Count")['Count'] > 0].reset_index()

# Calculate the k-value and the number of unique quasi-identifier permutations
print("The anonymised dataset is " + str(counts_exceeding_0['Count'][0]) + "-anonymous; there are " +
      str(len(df_count[df_count['Count']==1])) + " unique quasi-identifier permutations.\n")

# Printing the final grouped output 
print("Least-frequent quasi-identifier permutations, in ascending order:")
counts_exceeding_0.head()

# %% [markdown]
# # Viewing and saving the anonymised dataset

# %%
# Re-order columns
anon_data = anon_data[['Sample.ID', 'Gender', 'Birthyear', 'Location.of.Birth', 'UK.Country', 'Weight', 
                        'Height', 'Education.Level', 'Avg.Alcohol', 'Avg.Cigarettes', 'Countries.Visited', 'CC.Status']]

# View the anonymised dataset
anon_data.head()

# %% [markdown]
# ## Creating CSV files for the anonymised data and the reference table

# %%
# Output the files into .csv format
output_name = "anon_dataset"
anon_data.to_csv(output_name + ".csv", sep=",", index=None)

reference_table.to_csv("reference_table.csv", sep=",", index=None)

# %% [markdown]
# ## Encrypting the dataset

# %%
# Encrypt csv and delete original file
encrypt(output_name + ".csv", output_name + "_encrypted.csv", "key.key")
os.remove(output_name + ".csv")
