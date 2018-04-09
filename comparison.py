# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 18:34:00 2018

@author: Bea

"""
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import shuffle

#function that selects different beh and gives a tupla with beh and occurence of each beh
def beh_select(Series):
    occurence=0
    lista = []
    for i in range (len(Series)):
        if i == len(Series)-1:
            occurence=occurence+1
            tupla=(occurence,Series.iloc[i])
            lista.append(tupla)
            
        elif Series.iloc[i] == Series.iloc[i+1]:
             occurence=occurence+1
             
        else:
            occurence=occurence+1
            tupla = (occurence,Series.iloc[i])
            lista.append(tupla)
            occurence=0
    return(lista)

#function that creates a colored rectangle; the color changes with the beh
def ret (behList, colorList,serie):
    maximum=serie.max()
    mi=serie.min()
    dic = { }
    pos = 0
    colorIndex = 0
    lista_ret = []
    for i in range (len(behList)):
        p1 = (pos, mi)
        beh = behList[i][1]
        width = behList[i][0]
        pos = width + pos
        if beh in dic.keys():
            rect = patches.Rectangle(p1, width , maximum*5, facecolor = dic.get(beh))
        else:
            rect = patches.Rectangle(p1,width,maximum*5,facecolor=colorList[colorIndex])
            dic.update({beh : colorList[colorIndex]})
            colorIndex += 1
        lista_ret.append(rect)
    return (lista_ret, dic)

#IMPORT DATA
Data_beh=pd.read_csv(r"C:\Users\Bea\Desktop\lab\Programmi\Vmh4M20dist.csv", sep=';')
x=Data_beh.loc[ : ,'Frames']
beh=Data_beh.loc[:,'Beh']    
y=Data_beh.loc[:,'Mean(3)']
y2 = Data_beh.loc [:,'Mean(2)']
maxim= y.max() 
minim= y.min()
lista_beh=beh_select(beh)
ListColor=[]
for name, cod in matplotlib.colors.cnames.items(): 
    ListColor.append(name)
shuffle(ListColor)
dictBehColor = ret(lista_beh, ListColor,y)[1]

#GRAPH
plt.subplot(2,1,1)
fig = plt.figure(figsize=(100,75))
ax = fig.add_subplot(2,1,1)
ax.plot(y,'k',linewidth=5)
fig.suptitle('Comparison', fontsize=100)
plt.xlabel('Frames',  fontsize=50)
plt.ylabel('Single Neuron Activity',  fontsize=50)
plt.tick_params(labelsize=50)
RectList = ret(lista_beh, ListColor,y)[0] 
for rect in RectList:
    ax.add_patch(rect)

plt.subplot(2,1,2) 
ax2 = fig.add_subplot(2,1,2) 
ax2.plot(y2,'k',linewidth=5)
ax2.set_xlabel('Frames', fontsize=50)
ax2.set_ylabel('Single Neuron Activity', fontsize=50)
plt.tick_params(labelsize=50) #per cambiare la dimensione dei numeri sugli assi
RectList2 = ret(lista_beh, ListColor,y2)[0] 
for rect2 in RectList2:
    ax2.add_patch(rect2) #sto aggiungendo patches all'immagine
j = 1
for el2 in dictBehColor.keys():
    legend_patch2 = patches.Patch(color = dictBehColor.get(el2), label = el2)
    legenda2 = plt.legend(handles = [legend_patch2], loc=1, bbox_to_anchor=(1.1,0.1*j),  prop={'size':60})
   
    if j != len(dictBehColor.keys()):
        j+=1
        ax2 = plt.gca().add_artist(legenda2)
        #aggiunge di volta in volta la legenda creata sopra al grafico
    else:
      plt.show() 

fig.savefig('image.png')
