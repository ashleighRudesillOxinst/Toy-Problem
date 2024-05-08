# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:59:54 2024

@author: Ashleigh.Rudesill
"""

#import libraries
import pandas as pd
#import plotly.express as px
#import plotly.graph_objects as go
#import plotly.io as pio
#pio.renderers.default='browser'

#import sklearn
#import sklearn.cluster as cluster
#import sklearn.metrics as metrics

#import numpy as np


#import state functions
from us_state_abbrev import abbrevToState, checkIfState, abbrevToStateDash

#import general dataframe and convert from CSV
df = pd.read_csv('C:/Users/ashleigh.rudesill/Downloads/aqidataset.csv')
#import lq dataframe
df2 = pd.read_csv('C:/Users/ashleigh.rudesill/Downloads/2023.q1-q3 31-33 NAICS 31-33 Manufacturing.csv', usecols=[0,8,9,14,15,16,22,23,24,25,26])

''' dataframe column names for reference
# =============================================================================
# df1 column names:
#     (null)    Date    Overall AQI Value    Main Pollutant    Site Name (of Overall AQI)    Site ID (of Overall AQI)    
#     Source (of Overall AQI)    Ozone    PM25    CO    PM10    NO2    AQI category    city    state
# =============================================================================


# ========================================================
# df2 column names:

#     area_fips    city    state    month1_emplvl    month2_emplvl    month3_emplvl    lq_qtrly_estabs_cout
#     lq_month1_emplvl    lq_month2_emplvl    lq_month3_emplvl   lq_total_qtrly_wages
# ========================================================
'''

#change column names and remove any statewide or improperly formatted data
df2 = df2.rename(columns={'area_title': 'city','own_title':'state'})
df2 = df2[df2['city'].str.contains(',') == True]

#separate area into city and state(s)
df3 = df2['city'].str.split(", ", expand=True)
df3.columns = ['city','state']
df2.loc[:,['city','state']]=df3[['city','state']]

#cleans states ending in MSA
df2['state'] = df2['state'].map(lambda x: x.rstrip(' MSA'))

#cleans states that are still abbreviated
df2['state'] = df2['state'].apply(lambda x: abbrevToStateDash(x) if '-' in x else x)
df2['state'] = df2['state'].apply(lambda x: abbrevToState(x) if len(x)<4 else x)

#remove null states
df2 = df2[df2['state'].notnull()]


#create dfs for valid measurements of Ozone, PM25, and both
cleanOzone = df[pd.to_numeric(df['Ozone'], errors='coerce').notnull()]
cleanPM25 = df[pd.to_numeric(df['PM25'], errors='coerce').notnull()]

#removes null ozone and pm25 values
cleanOzPM25 = cleanOzone#[pd.to_numeric(cleanOzone['PM25'], errors='coerce').notnull()]
cleanOzPM25['Ozone'] = cleanOzPM25.Ozone.apply(pd.to_numeric, errors = 'coerce')
cleanOzPM25['PM25'] = cleanOzPM25.PM25.apply(pd.to_numeric, errors = 'coerce')


#define a function to get the city and state from first dataframe
def getOgData(row):
    state = abbrevToState(cleanOzPM25.iloc[row,14]).strip().lower()
    city = cleanOzPM25.iloc[row,13].strip().lower()
    return [state,city]

def confirmBoth(city,state):
    tempDf = df2[df2['state'].str.lower().str.contains(str(state))]
    try:
        
        dfLen = len(tempDf)
        retVal = False
        for index,row in tempDf.iterrows():
            if( city in (row['city'].lower())):
                
                ''' add together data and add plus one to the count so it can be divided at the end'''
            #if(tempDf[i][1].str.lower().str.contains(city)==True):
        #        i = dfLen+1
        retVal = True
    except:
        retVal = False
    return retVal

x=getOgData(600)
#print(confirmBoth(x[1], x[0]))

# print(df2.state)
y = confirmBoth('dallas','texas')


#pick a state and project out a map with pollution levels by county
#short couple hundred word report on what ive done by firday
