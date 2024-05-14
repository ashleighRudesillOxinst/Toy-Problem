# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:59:54 2024

@author: Ashleigh.Rudesill
"""

#import libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'

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

#     area_fips    city    state    month1_emplvl    month2_emplvl    month3_emplvl    lq_qtrly_estabs_count
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

unique = cleanOzPM25[['city', 'state']].drop_duplicates().reset_index(drop=True)
uniqueList = unique.values.tolist()

#define a function to get the city and state from first dataframe
def getOgData(row):
    state = abbrevToState(cleanOzPM25.iloc[row,14]).strip().lower()
    city = cleanOzPM25.iloc[row,13].strip().lower()
    return [state,city]

#defines a function that given a city and state name returns if it is in the second dataset, and the average of the numeric columns for that city
def retSecVals(city,state):
    retVal = False
    values = [0, 0, 0, 0, 0, 0, 0, 0]
    means = []
    try:
        tempDf = df2[df2['state'].str.lower().str.contains(str(state.lower()))]
        print(len(tempDf))
        tempDf = tempDf[tempDf['city'].str.lower().str.contains(str(city.lower()))]
        print(len(tempDf))
        print(tempDf['month1_emplvl'].mean())
        valuesString = ['month1_emplvl', 'month2_emplvl', 'month3_emplvl', 'lq_qtrly_estabs_count', 'lq_month1_emplvl', 'lq_month2_emplvl', 'lq_month3_emplvl', 'lq_total_qtrly_wages']
        for values in valuesString:
            means.append(tempDf[values].mean())
        retVal = True
    except:
        means = None
        
    return [retVal, means]
"""  unnecessarily processing heavy
    #try getting average of each numeric column for any/all columns matching the city/state
    try:
        tempDf = df2[df2['state'].str.lower().str.contains(str(state.lower()))]
        valuesString = ['month1_emplvl', 'month2_emplvl', 'month3_emplvl', 'lq_qtrly_estabs_count', 'lq_month1_emplvl', 'lq_month2_emplvl', 'lq_month3_emplvl', 'lq_total_qtrly_wages']
        for index,row in tempDf.iterrows():
            if( city.lower() in (row['city'].lower())):
                retVal = True
                for i in range(len(values)):
                    values[i] = values[i] + row[valuesString[i]]
                valuesNum = valuesNum + 1
                
        for i in range(len(values)):
            values[i] = values[i]/valuesNum
                
        ''' add together data and add plus one to the count so it can be divided at the end'''
            #if(tempDf[i][1].str.lower().str.contains(city)==True):
        #        i = dfLen+1
        retVal = True
    except:
        values
    return [retVal, values]
"""



#define a function that given a city and state name returns the average Ozone and PM25 measurements of all those readings
def retFirstVals(city, stateAbbrev):
    tempDf = cleanOzPM25[cleanOzPM25['state'].str.lower().str.contains(str(stateAbbrev.lower()))]
    tempDf = tempDf[tempDf['city'].str.lower().str.contains(str(city.lower()))]
    values = [tempDf['Ozone'].mean(), tempDf['PM25'].mean()]
    return values


x=getOgData(600)
#print(retSecVals(x[1], x[0]))

# print(df2.state)
y = retSecVals('Dallas','texas')
z = retFirstVals('Dallas','TX')


def newDataFrame(uniqueList):
    totalList = []
    for unique in uniqueList:
        city = unique[0]
        stateAbbrev = unique[1]
        state = abbrevToState(stateAbbrev)
        second = retSecVals(city, state)
        allVals = list
        if(second[0]==True):
            first = retFirstVals(city, stateAbbrev)
            allVals = second[1]
            allVals.append(first[0])
            allVals.append(first[1])
            allVals.append(city)
            allVals.append(state)
            totalList.append(allVals)
    return totalList
"""

def function
does unique-

for all in unique-
get values from first and second dfs
combine into one slice
append to new dataframe



"""
newDfList = newDataFrame(uniqueList)
columns = ['month1_emplvl', 'month2_emplvl', 'month3_emplvl', 'lq_qtrly_estabs_count', 'lq_month1_emplvl', 'lq_month2_emplvl', 
          'lq_month3_emplvl', 'lq_total_qtrly_wages','Ozone', 'PM25','City', 'State']
newDf = pd.DataFrame(newDfList,columns=columns)

newDfOzone = newDf.drop('PM25',axis = 1)
newDfOzone = newDfOzone.dropna()

x = newDfOzone.drop('City',axis=1).drop('State',axis=1).corr()

newDfOzone=newDfOzone.sort_values(['Ozone'])

fig1 = px.scatter(newDfOzone, x = "City", y = newDfOzone.columns[7:9])
pio.show(fig1)
