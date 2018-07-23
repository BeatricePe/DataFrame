# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:35:30 2018

@author: Bea
"""
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import shuffle
maximumlist = []
minimumlist = []
listMean = []
path = r'C:\Users\Bea\Desktop\prova' *
for files in os.listdir(r'C:\Users\Bea\Desktop\m23'): *
    fileName = str(files)
    Data=pd.read_excel(r'C:\Users\Bea\Desktop\m23'+'\\'+fileName) *
    fileName = fileName.strip('.xlsx') 
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
    listMean.append(Mean)
    for el in listMean:
        el['Frames'] = frames
        el['Beh'] = beh
        el.to_excel(path +'\\'+ fileName + 'N.xlsx')
       
    Mean = Mean.drop ('Frames',1)
    Mean = Mean.drop ('Beh',1)
   
    for lab in Mean:
        
        maximumlist.append(Mean[lab].max())
        minimumlist.append(Mean[lab].min())
Min = min(minimumlist)
Max = max(maximumlist)

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
function that creates  colored rectangles; the color changes with the beh
'''
def ret (behList, colorList, minimum, maximum):
#    maximum=serie.max()
    dic = {'Avoidance':'green', 'Approach':'orange','Sapp':'yellow' }
    pos = 0
    colorIndex = 0
    lista_ret = []
    for i in range (len(behList)):
        p1 = (pos, minimum)
        beh = behList[i][1]
        width = behList[i][0]
        if beh in dic.keys():
            rect = patches.Rectangle(p1, width , maximum, facecolor = dic.get(beh))
        else:
            rect = patches.Rectangle(p1, width, maximum, facecolor = colorList[colorIndex])
            dic.update({beh : colorList[colorIndex]})
            colorIndex += 1
        pos = width + pos
        lista_ret.append(rect)
    return (lista_ret, dic)

"""
Function that makes graphs
"""
def Graphing (listaColumns, lista_beh, ListColor, fileName, path, mini,maxi):
    count = 0
    p = 0
    dictBehColor = {'Avoidance':'green', 'Approach':'orange','Sapp':'yellow' }
    Axes = []
    c =0
    control = False
    for beh in lista_beh:
        if beh[1] == 0:
            control = True
            break
    for el in listaColumns:
        plt.subplot (len(listaColumns), 1, count+1)
        if c == 0:
            c =1
            fig = plt.figure(figsize=(50,50))
        Axes.append(fig.add_subplot(len(listaColumns), 1, count+1))
        Axes[count].plot(el,'k',linewidth=5)
        fig.suptitle(fileName, fontsize=100)
        plt.ylabel(el.name, fontsize = 50)
        plt.ylim(Min, Max )
        plt.tick_params(labelsize=50)
        if control == True:
            count = count + 1
            continue
        
        tuplaRectColors = ret(lista_beh, ListColor,Min, Max)
        dictBehColor = tuplaRectColors[1]
        RectList = tuplaRectColors[0]
        for rect in RectList:
            Axes[count].add_patch(rect)
        count += 1
        p = p + 0.05
    plt.xlabel('Frames',  fontsize=50)
    if control == True:
#        plt.show() 
        fig.savefig(path + '\\'+fileName, transparent=True)
        fig.savefig(path + '\\'+fileName, transparent=True, format = 'svg')
        fig.savefig(path + '\\'+fileName, transparent=True, format = 'pdf')
        return
        
    j = 1
    for beh in dictBehColor.keys():
        legend_patch = patches.Patch(color = dictBehColor.get(beh), label = beh)
        legenda = plt.legend(handles = [legend_patch], loc=1, bbox_to_anchor=(1.1 ,p*j),  prop={'size':30})
        if j != len(dictBehColor.keys()):
            j+=1
            Axes[len(Axes) -1] = plt.gca().add_artist(legenda)
            #aggiunge di volta in volta la legenda creata sopra al grafico
        else:
#            plt.show() 
            fig.savefig(path + '\\'+fileName, transparent=True)
            fig.savefig(path + '\\'+fileName, transparent=True, format = 'svg')
            fig.savefig(path + '\\'+fileName, transparent=True, format = 'pdf')
#            fig.savefig(path + '\\'+fileName+'.'+'wmf',transparent=True)

'''

'''
def FolderFunction(FolderPath,outputPath,Sep):
    ListColor = []
    for name, cod in matplotlib.colors.cnames.items(): #creo la lista di colori
        ListColor.append(name)
    for files in os.listdir (FolderPath):
        fileName = str(files)
        if fileName[-3:] == 'xls' or fileName[-4:] == 'xlsx':
            Data = pd.read_excel (FolderPath+'\\'+fileName, sep = Sep, sheetname = None)
            fileName = fileName.strip('.xlsx') 
            fileName = fileName.strip('.xls') 
            for sheet in Data.keys():
                serie,beh = fun(Data.get(sheet))
                Graphing(serie,beh,ListColor,fileName+' '+str(sheet),outputPath, Min, Max) 
                
def fun(Data):
    labelList = []
    for label in Data:
        labelList.append(label)
    beh = Data.loc[:, labelList[1]]
    Mean = Data.drop(labelList[0],1)
    Mean = Mean.drop(labelList[1],1)
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
    return (serieList, lista_beh)

FolderFunction(r"C:\Users\Bea\Desktop\m23",r"C:\Users\Bea\Desktop\maria", ';')   *
    
    
            
        
