# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 11:06:01 2018

@author: Bea
"""

import pandas as pd
import ggplot as gp
from plotnine import *
import matplotlib as plt

#function that gives a list with beh and occurences of each beh
def BehSelector(Series):
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

#function that create a dataframe that has the variable that i want graphicate ordered in rows (in this way i can do the subplot with ggplot)
def DataFrameReorganization (Data, sepfile, ColumnLabel, Variable):  
    Df = pd.read_csv (Data, sep = sepfile)
    DfMelt = pd.melt (Df, id_vars = ColumnLabel[0:], value_vars = Variable[0:])
    return (Df, DfMelt)

DataFrame = DataFrameReorganization (r"C:\Users\Bea\Desktop\lab\Programmi\Vmh4SF21beh (6).csv", ';',['Beh','Frames'],['Mean(1)','Mean(4)', 'Mean(19)'])
Beh = BehSelector(DataFrame[0].loc[:,'Beh'])
# I generate a list with beh, start and end and I save this in a dataframe
count=0
lista_start_end=[]
for i in range (len (Beh)):
    tupla_start_end = [count, Beh[i][0]+count, Beh[i][1]]
    count= count + Beh[i][0]
    lista_start_end.append(tupla_start_end)
df=pd.DataFrame()
for j in range (len (lista_start_end)):
    df2 = pd.DataFrame({ "xstart": [lista_start_end[j][0]], "xend": [lista_start_end[j][1]],"place": [lista_start_end[j][2]],'ymin': [-0.05], 'ymax' : [0.05]})
    df=df.append(df2,ignore_index=True)

#graphs
graph = ggplot()+geom_line(DataFrame[1],aes(x='Frames',y='value'))+facet_wrap("variable",ncol=1)
graph2 = graph+geom_rect(df, aes (xmin='xstart',xmax='xend',ymin=-0.12,ymax=0.12,fill='place'),alpha=0.5)
g = graph2.draw()

