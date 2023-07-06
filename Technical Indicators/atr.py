# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 20:58:19 2023

@author: Danish
"""

import yfinance as yf
tickers = ["AMZN","GOOG","MSFT"]

ochlv_data = {}

for ticker in tickers:
    temp = yf.download(ticker,period = "1mo",interval = "5m")
    temp.dropna(inplace =True, how ='any')
    ochlv_data[ticker] = temp;
    
def ATR(DF, n=14):
    df = DF.copy()
    df["h-l"] = df["High"] - df["Low"] #high - low
    df["h-pc"] = abs(df ['High'] - df['Adj Close'].shift(1)) #abs of high - previous adj_close
    df["l-pc"] = abs(df ['Low'] - df['Adj Close'].shift(1)) #abs of low - previous adj_close
    df["TR"] = df[['h-l','h-pc','l-pc']].max(axis = 1,skipna=False) # true value = max of above three
    df["ATR"] = df["TR"].ewm(span = n, min_periods=n).mean() #Use span for trading view and com for yahoo finance
    return df["ATR"]

for ticker in ochlv_data:
    ochlv_data[ticker]["ATR"] = ATR(ochlv_data[ticker])
    