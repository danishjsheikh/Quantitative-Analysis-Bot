# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 10:53:25 2023

@author: Danish
"""

import yfinance as yf 
import numpy as np

tickers = ['AMZN','GOOG','MSFT']
ochlv = {}
for ticker in tickers:
    temp = yf.download(ticker,interval = '5m',period = '1mo')
    temp.dropna(inplace = True,how = 'any')
    ochlv[ticker] = temp
    
def RSI(DF,n=14):
     df = DF.copy()
     df['change'] = df['Adj Close'] - df['Adj Close'].shift(1)
     df['gain'] = np.where(df['change']>=0,df['change'],0)
     df['loss'] = np.where(df['change']<0,(-1)*df['change'],0)
     df['avg gain'] = df['gain'].ewm(alpha = 1/n,min_periods = n).mean()
     df['avg loss'] = df['loss'].ewm(alpha = 1/n,min_periods = n).mean()
     df['rs'] = df['avg gain']/df['avg loss']
     df['rsi'] = 100 - (100/(1+df['rs']))
     return df['rsi']

for ticker in tickers:
    ochlv[ticker]['RSI'] = RSI(ochlv[ticker])