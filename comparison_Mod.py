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

"""
Function that selects different beh and gives a tupla with beh and occurence of each beh
"""
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
    return lista

"""
Function that creates a rectangle for each beh in behList; the each rectangle's color changes with the beh
"""
def SelectableColors(behList, ColorList, minimum, maximum, dic):
    pos = 0
    listaRect = []
    for el in behList:
        p1 = (pos, minimum)
        beh = el[1]
        width = el[0]
        pos = width + pos
        if beh in dic.keys():
            rect = patches.Rectangle (p1, width, maximum*5, facecolor = dic.get(beh))
        else:
            for col in ColorList:
                print(str(ColorList.index(col)) + '  ' + col)
            colorIndex = int(input('insert the color number for ' + beh + ':'))
            dic.update ({beh: ColorList[colorIndex]})
            rect = patches.Rectangle(p1, width, maximum*5, facecolor=ColorList[colorIndex])
            ColorList.remove(ColorList[colorIndex])
        listaRect.append(rect)
    return (listaRect, dic)

"""
Function that returns a list of n colors that can be selected to do the rectangles 
"""
def GenColorList (n):
    ColorList = []
    for name, cod in matplotlib.colors.cnames.items(): 
        ColorList.append(name)
        shuffle(ColorList)
    return ColorList [0:n]
        
"""
Function that makes graphs
"""
def Graphing (listaColumns, lista_beh, ListColor):
    count = 0
    dictBehColor = {}
    Axes = []
    for el in listaColumns:
        plt.subplot (len(listaColumns), 1, count+1)
        if dictBehColor == {}:
            fig = plt.figure(figsize=(100,75))
        Axes.append(fig.add_subplot(len(listaColumns), 1, count+1))
        Axes[count].plot(el,'k',linewidth=5)
        fig.suptitle('Comparison', fontsize=100)
        plt.xlabel('Frames',  fontsize=50)
        plt.ylabel('Single Neuron Activity',  fontsize=50)
        plt.tick_params(labelsize=50)
        tuplaRectColors = SelectableColors(lista_beh, ListColor, el.max(), el.min(), dictBehColor)
        dictBehColor = tuplaRectColors[1]
        RectList = tuplaRectColors[0]
        for rect in RectList:
            Axes[count].add_patch(rect)
        count += 1    
    j = 1
    for beh in dictBehColor.keys():
        legend_patch = patches.Patch(color = dictBehColor.get(beh), label = beh)
        legenda = plt.legend(handles = [legend_patch], loc=1, bbox_to_anchor=(1.11 ,0.5*j),  prop={'size':60})
        if j != len(dictBehColor.keys()):
            j+=1
            Axes[len(Axes) -1] = plt.gca().add_artist(legenda)
            #aggiunge di volta in volta la legenda creata sopra al grafico
        else:
            plt.show() 
            fig.savefig('m.png',transparent=True)

''' 
Import Data
'''        
Data_beh=pd.read_csv(r"C:\Users\Bea\Desktop\lab\Programmi\Vmh4SF21beh (7).csv", sep=';')
x = Data_beh.loc[ : ,'Frames']
beh = Data_beh.loc[:,'Beh'] 
lista_beh = beh_select(beh)
ListColor = GenColorList(50)
listMean = []  
listSeries = []
for Mean in Data_beh:
    listMean.append(Mean)
while True:
    for el in listMean:
        print (str(listMean.index(el)+1)+' ' + el)
    val = int (input('Insert Mean Number, select 0 when you have finished!'))
    if val == 0:
        break
    neuron = listMean[val-1]
    listMean.remove (neuron)
    listSeries.append(Data_beh.loc[:,neuron])
Graphing (listSeries, lista_beh, ListColor)
    
### MIGLIORARE LA LEGENDA!!!!!!