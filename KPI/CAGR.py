# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 09:45:41 2023

@author: Danish

CAGR - Compounded Anual Growth Rate 
Formula: (cummilative_Growth)^(1/n) - 1
i.e. (end_value/begining_Value)^(1/n) - 1
"""

import yfinance as yf

tickers = ["AMZN","GOOG","MSFT","JPPOWER.NS"]

ohlcv = {}

for ticker in tickers:
    temp = yf.download(ticker,period = '7mo',interval = '1d')
    temp.dropna(how = 'any',inplace = True)
    ohlcv[ticker] = temp
    
def CAGR(DF):
    df = DF.copy()
    df['Daily_Ret'] = df['Adj Close'].pct_change()
    df['Cum_Ret'] = (1+df['Daily_Ret']).cumprod()
    n = (len(df))/ 245
    CAGR_Value = (df['Cum_Ret'][-1])**(1/n) - 1
    return CAGR_Value

for ticker in ohlcv:
    print('CAGR For {} is {}'.format(ticker,CAGR(ohlcv[ticker])))