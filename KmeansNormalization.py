# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 11:03:34 2018

@author: Bea
"""

from  sklearn.cluster import KMeans
import pandas as pd
import numpy as np; np.random.seed(0)
import seaborn.apionly as sns
import matplotlib.pyplot as plt


def ReadingAndColumnSelector (DataIn, sepFile):
    Data = pd.read_csv (DataIn, sep =sepFile)
    return Data
File = ReadingAndColumnSelector (r"C:\Users\Bea\Desktop\lab\Programmi\Vmh4SF21beh (7).csv", ';')
Beh = File.loc [:, 'Beh']
Means = File.loc [:,'Mean(1)': 'Mean(38)']
index = []
listaIndex = []

'''
Selection of the 50 activity before the first beh and of the 50 activity after the first beh ( the chosen beh is defense action)
'''
a = 50
for i in range (len(Beh)):
    if Beh[i] == 'defense action':
        if Beh [i-1] != 'defense action':
            for k in range (-a,0):
                listaIndex.append(i+k)
            
            for l in range (1,a+1):
                listaIndex.append(i+l)
        break
    else: continue
Means = Means.ix[listaIndex]
Beh = Beh.ix[listaIndex]
Means.index = range(-a,a)

'''
 Creation of two dataframes that contain the activity before and the activity after the chosen beh
'''
MeansT = Means.transpose()
MeansBefore = pd.DataFrame ()
MeansAfter = pd.DataFrame ()
for row,i in MeansT.iterrows():
    MeansBefore = MeansBefore.append( MeansT.loc [row,-a:-1])
    MeansAfter = MeansAfter.append (MeansT.loc [row, 0:a])
    
'''
Normalization: divide the activity of each neuron by the mean activity before the chosen beh
'''
listMean = []
for index, row in MeansBefore.iterrows():
    listMean.append(row.mean())
MeansBefore = MeansBefore.transpose()
MeansAfter = MeansAfter.transpose()
for column in MeansBefore:
    for el in listMean:
        MeansBefore[column] = MeansBefore[column]/el
        MeansAfter[column] = MeansAfter[column]/el
MeansBeforeN = MeansBefore.transpose()
MeansAfterN = MeansAfter.transpose()
df = MeansBeforeN.join(MeansAfterN)

''' 
Kmeans and hm
'''
km = KMeans(n_clusters=2, init='k-means++', n_init=20)
km.fit(df)
x = km.fit_predict(df)
df['Cluster'] = x
df = df.sort_values(by=['Cluster'])
df2 = df.drop ('Cluster',1)
fig, ax = plt.subplots(figsize=(10,10)) 
ax.vlines([49+0.5],0,1, transform=ax.get_xaxis_transform(), colors='k')      
ax.hlines([22],1,0, transform=ax.get_yaxis_transform(), colors='k')   

sns.heatmap(df2,annot = False, xticklabels=1)
    