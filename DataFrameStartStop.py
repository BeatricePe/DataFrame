# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 10:23:26 2018

@author: Bea
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 14:04:45 2018

@author: Bea
"""
import pandas as pd

#function that reads the data frames and that converts the column of the time in ms
def ReadingAndConversion (file_in, sepfile, column_time):
    Dataframe = pd.read_csv (file_in, sep = sepfile)
    Dataframe.loc[:, column_time] = Dataframe[column_time] * 1000 
    return Dataframe

#function that takes a DataFrame and gives a tupla of Beh and Frames 
def BehaviorAndFramesCounter(Data, ColumnTime, ColumnBeh, ColumnEvent, FrameSecConverter, StrPlace, StrEvent, num):
    count = 0
    countPlace = 0
    j = 1
    k = 1
    FrameCount = 0.00
    ListBeh = []
    ListFrame = []
    ListPlace = []
    ListFramePlace = []
    for i in range (len (Data)):
        if Data[ColumnBeh][i] != StrPlace:
            if Data[ColumnEvent][i] != StrEvent:
                while Data [ColumnBeh][i] != Data [ColumnBeh][j] or Data[ColumnEvent][j] != StrEvent:
                    j = j+1
                while count < Data [ColumnTime][j]:
                    ListBeh.append(Data[ColumnBeh][i])
                    count = count + FrameSecConverter
                    FrameCount = FrameCount + 1
                    ListFrame.append (FrameCount)
            else: continue
        else:   
            while Data [ColumnBeh][i] != Data [ColumnBeh][k] or Data[ColumnEvent][k] != StrEvent:
                k = k+1
            while countPlace < Data [ColumnTime][k]:
                ListPlace.append(Data[ColumnBeh][i])
                countPlace = countPlace + FrameSecConverter
                FramePlaceCount = FrameCount + 1
                ListFramePlace.append (FramePlaceCount)
    return (ListBeh, ListFrame, ListPlace, ListFramePlace)

#function that does a DataFrame with Beh and Frames       
def BehAndFrames (Beh, Frames, Place, ColumnLabel1, ColumnLabel2, ColumnLabel3):
    Data=pd.DataFrame({ColumnLabel1:Frames, ColumnLabel2:Beh, ColumnLabel3:Place})
    return Data

#function that does a DataFrames with all Means        
def MeanSelection (file_in, ColumnLabel, SepFile ):
    Data=pd.read_csv (file_in, sep = SepFile)
    lista=[]
    for el in Data.columns:
        if el[0:len(ColumnLabel)] == ColumnLabel:
            lista.append(el)
    Data=Data[lista]
    return (Data)


DataFrameMeans = MeanSelection(r"C:\Users\Bea\Desktop\lab\Programmi\ResultsA10T.csv", 'Mean',',')
DataIn = ReadingAndConversion (r"C:\Users\Bea\Desktop\lab\Programmi\Vmh1A10.csv",';', 'Time_Relative_sf')
ListCountBeh = BehaviorAndFramesCounter(DataIn, 'Time_Relative_sf', 'Behavior', 'Event_Type', 50, 'Home', 'State stop',2)
DataFrameBehAndFrames = BehAndFrames(ListCountBeh[0], ListCountBeh[1], ListCountBeh[2],'Frames', 'Beh', 'Place')
DFBehAndFramesCut = DataFrameBehAndFrames[:len(DataFrameMeans)]#cut the shorter DataFrame and join the DataFrame of Beh and Means
DataFrameOut = DFBehAndFramesCut.join(DataFrameMeans)

