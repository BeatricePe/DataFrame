# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 11:40:31 2018

@author: Bea
"""

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import shuffle

'''
function that selects different beh and gives a tupla with beh and occurence of each beh
'''
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

'''
function that creates a colored rectangle; the color changes with the beh
'''
def ret (behList, colorList, minimum, maximum):
#    maximum=serie.max()
#    mi=serie.min()
    dic = { }
    pos = 0
    colorIndex = 0
    lista_ret = []
    for i in range (len(behList)):
        p1 = (pos, -10)
        beh = behList[i][1]
        width = behList[i][0]
        pos = width + pos
        if beh in dic.keys():
            rect = patches.Rectangle(p1, width ,20, facecolor = dic.get(beh))
        else:
            rect = patches.Rectangle(p1,width,20,facecolor=colorList[colorIndex])
            dic.update({beh : colorList[colorIndex]})
            colorIndex += 1
        lista_ret.append(rect)
    return (lista_ret, dic)

"""
Function that makes graphs
"""
def Graphing (listaColumns, lista_beh, ListColor, fileName):
    count = 0
    p = 0
    dictBehColor = {}
    Axes = []
    for el in listaColumns:
        plt.subplot (len(listaColumns), 1, count+1)
        if dictBehColor == {}:
            fig = plt.figure(figsize=(150,100))
        Axes.append(fig.add_subplot(len(listaColumns), 1, count+1))
        Axes[count].plot(el,'k',linewidth=5)
        fig.suptitle('Comparison', fontsize=100)
        plt.ylabel(el.name, fontsize = 50)
        plt.ylim(0,3)
        plt.tick_params(labelsize=50)
        tuplaRectColors = ret(lista_beh, ListColor, el.max(), el.min())
        dictBehColor = tuplaRectColors[1]
        RectList = tuplaRectColors[0]
        for rect in RectList:
            Axes[count].add_patch(rect)
        count += 1
        p = p + 0.05
    plt.xlabel('Frames',  fontsize=50)
    j = 1
    for beh in dictBehColor.keys():
        legend_patch = patches.Patch(color = dictBehColor.get(beh), label = beh)
        legenda = plt.legend(handles = [legend_patch], loc=1, bbox_to_anchor=(1.1 ,p*j),  prop={'size':30})
        if j != len(dictBehColor.keys()):
            j+=1
            Axes[len(Axes) -1] = plt.gca().add_artist(legenda)
            #aggiunge di volta in volta la legenda creata sopra al grafico
        else:
            plt.show() 
            fig.savefig(fileName,transparent=True)

'''
import Data
'''
sheetName = 'm23units_Df02pdef'
Data=pd.read_excel(r"C:\Users\Bea\Desktop\m23\m23units_Df02pdef.xlsx")
frames=Data.loc[ : ,'Frames']
beh=Data.loc[:,'Beh']    
Mean = Data.drop ('Beh',1)
Mean =Mean.drop('Frames',1)
lstmean = []
for means in Mean :
    m = Mean[means].mean()
    lstmean.append(m)

count = 0
for label in Mean:
       Mean[label]  = (Mean[label] - lstmean[count])/lstmean[count]
       count = count + 1
        
    

serieList = []
for serie in Mean:
    serieList.append(Mean[serie])
lista_beh=beh_select(beh)
ListColor=[]

for name, cod in matplotlib.colors.cnames.items(): #creo la lista di colori
    ListColor.append(name)
shuffle(ListColor)

Graphing (serieList, lista_beh, ListColor, sheetName)