import os, logging
import math
import hashlib
import country_converter as coco
import pycountry_convert as pc
#import pgeocode
from geopy.geocoders import Nominatim



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
    hash = hashlib.sha256(salt + to_hash.encode()).hexdigest()
    return to_hash, hash, salt.hex()