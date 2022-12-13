import os, logging
import math
import hashlib
import country_converter as coco
import pycountry_convert as pc
#import pgeocode
from geopy.geocoders import Nominatim
import cryptography
from cryptography.fernet import Fernet



#
# Helper functions
#

# Convert country to continent
def parse_country(country_name):
    country = coco.convert(country_name, to='ISO3')
    if(country_name == 'Netherlands Antilles'): # Hard-coded fix for the single unmatched country
        country = 'Netherlands'
    return country


# Convert country to continent
def country_to_continent(country_name):
    continent = coco.convert(country_name, to='Continent')
    if(country_name == 'Netherlands Antilles'): # Hard-coded fix for the single unmatched country
        continent = 'Europe'
    return 'OceaniaAntarct' if continent in ['Antarctica', 'Oceania'] else continent


def country_to_continent2(country_name):
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
    return continent_name

# SHA hash using key and salt
def hash(key, to_hash):
    salt = os.urandom(16)
    h = hashlib.sha256()
    h.update(key)
    h.update(salt)
    h.update(to_hash.encode())
    return to_hash, h.hexdigest(), salt.hex()

# Encrypt and save as encrypted file; specify file to encrypt, encrypted file destination, and destination key location
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

# Decrypt and save as plaintext file; specify file to decrypt, decrypted file destination, and key location
def decrypt(to_decrypt, file_destination, key_location):
    with open(key_location, 'rb') as f:
        key = f.read()
        
    fernet = Fernet(key)

    with open(to_decrypt, 'rb') as f:
        encrypted = f.read()

    decrypted = fernet.decrypt(encrypted)
    
    with open(file_destination, 'wb') as f:
        f.write(decrypted)
