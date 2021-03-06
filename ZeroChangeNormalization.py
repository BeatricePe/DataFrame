# -*- coding: utf-8 -*-
"""
Created on Wed May  2 14:05:11 2018

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

'''
Function that selects a chosen number of elements before and after a chosen action
'''
def SelectionElement (num, action, serieBeh, serieMeans):
    listaIndex = []
    for i in range (len(serieBeh)):
        if serieBeh[i] == action:
            if serieBeh [i-1] != action:
                if num <= i-1:
                    for k in range (-num,0):
                        listaIndex.append((i-15)+k)
                    for l in range (1,num+1):
                        listaIndex.append((i-15)+l)
                    break
                else: print ('You have to choose a number smaller than ' + str(i) + '!')
        else: continue
    serieMeans = serieMeans.ix[listaIndex]
    serieBeh = serieBeh.ix[listaIndex]
    serieMeans.index = range(-num,num)
    return (serieMeans,serieBeh,listaIndex)
Beh = File.loc [:, 'Beh']
Means = File.loc [:,'Mean(1)': 'Mean(38)']
MeansS,BehS,Index = SelectionElement(30,'defense action', Beh, Means)

'''
Function that creates two dataframes that contain the activity before and the activity after the chosen beh
'''
def DataFrameAandB (serieM):
    serieMT = serieM.transpose()
    serieB = pd.DataFrame ()
    serieA = pd.DataFrame ()
    for i, row in serieMT.iterrows():
        serieB = serieB.append( serieMT.loc [i,-len(serieMT.transpose())/2: -1])
        serieA = serieA.append (serieMT.loc [i, 0: len(serieMT.transpose())]/2)
    return (serieB, serieA)
meanTupla = DataFrameAandB (MeansS)
meanBefore = meanTupla[0]
meanAfter = meanTupla[1]
Data = meanBefore.join(meanAfter)

'''
Function for normalization
'''
def Normalization (dfA, dfB):
    for index, row in dfB.iterrows():
        m = dfB.loc[index,:].mean()
        dfA.loc[index, :] =  dfA.loc[index, :]/m
        dfB.loc[index, :] =  dfB.loc[index, :]/m        
    return (dfA, dfB)
DataA, DataB= Normalization (meanAfter, meanBefore)
Data = DataB.join(DataA)
Data = Data.drop ('Mean(4)',0)
Data = Data.drop ('Mean(6)',0)
Data = Data.drop ('Mean(8)',0)
Data = Data.drop ('Mean(28)',0)
Data = Data.drop ('Mean(2)',0)
'''
Kmeans and HM
'''
km = KMeans(n_clusters=3, init='k-means++', n_init=20)
km.fit(Data)
x = km.fit_predict(Data)
Data['Cluster'] = x
Data = Data.sort_values(by=['Cluster'])
df2 = Data.drop ('Cluster',1)
fig, ax = plt.subplots(figsize=(20,10)) 
#ax.vlines([50],0,1, transform=ax.get_xaxis_transform(), colors='k')   
ax.hlines([30],0,1, transform=ax.get_yaxis_transform(), colors='r')   
#ax.hlines([34],0,1, transform=ax.get_yaxis_transform(), colors='k')   
   
#df2 = df2.drop ('Mean(11)',0)
#df2 = df2.drop ('Mean(2)', 0)
#df2 = df2.drop ('Mean(10)',0)
#df2 = df2.drop ('Mean(29)',0)
#df2 = df2.drop ('Mean(32)',0)
#df2 = df2.drop ('Mean(36)',0)
#df2 = df2.drop ('Mean(17)',0) 
sns.heatmap(df2,annot = False, xticklabels=1, yticklabels = 1,cmap="BuPu",)