import pandas as pd
import config as cfg
import requests


api_key = cfg.settings["census"]["key"]

list_of_bgs = ['371830501001','371830507001','371830507002']
#list_of_bgs = ['371830501001']

def pull_census(geoid):
    state = geoid[0:2]
    county = geoid[2:5]
    tract = geoid[5:11]
    blockgroup = geoid[11:]

    url = ("https://api.census.gov/data/2010/sf1?get=NAME,P0050001,P0050002,P0050003,P0050004,P0050005,"+
            "P0050006,P0050007,P0050008,P0050009,P0050010,P0050011,P0050012,P0050013,P0050014,P0050015,"+
            "P0050016,P0050017,H0110001,H0110002,H0110003,H0110004&for=block%20group:"+ blockgroup +
            "&in=state:" + state + "%20county:" + county + "%20tract:" + tract + "&key=" + api_key)
    html = requests.get(url).json()
    bg_data = pd.DataFrame(html, columns=html[0])
    return bg_data[1:]


census_data = pull_census(list_of_bgs[0])

if len(list_of_bgs) > 1:
    for bg in list_of_bgs[1:]:
        next_bg = pull_census(bg)
        census_data = pd.concat([census_data,next_bg])

census_data

# Variables of interest:
    # - P0050001-P00500018: Race/Ethnicity
    # - H0100001-H0100004: Population in Owned v. Rented units
    
