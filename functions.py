#
# Helper functions
#

import pycountry_convert as pc

# Convert country to continent
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
    return continent_name