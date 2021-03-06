import pandas as pd
import config as cfg
import requests
import pymysql
import numpy as np
import csv


api_key = cfg.settings["census"]["key"]

connection = cfg.get_db_connection()

try:
    with connection.cursor() as cursor:
        # Read a single record
        cursor.execute("SELECT Geoid FROM community_units WHERE community_id=1")
        rows = cursor.fetchall()
        print(rows)
finally:
    connection.close()

list_of_bgs=[]
for i in rows:
    i = ''.join(filter(lambda x: x in '.0123456789', str(i)))
    i = str(i)
    list_of_bgs.append(i)


# list_of_bgs = ['371830501001','371830507001','371830507002']
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


        # Variables of interest:
        # - P0050001-P00500018: Race/Ethnicity
        # - H0100001-H0100004: Population in Owned v. Rented units

#asnumeric
census_data['P0050001']=census_data['P0050001'].astype(str).astype(int)
census_data['P0050002']=census_data['P0050002'].astype(str).astype(int)
census_data['P0050003']=census_data['P0050003'].astype(str).astype(int)
census_data['P0050004']=census_data['P0050004'].astype(str).astype(int)
census_data['P0050005']=census_data['P0050005'].astype(str).astype(int)
census_data['P0050006']=census_data['P0050006'].astype(str).astype(int)
census_data['P0050007']=census_data['P0050007'].astype(str).astype(int)
census_data['P0050008']=census_data['P0050008'].astype(str).astype(int)
census_data['P0050009']=census_data['P0050009'].astype(str).astype(int)
census_data['P0050010']=census_data['P0050010'].astype(str).astype(int)
census_data['P0050011']=census_data['P0050011'].astype(str).astype(int)
census_data['P0050012']=census_data['P0050012'].astype(str).astype(int)
census_data['P0050013']=census_data['P0050013'].astype(str).astype(int)
census_data['P0050014']=census_data['P0050014'].astype(str).astype(int)
census_data['P0050015']=census_data['P0050015'].astype(str).astype(int)
census_data['P0050016']=census_data['P0050016'].astype(str).astype(int)
census_data['P0050017']=census_data['P0050017'].astype(str).astype(int)
census_data['H0110001']=census_data['H0110001'].astype(str).astype(int)
census_data['H0110002']=census_data['H0110002'].astype(str).astype(int)
census_data['H0110003']=census_data['H0110003'].astype(str).astype(int)
census_data['H0110004']=census_data['H0110004'].astype(str).astype(int)
census_data['Hispanic']=census_data['P0050001']-census_data['P0050002']

#calcs
pct_white_non_hispanic=census_data['P0050003'].sum()/census_data['P0050001'].sum()
pct_black_non_hispanic=census_data['P0050004'].sum()/census_data['P0050001'].sum()
pct_hispanic=census_data['Hispanic'].sum()/census_data['P0050001'].sum()
pct_AINI_non_hispanic=census_data['P0050005'].sum()/census_data['P0050001'].sum()
pct_asian_non_hispanic=census_data['P0050006'].sum()/census_data['P0050001'].sum()
pct_NHPI_non_hispanic=census_data['P0050007'].sum()/census_data['P0050001'].sum()
pct_other_non_hispanic=census_data['P0050008'].sum()/census_data['P0050001'].sum()
pct_multi_non_hispanic=census_data['P0050009'].sum()/census_data['P0050001'].sum()
pct_renters=census_data['H0110004'].sum()/census_data['H0110001'].sum()

    
d = {"race:pct_white_non_hispanic":pct_white_non_hispanic, "race:pct_black_non_hispanic": pct_black_non_hispanic, "race:pct_AINI_non_hispanic": pct_AINI_non_hispanic, "race:pct_asian_non_hispanic": pct_asian_non_hispanic,"race:pct_hispanic":pct_hispanic, "race:pct_other_non_hispanic":pct_other_non_hispanic, "race:pct_multi_non_hispanic":pct_multi_non_hispanic, "housing:pct_renters":pct_renters }

(pd.DataFrame.from_dict(data=d, orient='index')
   .to_csv('dict_file.csv', header=False))