# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 14:04:45 2018

@author: Bea
"""
import pandas as pd
#I take the start of each beh and until the counter is minor than the time of start of the successive beh I add 50 to the counter.

#function that reads the data frames and that converts the column of the time in ms
def ReadingAndConversion (file_in, sepfile, column_time):
    Dataframe = pd.read_csv (file_in, sep = sepfile)
    Dataframe.loc[:, 'Time_Relative_sf'] = Dataframe['Time_Relative_sf'] * 1000 
    return Dataframe

#function that takes a DataFrame and gives a tupla of Beh and Frames 
def BehaviorAndFramesCounter(Data, ColumnTime, ColumnBeh, ColumnEvent, FrameSecConverter, StrPlace, StrEvent, num):
    count = 0
    FrameCount = 0.00
    ListBeh = []
    ListFrame = []
    for j in range (len (Data)):
        if Data[ColumnBeh][j] != StrPlace and Data[ColumnEvent][j] != StrEvent: # I want select only the start and the beh
            while count < Data [ColumnTime][j+num]: # I compare the time of each start with the successive start 
                ListBeh.append(Data[ColumnBeh][j])
                count = count + FrameSecConverter
                FrameCount = FrameCount + 1
                ListFrame.append (FrameCount)
    return (ListBeh, ListFrame)

#function that does a DataFrame with Beh and Frames       
def BehAndFrames (Beh, Frames, ColumnLabel1, ColumnLabel2):
    Data=pd.DataFrame({ColumnLabel1:Frames, ColumnLabel2:Beh})
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
DataFrameBehAndFrames = BehAndFrames(ListCountBeh[0], ListCountBeh[1], 'Frames', 'Beh')
DFBehAndFramesCut = DataFrameBehAndFrames[:len(DataFrameMeans)]#cut the shorter DataFrame and join the DataFrame of Beh and Means
DataFrameOut = DFBehAndFramesCut.join(DataFrameMeans)
    
        
