# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 12:45:17 2023

@author: Danish
"""


import yfinance as yf 
import numpy as np
from stocktrends import Renko

tickers = ['AMZN','GOOG','MSFT']
ochlv = {}
hour_data = {}
renko_data = {}

for ticker in tickers:
    temp = yf.download(ticker,interval = '5m',period = '1mo')
    temp.dropna(inplace = True,how = 'any')
    ochlv[ticker] = temp
    temp = yf.download(ticker,interval = '1h',period = '1y')
    temp.dropna(inplace = True,how = 'any')
    hour_data[ticker] = temp

def ATR(DF, n=14):
    df = DF.copy()
    df["h-l"] = df["High"] - df["Low"] #high - low
    df["h-pc"] = abs(df ['High'] - df['Adj Close'].shift(1)) #abs of high - previous adj_close
    df["l-pc"] = abs(df ['Low'] - df['Adj Close'].shift(1)) #abs of low - previous adj_close
    df["TR"] = df[['h-l','h-pc','l-pc']].max(axis = 1,skipna=False) # true value = max of above three
    df["ATR"] = df["TR"].ewm(com = n, min_periods=n).mean() #Use span for trading view and com for yahoo finance
    return df["ATR"]    

def renko_DF(DF, hourly_df):
    "function to convert ohlc data into renko bricks"
    df = DF.copy()
    df.reset_index(inplace=True)
    df.drop("Close",axis=1,inplace=True)
    df.columns = ["date","open","high","low","close","volume"]
    df2 = Renko(df)
    df2.brick_size = 3*round(ATR(hourly_df,120).iloc[-1],0)
    renko_df = df2.get_ohlc_data() #if using older version of the library please use get_bricks() instead
    return renko_df

for ticker in ochlv:
    renko_data[ticker] = renko_DF(ochlv[ticker], hour_data[ticker])
    


