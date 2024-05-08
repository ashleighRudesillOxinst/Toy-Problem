# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 08:19:24 2024

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

import numpy as np

#import general dataframe and convert from CSV
df = pd.read_csv('C:/Users/ashleigh.rudesill/Downloads/aqidataset.csv')

# =============================================================================
# column names:
#     (null)    Date    Overall AQI Value    Main Pollutant    Site Name (of Overall AQI)    Site ID (of Overall AQI)    
#     Source (of Overall AQI)    Ozone    PM25    CO    PM10    NO2    AQI category    city    state
# =============================================================================

#main pollutant is ozone, followed by pm2.5- others are negligible in comparison
print(df['Main Pollutant'].value_counts())

#df=df.sort_values(['city', 'Ozone'], ascending=[True, True])


#create dfs for valid measurements of Ozone, PM25, and both
cleanOzone = df[pd.to_numeric(df['Ozone'], errors='coerce').notnull()]
cleanPM25 = df[pd.to_numeric(df['PM25'], errors='coerce').notnull()]

cleanOzPM25 = cleanOzone#[pd.to_numeric(cleanOzone['PM25'], errors='coerce').notnull()]
cleanOzPM25['Ozone'] = cleanOzPM25.Ozone.apply(pd.to_numeric, errors = 'coerce')
cleanOzPM25['PM25'] = cleanOzPM25.PM25.apply(pd.to_numeric, errors = 'coerce')

# print(len(cleanOzone))
# print(len(cleanPM25))
# print(len(cleanOzPM25))



#cleanOzPM25Sort = cleanOzPM25.sort_values(['city', 'Ozone'], ascending=[True, True])
print(len(cleanOzPM25))
print(type(cleanOzone['Ozone'].iloc[100]))

fig1 = px.scatter(cleanOzPM25, x = "city", y = "Ozone",color_discrete_sequence=['blue'])

fig1.update_traces(marker=dict(size=8), selector=dict(mode='markers'))

fig2 = px.scatter(cleanOzPM25, x = "city", y = "PM25",color_discrete_sequence=['red'])
fig2.update_traces(marker = dict(symbol="diamond"))

fig = go.Figure(data = fig1.data + fig2.data)
pio.show(fig)


chicago = cleanOzPM25[cleanOzPM25['city'] =='Chicago']
chic1 = px.scatter(chicago, x = 'Date', y = 'Ozone')
chic1.add_trace(go.Scatter( x = chicago['Date'],y= chicago['PM25'], mode='markers'))
#pio.show(chic1)

chicago = chicago.sort_values('Site Name (of Overall AQI)',ascending = True)
chic2Oz = px.scatter(chicago, x = 'Site Name (of Overall AQI)', y = 'Ozone')
chic2PM = px.scatter(chicago, x = 'Site Name (of Overall AQI)', y = 'PM25', color_discrete_sequence=['red'])
chic2PM.update_traces(marker = dict(symbol="diamond"))
chic2 = go.Figure(data = chic2Oz.data+chic2PM.data)
chic2.update_layout(title = go.layout.Title(text = 'Chicago Ozone and PM25 Measurements by Location'), xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text='Locations')))
chic2.update_layout(showlegend=True)
pio.show(chic2)

# chicagoDF = chicago.iloc[:,[0,7]]
# kmeans = cluster.KMeans(n_clusters=3)
# kmeans =kmeans.fit(chicagoDF)
# labels = kmeans.predict(chicagoDF)
# centroids = kmeans.cluster_centers_
# labelsList = labels.tolist()



# for i in range(len(labelsList)):
#     if(labelsList[i]==0):
#         labelsList[i]='red'
#     if(labelsList[i]==1):
#         labelsList[i]='blue'
#     if(labelsList[i]==2):
#         labelsList[i]='red'
        
# print(labelsList)


# print('centroids are',centroids)


chic3 = px.scatter_3d(chicago, x = 'Site Name (of Overall AQI)', y = 'Ozone', z = 'PM25')
pio.show(chic3)
