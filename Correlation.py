# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 11:34:04 2018

@author: Bea
"""

from  sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import pandas as pd
import numpy as np; np.random.seed(0)
import seaborn.apionly as sns
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr   

def ReadingAndColumnSelector (DataIn, sepFile):
    Data = pd.read_csv (DataIn, sep =sepFile)
    return Data
File = ReadingAndColumnSelector (r"C:\Users\Bea\Desktop\lab\Programmi\Vmh4SF21beh (7).csv", ';')
Beh = File.loc [:, 'Beh']
Means = File.loc [:,'Mean(1)': 'Mean(38)']
Means2 = File.loc [:,'Mean(1)': 'Mean(38)']
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
Means2 = Means2.ix[listaIndex]
Means2.index = range (-a,a)

''' 
Heat Map for select neurons that change in significant way 
'''
fig, ax = plt.subplots(figsize=(10,20)) 
ax.vlines([49+0.5],0,1, transform=ax.get_xaxis_transform(), colors='k')        
sns.heatmap(Means.transpose(),annot = False, xticklabels=1)

'''
Correlation between mean1,mean32,mean13,mean4 and all others neurons.
Save only neurons that have high positive correlation
Select and graphs only neurons that are present more than 1 time
'''
listMean = ('Mean(13)','Mean(32)','Mean(4)')
listCorr = []
for el in listMean:
    for column in Means:
        if column != el:
            p = Means[el].corr(Means[column])
            tupla = (p.round(1), column)
            listCorr.append(tupla)
highpositivecorr = []     
highpositiveMean = []       
for i in range (len(listCorr)):
    if (listCorr[i][0]) > 0.8:
       highpositivecorr.append(listCorr[i])
highpositivecorr = sorted(highpositivecorr, reverse=True)
neurons =[]
for j in  range(len( highpositivecorr)):
   if  len(set(highpositivecorr[j][1])) != len(highpositivecorr):
       neurons.append(highpositivecorr[j][1])
from collections import Counter
NeuronsCorreleted = []
cnt = Counter(neurons)
for el,k in cnt.items():
    if k > 1:
        NeuronsCorreleted.append(el)
for label in Means:
    if label in NeuronsCorreleted:
        continue
    else: Means = Means.drop(label,axis = 1)

''' 
Do the same thing with negative correlation
''' 
'''
Correlation between mean31,mean32,mean13,mean4 and all others neurons.
Save only neurons that have high positive correlation
Select and graphs only neurons that are present more than 1 time
'''
listMean2 = ('Mean(15)','Mean(22)','Mean(20)')
listCorr2 = []
for el in listMean2:
    for column in Means2:
        if column != el:
            p = Means2[el].corr(Means2[column])
            tupla = (p.round(1), column)
            listCorr2.append(tupla)
highpositivecorr2 = []            
for i in range (len(listCorr2)):
    if (listCorr2[i][0]) > 0.7:
       highpositivecorr2.append(listCorr2[i])
neurons2 =[]
for j in  range(len( highpositivecorr2)):
   if  len(set(highpositivecorr2[j][1])) != len(highpositivecorr2):
       neurons2.append(highpositivecorr2[j][1])
from collections import Counter
NeuronsCorreleted2 = []
cnt2 = Counter(neurons2)
for el,k in cnt2.items():
    if k > 1:
        NeuronsCorreleted2.append(el)
for label in Means2:
    if label in NeuronsCorreleted2:
        continue
    else: Means2 = Means2.drop(label,axis = 1)
df = Means.join(Means2)

''' 
Graph  clusters
'''
fig, ax = plt.subplots(figsize=(10,10)) 
ax.vlines([49+0.5],0,1, transform=ax.get_xaxis_transform(), colors='k')   
ax.hlines([12],1,0, transform=ax.get_yaxis_transform(), colors='k')   
     
sns.heatmap(df.transpose(),annot = False, xticklabels=1,cmap="Greens")
       