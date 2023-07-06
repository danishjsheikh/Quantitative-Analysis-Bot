# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 10:33:43 2023

@author: Danish
Anuallised Volitality = std of daily return and normailised with sqrt of term
"""

import yfinance as yf
import numpy as np

tickers = ["AMZN","GOOG","MSFT","JPPOWER.NS"]

ohlcv = {}

for ticker in tickers:
    temp = yf.download(ticker,period = '1y',interval = '1d')
    temp.dropna(how = 'any',inplace = True)
    ohlcv[ticker] = temp

def Volitality(DF):
    df = DF.copy()
    df['Daily_Ret'] = df['Adj Close'].pct_change()
    vol = df['Daily_Ret'].std() * np.sqrt(252)
    return vol

for ticker in ohlcv:
    print('Volitatlity For {} is {}'.format(ticker,Volitality(ohlcv[ticker])))